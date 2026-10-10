#!/usr/bin/env python3
"""Local, evidence-bound textbook run harness. Python 3 standard library only."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
from html import unescape
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlparse

STATES = ['started', 'checked', 'reviewed', 'accepted', 'blocked']
TRANSITIONS = {'check': ['started', 'checked', 'reviewed', 'blocked'],
               'review': ['checked'], 'accept': ['reviewed'],
               'resume': ['blocked', 'checked', 'reviewed']}
MANUAL = ['teaching', 'sources', 'exercises', 'figures', 'consistency']
POLICY_KEYS = {'name', 'scopes', 'stages', 'states', 'transitions', 'required_inputs',
               'manual_checks', 'final_forbidden_markers', 'word_count',
               'progress_file', 'limits', 'instructions'}
SPEC_KEYS = {'scope', 'stage', 'chapter', 'title', 'manuscript', 'blueprint',
             'required_content', 'figures', 'materials', 'todos'}
RUN_KEYS = {'id', 'state', 'created_at', 'updated_at', 'spec_path', 'spec_sha256',
            'spec', 'policy_sha256', 'engine_sha256', 'inputs', 'check', 'review', 'events'}

class HarnessError(Exception):
    def __init__(self, message, code=2):
        super().__init__(message)
        self.code = code

def ensure(condition, message):
    if not condition:
        raise HarnessError(message)

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def object_pairs(pairs):
    obj = {}
    for key, value in pairs:
        ensure(key not in obj, f'Duplicate JSON key: {key}')
        obj[key] = value
    return obj

def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=object_pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              HarnessError(f'Invalid JSON number: {value}')))
    except (OSError, UnicodeError, ValueError) as exc:
        raise HarnessError(f'Cannot read JSON {path.name}: {exc}') from exc

def strings(value, label, nonempty=True):
    ensure(isinstance(value, list) and all(isinstance(s, str) and s.strip() for s in value),
           f'{label} must be an array of nonempty strings')
    ensure(not nonempty or bool(value), f'{label} cannot be empty')
    ensure(len(value) == len(set(value)), f'{label} contains duplicates')

def text(value, label):
    ensure(isinstance(value, str) and bool(value.strip()), f'{label} must be nonempty text')

def safe_path(root, name, exists=False):
    text(name, 'path')
    ensure('\x00' not in name and not urlparse(name).scheme, 'Only local project paths are supported')
    path = (root / name).resolve()
    ensure(path != root and path.is_relative_to(root), f'Path escapes project: {name}')
    ensure(path.name not in {'harness.json', '.harness.lock'}, f'Reserved path: {name}')
    ensure(not exists or path.is_file(), f'Missing file: {name}')
    return path

def relative(root, path):
    return str(path.relative_to(root))

def validate_policy(root, doc):
    ensure(isinstance(doc, dict) and set(doc) == {'schema_version', 'policy', 'runs'},
           'Root must contain exactly schema_version, policy, runs')
    ensure(type(doc['schema_version']) is int and doc['schema_version'] == 1, 'Unsupported schema_version')
    p = doc['policy']
    ensure(isinstance(p, dict) and set(p) == POLICY_KEYS, 'Invalid or unknown policy fields')
    text(p['name'], 'policy.name')
    ensure(p['scopes'] == ['blueprint', 'section', 'chapter'], 'Unsupported policy.scopes')
    ensure(p['stages'] == ['draft', 'final'], 'Unsupported policy.stages')
    ensure(p['states'] == STATES and p['transitions'] == TRANSITIONS, 'Unsupported state machine')
    ensure(p['manual_checks'] == MANUAL, 'Required manual checks cannot be removed')
    for key in ['required_inputs', 'final_forbidden_markers', 'limits', 'instructions']:
        strings(p[key], 'policy.' + key)
    for name in p['required_inputs']:
        safe_path(root, name)
    ensure(p['progress_file'] == '教材编写现状与目的.md', 'progress_file must be the project progress record')
    w = p['word_count']
    ensure(isinstance(w, dict) and set(w) == {'method', 'chapter_min', 'chapter_max'}, 'Invalid word_count')
    ensure(w['method'] == 'han_characters_approx', 'Unsupported word count method')
    ensure(type(w['chapter_min']) is int and type(w['chapter_max']) is int and
           0 < w['chapter_min'] <= w['chapter_max'], 'Invalid chapter word bounds')
    ensure(isinstance(doc['runs'], list), 'runs must be an array')
    ids = set()
    for run in doc['runs']:
        ensure(isinstance(run, dict) and set(run) == RUN_KEYS, 'Invalid run fields')
        validate_id(run['id'])
        ensure(run['id'] not in ids, 'Duplicate run id in ledger')
        ids.add(run['id'])
        ensure(run['state'] in STATES and isinstance(run['events'], list) and run['events'], 'Invalid run state/history')
        validate_spec(root, p, run['spec'])
        safe_path(root, run['spec_path'])
        ensure(isinstance(run['inputs'], dict), 'Invalid run input snapshot')
        for key in ['created_at', 'updated_at', 'spec_sha256', 'policy_sha256', 'engine_sha256']:
            text(run[key], 'run.' + key)
        for event in run['events']:
            ensure(isinstance(event, dict) and set(event) == {'at', 'action', 'state', 'details'}, 'Invalid event')
        validate_records(run)
    return p

def validate_records(run):
    check, review = run['check'], run['review']
    if check is not None:
        ensure(isinstance(check, dict) and set(check) == {'at', 'passed', 'snapshot', 'errors', 'pending', 'han_characters_approx'},
               'Invalid check record')
        ensure(type(check['passed']) is bool and isinstance(check['snapshot'], dict), 'Invalid check snapshot')
        strings(check['errors'], 'check.errors', False)
        strings(check['pending'], 'check.pending', False)
    if review is not None:
        ensure(isinstance(review, dict) and set(review) == {'at', 'path', 'sha256', 'evidence'}, 'Invalid review record')
        ensure(isinstance(review['evidence'], dict), 'Invalid review evidence')
    if run['state'] in {'checked', 'reviewed', 'accepted'}:
        ensure(check is not None and check['passed'], 'State requires a passing check record')
    if run['state'] in {'reviewed', 'accepted'}:
        ensure(review is not None, 'State requires review evidence')

def validate_id(value):
    ensure(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', value),
           'id must be 1–80 ASCII letters, digits, dots, underscores or hyphens')

def validate_spec(root, p, spec):
    ensure(isinstance(spec, dict) and set(spec) == SPEC_KEYS, 'Invalid or unknown run spec fields')
    ensure(spec['scope'] in p['scopes'] and spec['stage'] in p['stages'], 'Invalid scope or stage')
    ensure((spec['scope'] == 'blueprint' and spec['chapter'] is None) or
           (spec['scope'] != 'blueprint' and type(spec['chapter']) is int and 1 <= spec['chapter'] <= 10),
           'chapter must be 1–10, or null for blueprint')
    text(spec['title'], 'title')
    manuscript = safe_path(root, spec['manuscript'])
    ensure(manuscript.suffix.lower() == '.md', 'v1 manuscripts must be Markdown')
    ensure(relative(root, manuscript) != p['progress_file'], 'Progress record cannot be a manuscript')
    if spec['scope'] == 'blueprint':
        ensure(spec['blueprint'] is None, 'Blueprint runs use manuscript; blueprint must be null')
    else:
        safe_path(root, spec['blueprint'])
    for key in ['required_content', 'materials', 'todos']:
        strings(spec[key], key, key == 'required_content')
    for name in spec['materials']:
        safe_path(root, name)
    ensure(isinstance(spec['figures'], list), 'figures must be an array')
    ids, paths = set(), set()
    for fig in spec['figures']:
        ensure(isinstance(fig, dict) and set(fig) == {'id', 'file', 'caption', 'source', 'status'}, 'Invalid figure fields')
        for key in ['id', 'caption', 'source']:
            text(fig[key], 'figure.' + key)
        ensure(fig['id'] not in ids, 'Duplicate figure id')
        ids.add(fig['id'])
        ensure(fig['status'] in ['planned', 'ready'], 'Invalid figure status')
        ensure(fig['file'] is not None or fig['status'] == 'planned', 'Ready figure needs file')
        if fig['file'] is not None:
            path = safe_path(root, fig['file'])
            ensure(path not in paths and path != manuscript, 'Duplicate or manuscript figure path')
            paths.add(path)

@contextmanager
def ledger(root):
    config = root / 'harness.json'
    lock_path = root / '.harness.lock'
    ensure(not config.is_symlink() and not lock_path.is_symlink(), 'Ledger and lock cannot be symlinks')
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        original = config.read_bytes()
        doc = read_json(config)
        validate_policy(root, doc)
        before = digest(doc)
        try:
            yield doc
        finally:
            if digest(doc) != before:
                validate_policy(root, doc)
                ensure(config.read_bytes() == original, 'Ledger changed outside the lock; refusing overwrite')
                fd, name = tempfile.mkstemp(prefix='.harness-', suffix='.tmp', dir=root)
                try:
                    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                        json.dump(doc, stream, ensure_ascii=False, indent=2, allow_nan=False)
                        stream.write('\n')
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.replace(name, config)
                    directory = os.open(root, os.O_DIRECTORY)
                    try:
                        os.fsync(directory)
                    finally:
                        os.close(directory)
                finally:
                    if os.path.exists(name):
                        os.unlink(name)

def policy_sha(doc):
    return digest({'schema_version': doc['schema_version'], 'policy': doc['policy']})

def engine_sha():
    return sha(Path(__file__).resolve())

def snapshot(root, names):
    result = {}
    for name in names:
        path = safe_path(root, name, True)
        result[relative(root, path)] = sha(path)
    return result

def event(run, action, state, details):
    at = now()
    run.update(state=state, updated_at=at)
    run['events'].append({'at': at, 'action': action, 'state': state, 'details': details})

def find_run(doc, run_id):
    validate_id(run_id)
    for run in doc['runs']:
        if run['id'] == run_id:
            return run
    raise HarnessError(f'Unknown run: {run_id}')

def stable_json(path):
    before = sha(path)
    value = read_json(path)
    ensure(sha(path) == before, f'JSON changed while reading: {path.name}')
    return value, before

def bind(root, doc, spec_path, spec, spec_hash):
    return {'spec': spec, 'spec_path': relative(root, spec_path), 'spec_sha256': spec_hash,
            'policy_sha256': policy_sha(doc), 'engine_sha256': engine_sha(),
            'inputs': snapshot(root, doc['policy']['required_inputs']), 'check': None, 'review': None}

def stale(root, doc, run):
    reasons = []
    if run['policy_sha256'] != policy_sha(doc):
        reasons.append('policy changed')
    if run['engine_sha256'] != engine_sha():
        reasons.append('engine changed')
    recorded = dict(run['inputs'])
    recorded[run['spec_path']] = run['spec_sha256']
    if run['check'] is not None:
        recorded.update(run['check']['snapshot'])
    if run['review'] is not None:
        recorded[run['review']['path']] = run['review']['sha256']
    for name, expected in recorded.items():
        try:
            if sha(safe_path(root, name, True)) != expected:
                reasons.append(f'file changed: {name}')
        except (HarnessError, OSError):
            reasons.append(f'file missing or unsafe: {name}')
    return reasons

def require_fresh(root, doc, run):
    reasons = stale(root, doc, run)
    if reasons:
        event(run, 'invalidate', 'blocked', reasons)
        raise HarnessError('Evidence is stale; resume, check and review again: ' + '; '.join(reasons), 1)

def require_transition(doc, run, action):
    if run['state'] not in doc['policy']['transitions'][action]:
        event(run, 'rejected:' + action, run['state'], ['Invalid state transition'])
        raise HarnessError(f'Cannot {action} a {run["state"]} run', 1)

def visible_markdown(raw):
    # Comments and fenced examples must not satisfy actual manuscript headings/content.
    raw = re.sub(r'<!--[\s\S]*?-->', '', raw)
    lines, fence = [], None
    for line in raw.splitlines():
        m = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if m:
            token = m.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)

def image_paths(root, manuscript, body):
    refs = re.findall(r'!\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)', body)
    for tag in re.findall(r'<img\b[^>]*>', body, flags=re.I):
        match = re.search(r'\bsrc\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', tag, flags=re.I)
        ensure(match is not None, 'Image tag needs a local src')
        refs.append(next(value for value in match.groups() if value is not None))
    definitions = dict(re.findall(r'^\s*\[([^\]]+)\]:\s*(<[^>]+>|\S+)', body, flags=re.M))
    for match in re.finditer(r'!\[([^\]]*)\]\[([^\]]*)\]', body):
        label = match.group(2) or match.group(1)
        ensure(label in definitions, f'Missing image reference definition: {label}')
        refs.append(definitions[label])
    # Shortcut reference images are also resolved, so they cannot bypass registration.
    for match in re.finditer(r'!\[([^\]]+)\](?![\[(])', body):
        label = match.group(1)
        ensure(label in definitions, f'Missing image reference definition: {label}')
        refs.append(definitions[label])
    paths = set()
    for ref in refs:
        ref = unescape(ref.strip('<>'))
        ensure(not urlparse(ref).scheme and not ref.startswith('//'), 'Images must be saved inside the project')
        path = safe_path(root, str(manuscript.parent / unquote(ref.split('#', 1)[0])), True)
        paths.add(path)
    return paths

def check_manuscript(root, doc, run):
    p, spec = doc['policy'], run['spec']
    errors, pending, files = [], list(spec['todos']), list(p['required_inputs'])
    count = None
    # Files are not locked against editors; compare their hashes across inspection.
    names = files + [spec['manuscript']] + spec['materials']
    if spec['blueprint'] is not None:
        names.append(spec['blueprint'])
    names += [fig['file'] for fig in spec['figures'] if fig['file'] is not None]
    before = {}
    for name in names:
        path = safe_path(root, name)
        if path.is_file():
            before[relative(root, path)] = sha(path)
    def attempt(fn):
        try:
            return fn()
        except (HarnessError, OSError, UnicodeError) as exc:
            errors.append(str(exc))
            return None
    manuscript = attempt(lambda: safe_path(root, spec['manuscript'], True))
    body = None
    if manuscript is not None:
        files.append(spec['manuscript'])
        body = attempt(lambda: visible_markdown(manuscript.read_text(encoding='utf-8')))
    if body is not None:
        if spec['title'] not in body:
            errors.append('Declared title is absent from manuscript')
        for item in spec['required_content']:
            if item not in body:
                errors.append(f'Declared content is absent: {item}')
        count = len(re.findall(r'[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0003134f]', body))
        markers = [marker for marker in p['final_forbidden_markers'] if marker in body]
        pending += [f'Unresolved marker: {m}' for m in markers]
        if spec['scope'] == 'chapter':
            w = p['word_count']
            if not w['chapter_min'] <= count <= w['chapter_max']:
                msg = f'Approximate Han count {count} outside {w["chapter_min"]}–{w["chapter_max"]}'
                (errors if spec['stage'] == 'final' else pending).append(msg)
    blueprint_name = spec['manuscript'] if spec['scope'] == 'blueprint' else spec['blueprint']
    def blueprint_check():
        path = safe_path(root, blueprint_name, True)
        bp = visible_markdown(path.read_text(encoding='utf-8'))
        chinese = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
                   '七': 7, '八': 8, '九': 9, '十': 10}
        nums = []
        for s in re.findall(r'^#{1,6}\s+第(\d+|[一二三四五六七八九十]+)章[^\n]*', bp, re.M):
            nums.append(int(s) if s.isdigit() else chinese.get(s, -1))
        ensure(sorted(nums) == list(range(1, 11)), 'Blueprint needs exactly ten chapter headings, numbered 1–10')
        files.append(blueprint_name)
    attempt(blueprint_check)
    for name in spec['materials']:
        path = attempt(lambda n=name: safe_path(root, n, True))
        if path is not None:
            files.append(name)
    registered = set()
    for fig in spec['figures']:
        path = safe_path(root, fig['file']) if fig['file'] is not None else None
        if fig['status'] == 'planned':
            pending.append(f'Planned figure: {fig["id"]}')
        if path is not None and path.is_file():
            files.append(fig['file'])
        if fig['status'] == 'ready':
            if path is None or not path.is_file():
                errors.append(f'Ready figure missing: {fig["id"]}')
            else:
                registered.add(path)
            if body is not None and (fig['id'] not in body or fig['caption'] not in body):
                errors.append(f'Figure id/caption absent from manuscript: {fig["id"]}')
    if body is not None:
        used = attempt(lambda: image_paths(root, manuscript, body))
        if used is not None:
            for path in sorted(used - registered):
                errors.append(f'Image not registered ready: {relative(root, path)}')
            for path in sorted(registered - used):
                errors.append(f'Ready figure not embedded in manuscript: {relative(root, path)}')
    if spec['stage'] == 'final':
        errors += [f'Final cannot contain pending item: {s}' for s in pending]
    captured = attempt(lambda: snapshot(root, files)) or {}
    for name, value in captured.items():
        if before.get(name) != value:
            errors.append(f'File changed during check: {name}')
    return {'at': now(), 'passed': not errors, 'snapshot': captured,
            'errors': list(dict.fromkeys(errors)), 'pending': list(dict.fromkeys(pending)),
            'han_characters_approx': count}

def validate_review(doc, run, evidence):
    fields = {'reviewer', 'reviewed_at', 'policy_sha256', 'engine_sha256', 'snapshot', 'checks'}
    ensure(isinstance(evidence, dict) and set(evidence) == fields, 'Invalid review evidence fields')
    text(evidence['reviewer'], 'reviewer')
    ensure('待填写' not in evidence['reviewer'], 'reviewer must identify the actual reviewer')
    try:
        time = datetime.fromisoformat(evidence['reviewed_at'])
        ensure(time.tzinfo is not None and time >= datetime.fromisoformat(run['check']['at']) and
               time <= datetime.now(timezone.utc), 'Review timestamp must follow check and cannot be in the future')
    except (TypeError, ValueError):
        raise HarnessError('reviewed_at must be ISO-8601 with timezone')
    ensure(evidence['policy_sha256'] == run['policy_sha256'] and evidence['engine_sha256'] == run['engine_sha256'],
           'Review policy/engine hash mismatch')
    ensure(evidence['snapshot'] == run['check']['snapshot'], 'Review snapshot mismatch')
    checks = evidence['checks']
    ensure(isinstance(checks, dict) and set(checks) == set(doc['policy']['manual_checks']), 'Missing or unknown manual check')
    for name, row in checks.items():
        ensure(isinstance(row, dict) and set(row) == {'status', 'notes'}, f'Invalid review row: {name}')
        text(row['notes'], f'{name}.notes')
        ensure(row['notes'] != '待完成实际审校后填写依据', f'{name}.notes must describe actual inspection')
        ensure(row['status'] in ['pass', 'pending', 'na'], f'Invalid review status: {name}')
        ensure(row['status'] != 'na' or name not in ['teaching', 'consistency'], f'{name} cannot be NA')
        ensure(name not in ['teaching', 'consistency'] or row['status'] == 'pass',
               f'{name} must pass for the current scope/stage')
        ensure(row['status'] != 'pending' or run['spec']['stage'] == 'draft', 'Final manual review cannot be pending')
        if name == 'figures' and run['spec']['figures']:
            ensure(row['status'] != 'na', 'Declared figures need actual figure review')
        if name == 'figures' and run['spec']['scope'] == 'chapter' and run['spec']['stage'] == 'final':
            ensure(row['status'] == 'pass', 'Final chapter needs figure-plan review')

def require_progress(root, doc, run):
    path = safe_path(root, doc['policy']['progress_file'], True)
    body = visible_markdown(path.read_text(encoding='utf-8'))
    links = re.findall(r'(?<!!)\[[^\]]+\]\(\s*(<[^>]+>|[^\s)]+)', body)
    expected = safe_path(root, run['spec']['manuscript'], True)
    for link in links:
        link = unquote(link.strip('<>')).split('#', 1)[0]
        # Codex local file links may include a one-based line suffix.
        link = re.sub(r':\d+$', '', link)
        if urlparse(link).scheme:
            continue
        try:
            if safe_path(root, str(path.parent / link)) == expected:
                return
        except HarnessError:
            pass
    raise HarnessError('Update the actual progress record with a Markdown link to this manuscript before accept', 1)

def execute(root, doc, args):
    p = doc['policy']
    if args.command == 'validate':
        return {'valid': True, 'policy_sha256': policy_sha(doc), 'engine_sha256': engine_sha(), 'runs': len(doc['runs'])}
    if args.command == 'start':
        validate_id(args.id)
        ensure(not any(r['id'] == args.id for r in doc['runs']), 'Run id already exists; existing run preserved')
        path = safe_path(root, args.spec, True)
        spec, spec_hash = stable_json(path)
        validate_spec(root, p, spec)
        run = {'id': args.id, 'created_at': now(), 'updated_at': now(), 'state': 'started', 'events': []}
        run.update(bind(root, doc, path, spec, spec_hash))
        event(run, 'start', 'started', ['Inputs, spec, policy and engine captured'])
        doc['runs'].append(run)
        return run
    if args.command == 'status':
        targets = [find_run(doc, args.id)] if args.id else doc['runs']
        any_stale = False
        for run in targets:
            reasons = stale(root, doc, run)
            if reasons:
                any_stale = True
                if run['state'] != 'blocked' or run['events'][-1]['details'] != reasons:
                    event(run, 'invalidate', 'blocked', reasons)
        return {'runs': targets, 'stale': any_stale}
    run = find_run(doc, args.id)
    require_transition(doc, run, args.command)
    if args.command == 'resume':
        path = safe_path(root, run['spec_path'], True)
        spec, spec_hash = stable_json(path)
        validate_spec(root, p, spec)
        bindings = bind(root, doc, path, spec, spec_hash)
        # Events retain prior evidence; current proofs are explicitly reset.
        event(run, 'resume', 'started', {'previous_check': run['check'], 'previous_review': run['review']})
        run.update(bindings)
        return run
    require_fresh(root, doc, run)
    if args.command == 'check':
        result = check_manuscript(root, doc, run)
        require_fresh(root, doc, run)
        run.update(check=result, review=None)
        event(run, 'check', 'checked' if result['passed'] else 'blocked', result)
        if not result['passed']:
            raise HarnessError('Mechanical checks failed: ' + '; '.join(result['errors']), 1)
    elif args.command == 'review':
        try:
            path = safe_path(root, args.evidence, True)
            ensure(relative(root, path) not in run['check']['snapshot'] and relative(root, path) != run['spec_path'],
                   'Review evidence must be a separate file')
            evidence, evidence_hash = stable_json(path)
            validate_review(doc, run, evidence)
            require_fresh(root, doc, run)
        except HarnessError as exc:
            event(run, 'review', 'blocked', [str(exc)])
            raise HarnessError(str(exc), 1) from exc
        run['review'] = {'at': now(), 'path': relative(root, path), 'sha256': evidence_hash, 'evidence': evidence}
        event(run, 'review', 'reviewed', run['review'])
    elif args.command == 'accept':
        try:
            validate_review(doc, run, run['review']['evidence'])
            require_progress(root, doc, run)
            require_fresh(root, doc, run)
        except HarnessError as exc:
            event(run, 'accept', 'blocked', [str(exc)])
            raise HarnessError(str(exc), 1) from exc
        event(run, 'accept', 'accepted', {'scope': run['spec']['scope'], 'stage': run['spec']['stage'],
                                          'snapshot': run['check']['snapshot'], 'review_sha256': run['review']['sha256']})
    return run

def parser():
    description = '''Evidence-bound textbook runs (Python 3.11+, stdlib, Linux file locking).
Exit codes: 0 success, 1 gate rejection, 2 invalid input/config.
Draft accepts explicitly pending work; final rejects todos, unresolved markers,
planned figures, pending reviews, and out-of-range whole-chapter Han count.
Accept applies only to the declared scope/stage; a draft acceptance is not final.
The engine does not prove teaching quality or enforce other Codex tool use.
'''
    epilog = '''Workflow:
  start --id ch01-s01-draft --spec runs/ch01-s01.spec.json
  check --id ch01-s01-draft
  review-template --id ch01-s01-draft > runs/ch01-s01.review.json
  (Actually inspect files, edit each review row, reviewer and reviewed_at.)
  review --id ch01-s01-draft --evidence runs/ch01-s01.review.json
  (Update 教材编写现状与目的.md with manuscript link/status/figure progress.)
  accept --id ch01-s01-draft
  status --id ch01-s01-draft
  resume --id ch01-s01-draft  (reset stale/blocked proofs; retain events)
Spec: templates/run.example.json; blueprint scope uses chapter=null, blueprint=null.
Figure: {id,file,caption,source,status:planned|ready}; planned file may be null.
materials: local citation ledgers, data and editable diagram sources to hash.
Review: {reviewer,reviewed_at,policy_sha256,engine_sha256,snapshot,checks}.
checks: teaching/sources/exercises/figures/consistency -> {status:pass|pending|na,notes}.
review-template emits pending rows; it never emits a passing review.
'''
    p = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--root', default=str(Path(__file__).resolve().parents[1]), help='Project directory containing harness.json')
    subs = p.add_subparsers(dest='command', required=True)
    for command in ['validate', 'start', 'check', 'review-template', 'review', 'accept', 'status', 'resume']:
        child = subs.add_parser(command)
        if command != 'validate':
            child.add_argument('--id', required=command != 'status')
        if command == 'start':
            child.add_argument('--spec', required=True)
        if command == 'review':
            child.add_argument('--evidence', required=True)
    return p

def main():
    args = parser().parse_args()
    root = Path(args.root).resolve()
    try:
        ensure(root.is_dir(), 'Project root does not exist')
        with ledger(root) as doc:
            if args.command == 'review-template':
                run = find_run(doc, args.id)
                ensure(run['state'] == 'checked', 'review-template requires checked state')
                require_fresh(root, doc, run)
                result = {'reviewer': '待填写实际审校者', 'reviewed_at': now(),
                          'policy_sha256': run['policy_sha256'], 'engine_sha256': run['engine_sha256'],
                          'snapshot': run['check']['snapshot'],
                          'checks': {name: {'status': 'pending', 'notes': '待完成实际审校后填写依据'} for name in MANUAL}}
            else:
                result = execute(root, doc, args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.command == 'status' and result['stale'] else 0
    except (HarnessError, OSError, UnicodeError) as exc:
        print(json.dumps({'error': str(exc), 'command': args.command}, ensure_ascii=False), file=sys.stderr)
        return exc.code if isinstance(exc, HarnessError) else 2

if __name__ == '__main__':
    sys.exit(main())

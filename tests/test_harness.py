"""Independent CLI acceptance tests, isolated from real textbook artifacts."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]

class HarnessAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='教材-harness-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        shutil.copyfile(PROJECT / 'scripts/harness.py', self.root / 'scripts/harness.py')
        self.config = json.loads((PROJECT / 'harness.json').read_text(encoding='utf-8'))
        self.config['runs'] = []
        self.save_config()
        for name in self.config['policy']['required_inputs']:
            (self.root / name).write_bytes(b'fixture input; hash checking only')
        self.write('十章编写蓝图.md', '# 十章蓝图\n' + '\n'.join(f'## 第{i}章 标题{i}' for i in range(1, 11)))
        self.write('manuscripts/一节 稿件.md', '# 问题分解\n## 学习目标\n具体目标\n## 案例\n问题情境\n## 方法\n判断过程\n## 反思\n调整依据\n')
        self.write('教材编写现状与目的.md', '[稿件](<manuscripts/一节 稿件.md>)\n第1章单节初稿；已完成目标与方法，配图不适用。')
        self.spec = {'scope': 'section', 'stage': 'draft', 'chapter': 1, 'title': '问题分解',
                     'manuscript': 'manuscripts/一节 稿件.md', 'blueprint': '十章编写蓝图.md',
                     'required_content': ['学习目标', '案例', '方法', '反思'], 'figures': [], 'materials': [], 'todos': []}
        self.save_spec()

    def write(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding='utf-8')
        return path

    def save_config(self):
        self.write('harness.json', json.dumps(self.config, ensure_ascii=False, indent=2) + '\n')

    def save_spec(self, name='runs/section.spec.json'):
        self.write(name, json.dumps(self.spec, ensure_ascii=False, indent=2) + '\n')

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.root / 'scripts/harness.py'), '--root', str(self.root), *args],
                              capture_output=True, text=True, encoding='utf-8', timeout=20)

    def success(self, *args):
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def failure(self, *args, code=None, contains=None):
        result = self.cli(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        if code is not None:
            self.assertEqual(result.returncode, code, result.stderr)
        if result.stderr:
            error = json.loads(result.stderr)['error']
        else:
            report = json.loads(result.stdout)
            self.assertTrue(report['stale'])
            error = 'stale'
        if contains:
            self.assertIn(contains, error)
        return result

    def run_record(self, run_id='fixture'):
        doc = json.loads((self.root / 'harness.json').read_text(encoding='utf-8'))
        return next(run for run in doc['runs'] if run['id'] == run_id)

    def start(self, run_id='fixture'):
        return self.success('start', '--id', run_id, '--spec', 'runs/section.spec.json')

    def check(self, run_id='fixture'):
        return self.success('check', '--id', run_id)

    def evidence(self, run_id='fixture', statuses=None, kind='ai_self'):
        run = self.run_record(run_id)
        evidence = {'reviewer': 'parent fixture reviewer', 'reviewed_at': datetime.now(timezone.utc).isoformat(),
                    'review_kind': kind, 'spec_sha256': run['spec_sha256'],
                    'policy_sha256': run['policy_sha256'], 'engine_sha256': run['engine_sha256'],
                    'snapshot': run['check']['snapshot'],
                    'checks': {key: {'status': 'pass', 'notes': f'Fixture inspection of {key}; not a real textbook review.'}
                               for key in self.config['policy']['manual_checks']}}
        for key, status in (statuses or {}).items():
            evidence['checks'][key]['status'] = status
        self.write('runs/review.json', json.dumps(evidence, ensure_ascii=False))
        return evidence

    def review(self):
        return self.success('review', '--id', 'fixture', '--evidence', 'runs/review.json')

    def accepted(self):
        self.start()
        self.check()
        self.evidence()
        self.review()
        return self.success('accept', '--id', 'fixture')

    def add_figure(self):
        self.write('assets/图 1.svg', '<svg xmlns="http://www.w3.org/2000/svg"><text>教学示例</text></svg>')
        path = self.root / self.spec['manuscript']
        path.write_text(path.read_text(encoding='utf-8') + '\n![关系图](<../assets/图 1.svg>)\n图1-1 问题关系\n', encoding='utf-8')
        self.spec['figures'] = [{'id': '图1-1', 'file': 'assets/图 1.svg', 'caption': '问题关系', 'source': '自绘教学示例', 'status': 'ready'}]
        self.save_spec()

    def test_bundle_is_json_with_policy_and_runs(self):
        self.assertIsInstance(self.config['policy'], dict)
        self.assertIsInstance(self.config['runs'], list)
        self.assertFalse(self.config['runs'])
        self.assertFalse((PROJECT / 'HARNESS.md').exists())

    def test_cli_exposes_help(self):
        result = self.cli('--help')
        self.assertEqual(result.returncode, 0)
        for command in ('validate', 'start', 'check', 'review', 'accept', 'resume', 'status'):
            self.assertIn(command, result.stdout)

    def test_policy_validates_without_assuming_real_project_is_empty(self):
        self.assertTrue(self.success('validate')['valid'])
        result = subprocess.run([sys.executable, str(PROJECT / 'scripts/harness.py'), 'validate'],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['valid'])

    def test_malformed_json_does_not_damage_ledger(self):
        bad = b'{"policy": '
        (self.root / 'harness.json').write_bytes(bad)
        self.failure('status', code=2)
        self.assertEqual((self.root / 'harness.json').read_bytes(), bad)

    def test_invalid_policy_type_does_not_damage_ledger(self):
        self.config['policy'] = 'invalid'
        self.save_config()
        before = (self.root / 'harness.json').read_bytes()
        self.failure('status', code=2)
        self.assertEqual((self.root / 'harness.json').read_bytes(), before)

    def test_unknown_policy_fields_fail_closed(self):
        self.config['policy']['pretend_gate'] = True
        self.save_config()
        self.failure('validate', code=2, contains='policy fields')

    def test_duplicate_json_keys_and_nan_fail_closed(self):
        for raw in ('{"schema_version":1,"schema_version":1}', '{"schema_version":NaN}'):
            with self.subTest(raw=raw):
                self.write('harness.json', raw)
                self.failure('validate', code=2)
                self.assertEqual((self.root / 'harness.json').read_text(), raw)

    def test_full_section_lifecycle_and_history(self):
        run = self.accepted()
        self.assertEqual(run['state'], 'accepted')
        self.assertEqual([e['action'] for e in run['events']], ['start', 'check', 'review', 'accept'])
        self.assertEqual(run['spec']['stage'], 'draft')
        self.assertGreater(run['check']['han_characters_approx'], 0)
        for event in run['events']:
            self.assertIsNotNone(datetime.fromisoformat(event['at']).tzinfo)
        self.assertFalse(self.success('status', '--id', 'fixture')['stale'])

    def test_status_summary_keeps_history_available_without_mutation(self):
        self.accepted()
        before = (self.root/'harness.json').read_bytes()
        summary = self.success('status')['runs'][0]
        self.assertEqual(summary['effective_state'], 'accepted')
        self.assertEqual(summary['manuscript'], self.spec['manuscript'])
        self.assertNotIn('events', summary)
        detail = self.success('status', '--id', 'fixture')['runs'][0]
        self.assertEqual(len(detail['events']), 4)
        self.assertEqual(detail['review']['evidence']['review_kind'], 'ai_self')
        self.assertEqual((self.root/'harness.json').read_bytes(), before)

    def test_legacy_started_status_resume_flow_still_works(self):
        self.start()
        self.spec['todos'] = ['真实待办']
        self.save_spec()
        self.failure('status', '--id', 'fixture', code=1)
        self.assertEqual(self.run_record()['state'], 'started')
        self.success('resume', '--id', 'fixture')
        self.assertEqual(self.check()['state'], 'checked')

    def test_section_is_not_subject_to_whole_chapter_word_budget(self):
        self.spec['stage'] = 'final'
        self.save_spec()
        self.accepted()
        self.assertEqual(self.run_record()['state'], 'accepted')

    def test_cannot_skip_check_or_review(self):
        self.start()
        self.failure('accept', '--id', 'fixture', code=1)
        self.check()
        self.failure('accept', '--id', 'fixture', code=1)
        self.assertEqual(self.run_record()['state'], 'checked')

    def test_duplicate_id_preserves_existing_run(self):
        self.start()
        before = (self.root / 'harness.json').read_bytes()
        self.failure('start', '--id', 'fixture', '--spec', 'runs/section.spec.json', code=2)
        self.assertEqual((self.root / 'harness.json').read_bytes(), before)

    def test_draft_records_pending_items_and_final_rejects_them(self):
        self.spec['todos'] = ['核验来源']
        self.spec['figures'] = [{'id': '图1-1', 'file': None, 'caption': '关系图', 'source': '计划自绘', 'status': 'planned'}]
        self.save_spec()
        self.start()
        run = self.check()
        self.assertTrue(run['check']['pending'])
        self.evidence(statuses={'sources': 'pending', 'figures': 'pending'})
        self.review()
        self.success('accept', '--id', 'fixture')
        self.spec['stage'] = 'final'
        self.save_spec()
        self.success('start', '--id', 'final', '--spec', 'runs/section.spec.json')
        self.failure('check', '--id', 'final', code=1, contains='pending')

    def test_final_rejects_explicit_placeholder(self):
        self.spec['stage'] = 'final'
        self.save_spec()
        path = self.root / self.spec['manuscript']
        path.write_text(path.read_text() + '\n【待核验】事实\n')
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='待核验')

    def test_required_content_in_comments_and_fences_does_not_count(self):
        self.write(self.spec['manuscript'], '# 问题分解\n<!-- 学习目标 案例 方法 反思 -->\n```text\n学习目标 案例 方法 反思\n```\n')
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='content is absent')

    def test_missing_manuscript_blocks(self):
        (self.root / self.spec['manuscript']).unlink()
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='Missing file')

    def test_missing_blueprint_ninth_chapter_blocks(self):
        self.write('十章编写蓝图.md', '# 十章蓝图\n' + '\n'.join(f'## 第{i}章 内容' for i in range(1, 11) if i != 9))
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='ten chapter headings')

    def test_blueprint_scope_accepts_ten_real_headings(self):
        self.spec.update(scope='blueprint', chapter=None, title='十章蓝图', manuscript='十章编写蓝图.md', blueprint=None,
                         required_content=['第9章'])
        self.save_spec()
        self.write('教材编写现状与目的.md', '[蓝图](十章编写蓝图.md)\n初稿已列十章，教学方案仍待细化。')
        self.accepted()

    def test_final_short_chapter_fails_approximate_budget(self):
        self.spec.update(scope='chapter', stage='final')
        self.save_spec()
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='Approximate Han count')

    def test_missing_ready_figure_blocks_draft_too(self):
        self.add_figure()
        (self.root / 'assets/图 1.svg').unlink()
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='figure missing')

    def test_unregistered_inline_reference_and_html_images_block(self):
        variants = ['![图](<../assets/图 1.svg>)', '![图][img]\n[img]: <../assets/图 1.svg>',
                    '<img src="../assets/图 1.svg">', '![img]\n[img]: <../assets/图 1.svg>']
        self.add_figure()
        self.spec['figures'] = []
        self.save_spec()
        original = '# 问题分解\n学习目标 案例 方法 反思\n'
        for i, variant in enumerate(variants):
            with self.subTest(variant=variant):
                self.write(self.spec['manuscript'], original + variant)
                self.start(str(i))
                self.failure('check', '--id', str(i), code=1, contains='not registered')

    def test_ready_figure_must_have_caption_and_be_embedded(self):
        self.add_figure()
        self.write(self.spec['manuscript'], '# 问题分解\n学习目标 案例 方法 反思\n')
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='caption absent')

    def test_changed_figure_invalidates_accepted_run(self):
        self.add_figure()
        self.accepted()
        self.write('assets/图 1.svg', '<svg/>')
        before = (self.root / 'harness.json').read_bytes()
        self.failure('status', '--id', 'fixture', code=1)
        self.assertEqual(self.run_record()['state'], 'accepted')
        self.assertEqual((self.root / 'harness.json').read_bytes(), before)
        report = json.loads(self.cli('status', '--id', 'fixture').stdout)['runs'][0]
        self.assertEqual(report['effective_state'], 'blocked')
        self.assertIn('file changed: assets/图 1.svg', report['stale_reasons'])
        self.assertTrue(any(e['action'] == 'accept' for e in self.run_record()['events']))

    def test_changed_manuscript_core_source_blueprint_and_material_invalidate(self):
        names = [self.spec['manuscript'], self.config['policy']['required_inputs'][0], '十章编写蓝图.md', 'materials/引用台账.json']
        self.write('materials/引用台账.json', '{"claims":[]}')
        self.spec['materials'] = ['materials/引用台账.json']
        self.save_spec()
        self.start()
        for name in names:
            with self.subTest(name=name):
                self.check()
                self.evidence()
                self.review()
                with (self.root / name).open('ab') as stream:
                    stream.write(b'\n ')
                self.failure('accept', '--id', 'fixture', code=1, contains='stale')
                self.success('resume', '--id', 'fixture')
        self.assertGreater(len(self.run_record()['events']), 10)

    def test_policy_changes_invalidate_but_other_runs_do_not(self):
        self.accepted()
        self.start('other')
        self.assertFalse(self.success('status', '--id', 'fixture')['stale'])
        doc = json.loads((self.root / 'harness.json').read_text())
        doc['policy']['instructions'].append('New routing instruction')
        doc['policy']['limits'].append('Clarify a limitation without changing a gate')
        doc['policy']['name'] = 'Updated display name'
        self.write('harness.json', json.dumps(doc, ensure_ascii=False))
        self.assertFalse(self.success('status', '--id', 'fixture')['stale'])
        doc['policy']['word_count']['chapter_min'] += 1
        self.write('harness.json', json.dumps(doc, ensure_ascii=False))
        self.failure('status', '--id', 'fixture', code=1)
        self.failure('accept', '--id', 'fixture', code=1, contains='stale')

    def test_engine_change_invalidates(self):
        self.accepted()
        with (self.root / 'scripts/harness.py').open('a') as stream:
            stream.write('\n# changed implementation\n')
        self.failure('status', '--id', 'fixture', code=1)

    def test_review_file_change_invalidates(self):
        self.accepted()
        with (self.root / 'runs/review.json').open('a') as stream:
            stream.write('\n')
        self.failure('status', '--id', 'fixture', code=1)

    def test_wrong_snapshot_and_missing_manual_rows_rejected(self):
        self.start()
        self.check()
        evidence = self.evidence()
        evidence['snapshot'] = {}
        self.write('runs/review.json', json.dumps(evidence))
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1, contains='snapshot mismatch')
        self.success('resume', '--id', 'fixture')
        self.check()
        evidence = self.evidence()
        del evidence['checks']['teaching']
        self.write('runs/review.json', json.dumps(evidence))
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1, contains='manual check')

    def test_final_manual_pending_and_teaching_na_rejected(self):
        self.spec['stage'] = 'final'
        self.save_spec()
        self.start()
        self.check()
        self.evidence(statuses={'sources': 'pending'})
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1, contains='cannot be pending')
        self.success('resume', '--id', 'fixture')
        self.check()
        self.evidence(statuses={'teaching': 'na'})
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1, contains='cannot be NA')

    def test_review_template_contains_no_automatic_pass(self):
        self.start()
        self.check()
        evidence = self.success('review-template', '--id', 'fixture')
        self.assertEqual({r['status'] for r in evidence['checks'].values()}, {'pending'})
        self.write('runs/review.json', json.dumps(evidence))
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1, contains='reviewer')

    def test_draft_teaching_review_cannot_remain_pending(self):
        self.start()
        self.check()
        self.evidence(statuses={'teaching': 'pending'})
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1, contains='must pass')

    def test_unquoted_html_image_cannot_bypass_registration(self):
        self.write('assets/figure.svg', '<svg/>')
        self.write(self.spec['manuscript'], '# 问题分解\n学习目标 案例 方法 反思\n<img src=../assets/figure.svg>')
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='not registered')

    def test_file_changed_during_check_cannot_receive_passing_proof(self):
        self.start()
        module_spec = importlib.util.spec_from_file_location('fixture_harness', self.root / 'scripts/harness.py')
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        original_snapshot = module.snapshot
        def changed_snapshot(root, names):
            with (root / self.spec['manuscript']).open('a') as stream:
                stream.write('\nchanged during inspection')
            return original_snapshot(root, names)
        doc = json.loads((self.root / 'harness.json').read_text())
        with patch.object(module, 'snapshot', side_effect=changed_snapshot):
            result = module.check_manuscript(self.root, doc, doc['runs'][0])
        self.assertFalse(result['passed'])
        self.assertTrue(any('changed during check' in error for error in result['errors']))

    def test_forged_progress_path_and_plaintext_link_do_not_pass(self):
        self.config['policy']['progress_file'] = 'fake.md'
        self.save_config()
        self.failure('validate', code=2, contains='progress_file')
        self.config['policy']['progress_file'] = '教材编写现状与目的.md'
        self.save_config()
        self.start()
        self.check()
        self.evidence()
        self.review()
        self.write('教材编写现状与目的.md', 'manuscripts/一节 稿件.md （只写路径，没有产物链接）')
        self.failure('accept', '--id', 'fixture', code=1, contains='Markdown link')

    def test_progress_updates_do_not_invalidate_review_snapshot(self):
        self.accepted()
        self.write('教材编写现状与目的.md', '[稿件](<manuscripts/一节 稿件.md>)\n初稿已验收；开始下一章。')
        self.assertFalse(self.success('status', '--id', 'fixture')['stale'])

    def test_outside_root_and_symlink_escape_rejected(self):
        outside = Path(self.temp.name).parent / (self.root.name + '-outside.md')
        outside.write_text('outside')
        self.addCleanup(outside.unlink)
        for name in [str(outside), 'escape.md']:
            if name == 'escape.md':
                (self.root / name).symlink_to(outside)
            self.spec['manuscript'] = name
            self.save_spec()
            self.failure('start', '--id', 'fixture', '--spec', 'runs/section.spec.json', code=2, contains='escapes')
        self.assertEqual(outside.read_text(), 'outside')

    def test_blocked_resume_preserves_failure_and_clears_current_proofs(self):
        path = self.root / self.spec['manuscript']
        original = path.read_text()
        self.write(self.spec['manuscript'], '# 问题分解\n')
        self.start()
        self.failure('check', '--id', 'fixture', code=1)
        self.write(self.spec['manuscript'], original)
        run = self.success('resume', '--id', 'fixture')
        self.assertEqual(run['state'], 'started')
        self.assertIsNone(run['check'])
        self.assertIsNone(run['review'])
        self.assertFalse(run['events'][1]['details']['passed'])
        self.check()

    def test_concurrent_start_preserves_both_runs(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda i: self.cli('start', '--id', i, '--spec', 'runs/section.spec.json'), ['one', 'two']))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        doc = json.loads((self.root / 'harness.json').read_text())
        self.assertEqual({run['id'] for run in doc['runs']}, {'one', 'two'})

    def test_editing_started_spec_rechecks_without_status_or_resume(self):
        self.start()
        self.spec['todos'] = ['真实初稿待办']
        self.save_spec()
        run = self.check()
        self.assertEqual(run['spec'], self.spec)
        self.assertIn('真实初稿待办', run['check']['pending'])
        self.assertEqual([e['action'] for e in run['events']], ['start', 'refresh', 'check'])

    def test_unchanged_recheck_keeps_review_and_ledger_bytes(self):
        for checkpoint in ['checked', 'reviewed', 'accepted']:
            with self.subTest(checkpoint=checkpoint):
                self.start(checkpoint)
                self.check(checkpoint)
                if checkpoint != 'checked':
                    self.evidence(checkpoint)
                    self.success('review', '--id', checkpoint, '--evidence', 'runs/review.json')
                if checkpoint == 'accepted':
                    self.success('accept', '--id', checkpoint)
                before = (self.root / 'harness.json').read_bytes()
                self.assertEqual(self.check(checkpoint)['state'], checkpoint)
                self.assertEqual((self.root / 'harness.json').read_bytes(), before)

    def test_accepted_revision_rechecks_and_old_review_cannot_be_reused(self):
        old = self.accepted()
        old_evidence = old['review']['evidence']
        with (self.root / self.spec['manuscript']).open('a') as stream:
            stream.write('\n新的教学解释\n')
        updated = self.check()
        self.assertEqual(updated['state'], 'checked')
        self.assertIsNone(updated['review'])
        self.assertIn('accept', [e['action'] for e in updated['events']])
        self.assertNotEqual(updated['check']['snapshot'], old['check']['snapshot'])
        self.write('runs/review.json', json.dumps(old_evidence))
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1)
        self.evidence()
        self.review()
        self.success('accept', '--id', 'fixture')
        self.assertEqual(len([e for e in self.run_record()['events'] if e['action'] == 'accept']), 2)

    def test_fixed_review_and_progress_retry_without_rechecking(self):
        self.start()
        self.check()
        checked = self.run_record()['check']
        evidence = self.evidence()
        evidence['checks']['teaching']['status'] = 'pending'
        self.write('runs/review.json', json.dumps(evidence))
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1)
        self.evidence()
        self.review()
        self.write('教材编写现状与目的.md', '进度链接暂缺')
        self.failure('accept', '--id', 'fixture', code=1)
        self.write('教材编写现状与目的.md', '[稿件](<manuscripts/一节 稿件.md>)\n范围section/draft，配图不适用，无待办。')
        run = self.success('accept', '--id', 'fixture')
        self.assertEqual(run['check'], checked)
        self.assertEqual(len([e for e in run['events'] if e['action'] == 'check']), 1)
        self.assertEqual(run['events'][-1]['details']['review_kind'], 'ai_self')
        self.assertEqual(run['events'][-1]['details']['progress_sha256'],
                         hashlib.sha256((self.root / '教材编写现状与目的.md').read_bytes()).hexdigest())

    def test_recovery_never_bypasses_missing_or_stale_proofs(self):
        self.start()
        self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1)
        self.failure('accept', '--id', 'fixture', code=1)
        self.check()
        self.evidence()
        self.write('教材编写现状与目的.md', '链接暂缺')
        self.review()
        self.failure('accept', '--id', 'fixture', code=1)
        with (self.root / self.spec['manuscript']).open('a') as stream:
            stream.write('\n改变稿件\n')
        self.write('教材编写现状与目的.md', '[稿件](<manuscripts/一节 稿件.md>)')
        self.failure('accept', '--id', 'fixture', code=1, contains='stale')

    def test_review_kind_and_spec_binding_are_required_for_new_reviews(self):
        self.start()
        self.check()
        for field, value in [('review_kind', None), ('review_kind', 'pretend-independent'),
                             ('spec_sha256', 'wrong')]:
            with self.subTest(field=field, value=value):
                evidence = self.evidence()
                if value is None:
                    del evidence[field]
                else:
                    evidence[field] = value
                self.write('runs/review.json', json.dumps(evidence))
                self.failure('review', '--id', 'fixture', '--evidence', 'runs/review.json', code=1)
                self.check()
        for kind in ['ai_self', 'independent', 'human']:
            with self.subTest(kind=kind):
                self.evidence(kind=kind)
                run = self.review()
                self.assertEqual(run['review']['evidence']['review_kind'], kind)
                self.assertEqual(self.success('status', '--id', 'fixture')['runs'][0]['review_kind'], kind)
                self.success('resume', '--id', 'fixture')
                self.check()

    def test_invalid_spec_refresh_leaves_saved_evidence_untouched(self):
        self.accepted()
        before = (self.root / 'harness.json').read_bytes()
        self.spec['manuscript'] = '../outside.md'
        self.save_spec()
        self.failure('check', '--id', 'fixture', code=2, contains='escapes')
        self.assertEqual((self.root / 'harness.json').read_bytes(), before)
        self.failure('status', '--id', 'fixture', code=1)

    def test_recheck_captures_a_newly_created_planned_figure(self):
        self.spec['figures'] = [{'id': '图1-1', 'file': 'assets/planned.svg', 'caption': '关系图',
                                'source': '计划自绘', 'status': 'planned'}]
        self.save_spec()
        self.start()
        self.check()
        self.assertNotIn('assets/planned.svg', self.run_record()['check']['snapshot'])
        self.write('assets/planned.svg', '<svg/>')
        self.failure('status', '--id', 'fixture', code=1)
        self.assertIn('assets/planned.svg', self.check()['check']['snapshot'])

    def test_final_chapter_requires_actual_registered_figures(self):
        self.spec.update(scope='chapter', stage='final')
        self.save_spec()
        with (self.root / self.spec['manuscript']).open('a') as stream:
            stream.write('教' * 30000)
        self.start()
        self.failure('check', '--id', 'fixture', code=1, contains='figure')

    def test_ten_chapters_deliver_without_per_section_runs(self):
        for chapter in range(1, 11):
            run_id = f'ch{chapter:02d}'
            name = f'manuscripts/ch{chapter:02d}.md'
            self.spec.update(scope='chapter', stage='final', chapter=chapter, manuscript=name)
            self.write(name, '# 问题分解\n学习目标 案例 方法 反思\n' + '教' * 30000 + '\n![关系图](../assets/shared.svg)\n图1-1 问题关系\n')
            self.write('assets/shared.svg', '<svg xmlns="http://www.w3.org/2000/svg"/>')
            self.spec['figures'] = [{'id':'图1-1', 'file':'assets/shared.svg', 'caption':'问题关系', 'source':'教学fixture', 'status':'ready'}]
            spec_name = f'runs/{run_id}.spec.json'
            self.save_spec(spec_name)
            self.success('start', '--id', run_id, '--spec', spec_name)
            # Repeated ordinary drafting requires no Harness calls.
            with (self.root / name).open('a') as stream:
                stream.write('\n连续修改一次\n再修改一次\n')
            self.check(run_id)
            self.evidence(run_id)
            evidence_name = f'runs/{run_id}.review.json'
            self.write(evidence_name, (self.root/'runs/review.json').read_text())
            self.success('review', '--id', run_id, '--evidence', evidence_name)
            with (self.root / '教材编写现状与目的.md').open('a') as stream:
                stream.write(f'\n[第{chapter}章](../{self.root.name}/{name}) chapter/final；已完成，配图ready，无待办。\n')
            self.success('accept', '--id', run_id)
        report = self.success('status')
        self.assertEqual(len(report['runs']), 10)
        self.assertTrue(all(r['effective_state'] == 'accepted' for r in report['runs']))

    def test_legacy_review_history_remains_unclassified(self):
        self.accepted()
        doc = json.loads((self.root/'harness.json').read_text())
        evidence = doc['runs'][0]['review']['evidence']
        del evidence['review_kind']
        del evidence['spec_sha256']
        self.write('harness.json', json.dumps(doc, ensure_ascii=False))
        self.assertTrue(self.success('validate')['valid'])
        report = self.success('status', '--id', 'fixture')['runs'][0]
        self.assertEqual(report['review_kind'], 'legacy_unspecified')
        self.failure('accept', '--id', 'fixture', code=1)

    def test_original_book_sources_remain_unchanged(self):
        expected = {'AI时代的计算思维--跨界创新与终身学习能力培养-教材大纲.docx': '4b2526dd13a07ea1facaeefcef09658b9df46ab4496df6c782c8dc222967d8be',
                    'AI时代的思维训练3.1节样稿.docx': '2fde276942f55dd4cfb00f0036a0d4a8935bd8320cef4c2eb0c47ed707e5aa17'}
        for name, value in expected.items():
            self.assertEqual(hashlib.sha256((PROJECT / name).read_bytes()).hexdigest(), value)

if __name__ == '__main__':
    unittest.main()

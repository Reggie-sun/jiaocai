"""Assemble owned chapter sources; report exact source and manuscript hashes."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MS = ROOT / 'manuscripts/ch03'
names = ['opening.md', 's3-1.md', 's3-2.md', 's3-3.md', 'closing.md']
names += ['answers-e%02d.md' % i for i in range(1, 7)]
names += ['references.md']
parts = [(MS / name).read_text(encoding='utf-8').rstrip() for name in names]
text = '\n\n'.join(parts) + '\n'
(MS / 'ch03.md').write_text(text, encoding='utf-8')
count_text = re.sub(r'```.*?```', '', text, flags=re.S)
count_text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', count_text)
count_text = re.sub(r'https?://\S+', '', count_text)
count = len(re.findall(r'[\u4e00-\u9fff]', count_text))
assert 28000 <= count <= 40000, count
assert re.findall(r'^## (3\.\d) ', text, re.M) == ['3.1', '3.2', '3.3']
assert len(re.findall(r'^# ', text, re.M)) == 1
assert len(re.findall(r'^### E0[1-6].*参考解', text, re.M)) == 6
tables = [int(v) for v in re.findall(r'^\*\*表3-(\d+) ', text, re.M)]
assert tables == list(range(1, len(tables) + 1)), tables
body, refs = text.split('## 参考文献', 1)
first = list(dict.fromkeys(re.findall(r'\[(\d+)\]', body)))
assert first == [str(i) for i in range(1, 10)], first
assert re.findall(r'^\[(\d+)\]', refs, re.M) == first
report = {'manuscript': 'manuscripts/ch03/ch03.md', 'sha256': hashlib.sha256(text.encode()).hexdigest(),
          'hanzi_approx': count, 'count_method': 'CJK Hanzi; exclude fenced code and Markdown/standalone URL targets; includes answers/captions; not publisher or Word count',
          'tables': len(tables), 'references': len(first), 'exercises': 6,
          'sources': {name: hashlib.sha256((MS / name).read_bytes()).hexdigest() for name in names}}
(ROOT / 'materials/ch03/assembly.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: report[k] for k in ['hanzi_approx', 'tables', 'references', 'exercises', 'sha256']}, ensure_ascii=False))

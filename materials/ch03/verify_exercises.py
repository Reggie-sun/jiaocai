"""Recalculate Chapter 3 examples and exercises from the actual Markdown tables."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MS = ROOT / 'manuscripts/ch03'
checks = []


def read(name):
    return (MS / name).read_text(encoding='utf-8')


def table(text, title):
    after = text.split(title, 1)[1]
    lines = after.splitlines()
    rows = []
    started = False
    for line in lines:
        if line.startswith('|'):
            started = True
            cells = [v.strip() for v in line.strip('|').split('|')]
            if not all(re.fullmatch(r'[:\-\s]+', v) for v in cells):
                rows.append(cells)
        elif started:
            break
    assert len(rows) > 1, title
    return rows[1:]


def check(label, actual, expected):
    assert actual == expected, (label, actual, expected)
    checks.append({'id': label, 'actual': actual, 'expected': expected})


def matrix(rows, actual_col, predicted_col):
    return Counter((r[actual_col], r[predicted_col]) for r in rows)


def energy(rows):
    data = []
    for r in rows:
        lamps, watts, old, occupied, buffer = map(float, r[1:])
        kw = lamps * watts / 1000
        data.append({'room': r[0], 'kw': kw, 'minimum_hours': occupied + buffer,
                     'baseline': kw * old * 20,
                     'potential_saving': kw * (old - occupied - buffer) * 20})
    return data


s31, s32, s33 = [read('s3-' + str(i) + '.md') for i in range(1, 4)]
seats = table(s31, 'E01教学模拟的房间记录')
check('E01-free-seats', [int(r[1]) - int(r[2]) for r in seats], [6, 0, 3])
e02 = table(s31, 'E02教学模拟记录')
m = matrix(e02, 1, 2)
check('E02-four-outcomes', [m[k] for k in [('是', '是'), ('是', '否'), ('否', '是'), ('否', '否')]], [3, 1, 3, 3])
check('E02-total', len(e02), 10)
check('E02-alerts', sum(r[2] == '是' for r in e02), 6)
check('E02-agreement-percent', 100 * (m['是', '是'] + m['否', '否']) / len(e02), 60)
check('E02-true-negative-records', [r[0] for r in e02 if r[1:3] == ['否', '否']], ['07', '08', '10'])
assert '07、08、10' in read('answers-e02.md')
priority_text = read('answers-e02.md').split('排序：', 1)[1].split('等情况可优先查看', 1)[0]
priority_ids = re.findall(r'记录(\d{2})', priority_text)
alerts = {r[0] for r in e02 if r[2] == '是'}
check('E02-priority-examples-outside-alerts', sorted(set(priority_ids) - alerts), [])
check('E02-priority-examples-count', len(set(priority_ids)), 3)

worked = table(s31, '模拟核验记录与转介提醒')
m = matrix(worked, 1, 2)
check('worked-finance-four-outcomes', [m[k] for k in [('是', '是'), ('是', '否'), ('否', '是'), ('否', '否')]], [2, 1, 2, 3])
check('worked-finance-agreement-percent', 100 * (m['是', '是'] + m['否', '否']) / len(worked), 62.5)

images = table(s32, '医学影像质量标注的教学模拟清单')
check('image-records', len(images), 8)
check('image-subjects', len({r[1] for r in images}), 7)
check('image-labels', dict(Counter(r[4] for r in images)), {'有': 3, '无': 4, '待复核': 1})
check('image-sites', dict(Counter(r[2] for r in images)), {'A': 4, 'B': 4})
check('image-devices', dict(Counter(r[3] for r in images)), {'X': 4, 'Y': 4})

faces = table(s32, 'E03人脸核验教学模拟记录')
for group, expected in [('甲', [2, 1, 1, 2]), ('乙', [3, 0, 2, 1])]:
    m = matrix([r for r in faces if r[1] == group], 2, 3)
    check('E03-' + group, [m[k] for k in [('是', '是'), ('是', '否'), ('否', '是'), ('否', '否')]], expected)
check('E03-correct-total', sum(r[2] == r[3] for r in faces), 8)
check('E03-total-records', len(faces), 12)

e05 = energy(table(s33, 'E05照明范围与固定条件'))
check('E05-baseline-kWh', round(sum(v['baseline'] for v in e05), 6), 230.4)
check('E05-candidate-reduction-kWh', round(sum(v['kw'] * 3 * 20 for v in e05), 6), 86.4)
check('E05-candidate-violations', [v['room'] for v in e05 if 5 < v['minimum_hours']], ['A', 'B', 'C', 'D'])
check('E05-potential-savings-kWh', [round(v['potential_saving'], 6) for v in e05], [10.8, 10.8, 18, 18])
check('E05-potential-total-kWh', round(sum(v['potential_saving'] for v in e05), 6), 57.6)
check('E05-change-C-total-kWh', round(sum(v['potential_saving'] for v in e05) - e05[2]['kw'] * .5 * 20, 6), 54)
check('E05-change-C-percent', round(54 / 230.4 * 100, 6), 23.4375)

e06 = energy(table(read('closing.md'), 'E06三个空间的固定教学数据'))
check('E06-baseline-kWh', [round(v['baseline'], 6) for v in e06], [36, 64, 80])
check('E06-potential-kWh', [round(v['potential_saving'], 6) for v in e06], [9, 20, 0])
check('E06-potential-total-kWh', round(sum(v['potential_saving'] for v in e06), 6), 29)
check('E06-candidate-two-hour-violations', [r[0] for r in table(read('closing.md'), 'E06三个空间的固定教学数据') if float(r[3]) - 2 < float(r[4]) + float(r[5])], ['U', 'W'])
check('E06-installed-cost-yuan', 3 * (600 + 200), 2400)
check('E06-budget-max-installs', 1000 // (600 + 200), 1)
check('E06-change-V-total-kWh', round(29 - e06[1]['kw'] * 1 * 20, 6), 21)
check('E06-monthly-gross-yuan', round(29 * .6, 6), 17.4)
check('E06-change-V-monthly-gross-yuan', round(21 * .6, 6), 12.6)

# An independent arithmetic seam for the worked generation example.
check('worked-light-baseline-kWh', round(10 * .024 * 7 * 18, 6), 30.24)
check('worked-light-after-kWh', round(10 * .024 * 5 * 18, 6), 21.6)
check('worked-light-saving-kWh', round(10 * .024 * 2 * 18, 6), 8.64)

report = {'status': 'PASS', 'scope': 'Actual Markdown data/count/unit/boundary recalculation; not real deployment or open-question acceptance',
          'check_count': len(checks), 'checks': checks,
          'inputs': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(MS.glob('*.md')) if p.name != 'ch03.md'}}
(ROOT / 'materials/ch03/exercise-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': report['status'], 'checks': len(checks)}, ensure_ascii=False))

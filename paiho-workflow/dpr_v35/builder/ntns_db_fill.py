# FILE_VERSION = 2
# -*- coding: utf-8 -*-
"""ntns_db_fill.py — R-0916-30（Amber 林彥博 2026-09-16「T1-G2 是」·轉正·永久）
DB 庫存主檔之 NS/NT 欄 → NT/NS 字典之「**只補空·不覆蓋**」第二採認路徑。

設計契約（三道守則·任一不成立即 raise，不得自行放寬）：
  G1 只補空：字典已有之料號一律以字典為準，DB 不得覆蓋（保護 Amber 具名裁示）。
  G2 只取明確值：DB 同一料號出現 NT 與 NS 並存者一律跳過（不臆測）；空白值跳過。
  G3 既有排除續行：pending_blank、protected、R-0819-7 之 ^99Z 系列、len(料號)<5 一律不補。
  G4 家族通則優先（v2·R-0916-33）：字典 family_rules 內具名之前綴家族，DB 值一律不採，
     強制為該規則之 force 值（現行：39／86 黏扣帶 → NS）。規則由字典驅動，改規則不需改本檔。
輸出：新版 ntns_dict_vNNN.json ＋ 衝突清單（字典 vs DB 不一致者·逐輪列出供 Amber 複核·不自動處理）。
用法：python3 ntns_db_fill.py <ntns_dict_vNNN.json> <DB_*.xlsx> <新版號整數>
"""
import collections
import json
import re
import sys

import openpyxl

EXCLUDE_RE = re.compile(r'^99Z')
MIN_LEN = 5          # R-v496-1 附帶：len(料號) >= 5


def db_values(db_path):
    wb = openpyxl.load_workbook(db_path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    hdr = [str(h) for h in next(it)]
    im, ins = hdr.index('料號'), hdr.index('NS/NT')
    agg = collections.defaultdict(collections.Counter)
    for r in it:
        m = str(r[im] or '').strip().upper()
        if not m:
            continue
        agg[m][str(r[ins] or '').strip().upper()] += 1
    single, ambiguous = {}, []
    for m, c in agg.items():
        vals = {k for k in c if k in ('NT', 'NS')}
        if len(vals) == 1:
            single[m] = vals.pop()
        elif len(vals) > 1:
            ambiguous.append(m)          # G2：DB 自身並存 → 跳過
    return single, ambiguous, len(agg)


def main(dict_path, db_path, newver):
    d = json.load(open(dict_path, encoding='utf-8'))
    keys = d['keys']
    before = dict(keys)
    prot = d['protected']
    blocked = set(prot.get('pending_blank', [])) | {k for k in prot if k.isupper() and k not in ('pending_blank',)}
    single, ambiguous, n_total = db_values(db_path)

    # G4：字典驅動之家族通則（R-0916-33）
    fam = []
    for rid, fr in (d.get('family_rules') or {}).items():
        pres, force = tuple(fr.get('prefixes') or ()), fr.get('force')
        if pres and force:
            fam.append((rid, pres, force))

    def family_force(mat):
        for rid, pres, force in fam:
            if mat.startswith(pres):
                return rid, force
        return None, None

    conflicts, fam_over, added, skipped = [], [], {}, collections.Counter()
    for m, v in sorted(single.items()):
        if m in keys:
            if keys[m] != v:
                rid, force = family_force(m)
                if force and keys[m] == force:
                    # G4：由具名家族通則決定，非待複核之真衝突
                    fam_over.append((m, keys[m], v, rid))
                else:
                    conflicts.append((m, keys[m], v))   # G1：字典優先·只記錄
            skipped['已在字典(不覆蓋)'] += 1
            continue
        if m in blocked:
            skipped['protected/pending_blank'] += 1
            continue
        if EXCLUDE_RE.match(m):
            skipped['R-0819-7 ^99Z'] += 1
            continue
        if len(m) < MIN_LEN:
            skipped['len<%d' % MIN_LEN] += 1
            continue
        rid, force = family_force(m)
        if force and force != v:
            skipped['家族通則覆蓋DB(%s)' % rid] += 1
            added[m] = force          # G4：不採 DB 值，入家族通則值
            continue
        added[m] = v

    keys.update(added)

    # ── 守則自證（任一不成立即 raise）──
    assert all(before[k] == keys[k] for k in before), 'G1 違反：既有鍵遭覆蓋'
    assert not (set(added) & set(before)), 'G1 違反：補入鍵與既有鍵重疊'
    assert not [m for m in added if EXCLUDE_RE.match(m) or len(m) < MIN_LEN or m in blocked], 'G3 違反'
    assert not (set(added) & set(ambiguous)), 'G2 違反：補入 DB 自身並存之料號'
    for m, v in added.items():
        rid, force = family_force(m)
        assert not force or v == force, f'G4 違反：{m} 屬 {rid} 家族應為 {force}，實為 {v}'
    for m, v in keys.items():
        rid, force = family_force(m)
        assert not force or v == force, f'G4 違反（存量）：{m} 屬 {rid} 家族應為 {force}，實為 {v}'

    d['keys'] = keys
    d['version'] = 'v%d' % newver
    d['counts'] = dict(collections.Counter(keys.values()))
    d['note_v%d' % newver] = {
        'date': '2026-09-16', 'rule': 'R-0916-30（Amber「T1-G2 是」）',
        'path': 'DB 庫存主檔 NS/NT 欄·只補空不覆蓋',
        'source': db_path.split('/')[-1],
        'db_distinct_materials': n_total, 'db_single_valued': len(single),
        'db_ambiguous_skipped': len(ambiguous),
        'added': len(added), 'NT': sum(1 for v in added.values() if v == 'NT'),
        'NS': sum(1 for v in added.values() if v == 'NS'),
        'keys_total': '%d → %d' % (len(before), len(keys)),
        'skipped': dict(skipped),
        'conflicts_kept_dict': [{'料號': m, '字典': a, 'DB': b} for m, a, b in conflicts],
        'family_rule_overrides': [{'料號': m, '字典': a, 'DB': b, 'rule': r} for m, a, b, r in fam_over],
        'guards': ('G1 只補空不覆蓋（保護具名裁示）／G2 DB 自身並存者跳過／'
                   'G3 pending_blank・protected・^99Z・len<5 不補／G4 家族通則優先（字典 family_rules 驅動）'),
        'family_rules_applied': [r[0] for r in fam],
        'R-v496-1': '逐鍵登錄·未作任何前綴推導',
    }
    out = dict_path.rsplit('_v', 1)[0] + '_v%d.json' % newver
    json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('✅ %s → %s：%d → %d 鍵（+%d·NT %d／NS %d）'
          % (dict_path.split('/')[-1], out.split('/')[-1], len(before), len(keys), len(added),
             sum(1 for v in added.values() if v == 'NT'), sum(1 for v in added.values() if v == 'NS')))
    print('   跳過：%s' % dict(skipped))
    if fam_over:
        print('   ℹ️ 家族通則覆蓋 DB %d 筆（R-0916-33 等·非待複核）' % len(fam_over))
    print('   ⚠️ 真衝突 %d 筆（字典優先·未變更·待 Amber 複核）：' % len(conflicts))
    for m, a, b in conflicts:
        print('      %-12s 字典=%s  DB=%s' % (m, a, b))
    return added, conflicts


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))

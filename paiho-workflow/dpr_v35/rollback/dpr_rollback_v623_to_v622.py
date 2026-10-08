# -*- coding: utf-8 -*-
"""dpr_rollback_v623_to_v622.py — 由 dpr_suite.py v623 逐位元組重建 v622（R-1002-25 備份）
用法：python3 dpr_rollback_v623_to_v622.py <v623 dpr_suite.py> <輸出 v622 路徑>
原理：v623 只比 v622 多 overrides v1.9→v1.10（suppress_7w 增 131641、203280）＋SUITE_VERSION＋docstring 4 行；
      反向移除兩鍵、版號改回、重打包，輸出 SHA256 必須＝41138cd0…，否則中止。再往前回 v621：dpr_rollback_v622_to_v621.py。
"""
import collections, hashlib, importlib.util, json, os, shutil, sys, tempfile
V623_SHA = 'f18f464021d92e654082342395e6bb8ab70cc010c326842f8da882a804a4285f'
V622_SHA = '41138cd04c7f5b2a91ed5c93fcdc531e85ad4e655e99dd71d6f537e463b2aeb8'
DOC623 = ('"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v623·1002 7w 白名單 v1.10）\n'
 'v623（2026-10-02·**R-1001-23／R-1002-19**·Amber 林彥博「B4-ok」「B14-OK」；v622 上線後照硬序上·R-1002-25）：\n'
 '  · brand_code_overrides v1.9→**v1.10**（檔名 v1_10 同步·R-0917-20）：suppress_7w 增 T1 131641 MXP、203280 TAN DE（local 採購·無開發窗口·15→17）。\n'
 '  · _PACK 重打包；棒次、builder v595、快照 v574、字典 v95、NT/NS v512、判定式一行未動。SUITE_VERSION 622 → 623（R-v556-1）。\n')
DOC622 = '"""dpr_suite.py — DPR 迴歸/迴路單檔套件（v622·1001 完成判定改讀 AO）\n'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
def main(src, dst):
    assert sha(src) == V623_SHA, 'v623 雜湊不符：%s' % sha(src)
    work = tempfile.mkdtemp(prefix='rb622_'); suite = os.path.join(work, 'dpr_suite.py'); shutil.copy(src, suite)
    m = load(suite, 's623'); pk = os.path.join(work, 'pack'); m.restore(pk, force=True)
    p10 = os.path.join(pk, 'brand_code_overrides_v1_10.json')
    d = json.load(open(p10, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
    for c in ('131641', '203280'): d['suppress_7w'].pop(c)
    d['version'] = 'v1.9'; d['updated'] = '2026-09-30'
    open(os.path.join(pk, 'brand_code_overrides_v1_9.json'), 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
    os.remove(p10); m.pack(pk)
    t = open(suite, encoding='utf-8').read()
    assert t.count('SUITE_VERSION = 623') == 1 and t.count(DOC623) == 1
    t = t.replace('SUITE_VERSION = 623', 'SUITE_VERSION = 622').replace(DOC623, DOC622)
    open(dst, 'w', encoding='utf-8').write(t); shutil.rmtree(work)
    assert sha(dst) == V622_SHA, '重建 v622 雜湊不符：%s' % sha(dst)
    print('v622 重建 OK  SHA256=%s  bytes=%d' % (sha(dst), os.path.getsize(dst)))
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

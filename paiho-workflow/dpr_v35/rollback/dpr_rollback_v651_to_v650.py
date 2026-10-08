# -*- coding: utf-8 -*-
"""dpr_rollback_v651_to_v650.py — R-1002-26 回滾程式（2026-10-07·R-1007-26）
用法：python3 dpr_rollback_v651_to_v650.py dpr_suite.py dpr_suite_v650.py
輸入 v651（SHA256 5a81f158…）→ 輸出 v650（SHA256 b72e63db…·逐位元組）。
做法：從 v651 _PACK 取出字典 v100，移除 R-1007-26 攝取項（orders GVPC26100090、rule_R_1007_26），
版本／更新日／筆數改回 v99，用 dict_v14_codec.encode 重編（須同目錄有 dict_v14_codec.py），
以 suite 自身的 _z 重壓放回 _PACK；docstring 首段與 SUITE_VERSION 照原文放回。"""
import sys,json,hashlib,importlib.util,os
SRC_SHA='5a81f15864727778e1f27c5fc93c664fdc4843d485ceb588315f43ef1e64dbdc'
DST_SHA='b72e63db65d43674e3e237d34b2ec8e247e11d8ccfcc2ba5249c977dbe98d6da'
SMALL=[[1, 5, "\"\"\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v650·1007 R-1007-21 tdt_link 選檔：Brooks-SL 鞋帶／鬆緊帶兩族各取最新）\n"], [229, 230, "SUITE_VERSION = 650   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）\n"]]
src,dst=sys.argv[1],sys.argv[2]
raw=open(src,'rb').read(); assert hashlib.sha256(raw).hexdigest()==SRC_SHA,'輸入不是 v651'
spec=importlib.util.spec_from_file_location('s651',src); S=importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
sys.path.insert(0,os.path.dirname(os.path.abspath(src)))
import dict_v14_codec as C
d=C.decode(json.loads(S._unz(S._PACK['回填原因處置字典_v100_columnar.json']).decode('utf-8')))
del d['orders']['GVPC26100090']; del d['rule_R_1007_26']
d['version']='v99'; d['updated']='2026-10-06'; d['count']=len(d['orders'])
js=json.dumps(C.encode(d),ensure_ascii=False,separators=(',',':')).encode('utf-8')
newline="    '回填原因處置字典_v99_columnar.json': '%s',\n"%S._z(js)
L=raw.decode('utf-8').splitlines(True)
i=[k for k,x in enumerate(L) if x.startswith("    '回填原因處置字典_v100_columnar.json'")]; assert len(i)==1
L[i[0]]=newline
for j1,j2,old in sorted(SMALL,key=lambda e:-e[0]): L[j1:j2]=[old]
out=''.join(L).encode('utf-8'); h=hashlib.sha256(out).hexdigest(); open(dst,'wb').write(out)
print(h,'✅ v650' if h==DST_SHA else '❌ 不符')

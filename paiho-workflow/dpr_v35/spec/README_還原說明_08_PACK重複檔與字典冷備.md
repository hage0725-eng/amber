# 08_PACK重複檔與字典冷備（R-0918-5 K1＋K2）還原說明

建立：2026-09-21（夜間覆盤 0920 續辦 → R-0918-5 落地）
來源：PROJECT `claude/` 下與 `dpr_suite.py::_PACK` 內容一致的六支重複檔（K2）＋ 回填字典 v85 冷備（K1）。
主本仍在 PROJECT `claude/dpr_suite.py`（SUITE_VERSION 609）之 `_PACK`；`python3 dpr_suite.py restore --dir .` 可自癒還原全部 10 檔。本資料夾僅為 Drive 端冷備。

## 檔案清冊（Drive 端 fileSize 已逐一核對 = 本機位元組數）
| 檔名 | 型態 | bytes | 備註 |
|---|---|---|---|
| xlrd.py | 原檔 | 3,538 | K2 |
| ntns_db_fill.py | 原檔 | 6,899 | K2 |
| brand_code_overrides_v1_1.json（內容v1.5·0916） | 原檔 | 9,927 | K2；檔名 v1_1、內容 version v1.5 |
| ntns_dict_v505.json.xz | xz | 16,440 | K2；NS 684 / NT 1,826（2,510 鍵） |
| build_dpr.py.xz.part00/01/02 | xz 分段 | 22,500 / 22,500 / 2,328 = 47,328 | K2；FILE_VERSION 587 |
| SKILL_v3_5_完整規格_權威自足版_v572.md.xz.part00–03 | xz 分段 | 15,000×3 + 10,460 = 55,460 | K2；DPR v572 |
| 回填原因處置字典_v85_columnar.json.xz.part00–06 | xz 分段 | 15,000×6 + 12,500 = 102,500 | K1；解壓後為 columnar JSON（PROJECT 原為 .gz.b64 文字） |

## 還原步驟（Linux/macOS）
```
cat build_dpr.py.xz.part0* > build_dpr.py.xz && xz -dk build_dpr.py.xz
cat SKILL_v3_5_完整規格_權威自足版_v572.md.xz.part0* > SKILL_v3_5_完整規格_權威自足版_v572.md.xz && xz -dk SKILL_v3_5_完整規格_權威自足版_v572.md.xz
cat 回填原因處置字典_v85_columnar.json.xz.part0* > 回填原因處置字典_v85_columnar.json.xz && xz -dk 回填原因處置字典_v85_columnar.json.xz
xz -dk ntns_dict_v505.json.xz
```
xz 內建 CRC64，若拼接或傳輸有誤會在 `xz -d` 時直接報錯（不會產生半壞檔）。

## 完整性校驗（SHA-256 前 16 碼）
- build_dpr.py.xz  fc878a00e799c339
- SKILL_v3_5_…_v572.md.xz  85c1e9d9798656c5
- ntns_dict_v505.json.xz  f896cfe3394ec389
- 回填原因處置字典_v85_columnar.json.xz  dba3c8724416a487
- 解壓後原檔 SHA-256 以 PROJECT `dpr_hash_registry.json`（0918 戳）為準。

## 注意
- 上傳經模型逐字轉錄 base64，Drive 端僅能以 fileSize 核對；若 `xz -d` 報 CRC 錯，請改用 `dpr_suite.py restore` 自 `_PACK` 還原（主本）。
- 對應 PROJECT 已移除路徑：claude/xlrd.py、claude/ntns_db_fill.py、claude/brand_code_overrides_v1_1.json、claude/ntns_dict_v505.json、claude/build_dpr.py、claude/SKILL_v3_5_完整規格_權威自足版_v572.md、claude/回填原因處置字典_v85_columnar.json.gz.b64。

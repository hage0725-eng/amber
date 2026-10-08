# paiho-workflow 安裝（Windows PowerShell）
# 用法：在本資料夾空白處按右鍵「在終端機開啟」，執行：
#   powershell -ExecutionPolicy Bypass -File install.ps1
# gate 沒有全綠就不會完成安裝，也不會建立任何提交。
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"; $env:PYTHONIOENCODING = "utf-8"

function Fail($msg) { Write-Host "==> $msg" -ForegroundColor Red; exit 1 }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail "缺少 Git：請先安裝 Git for Windows" }

# 找真正可用的 Python（避開 WindowsApps 商店假捷徑）
$pyExe = $null
foreach ($cand in @(@("py","-3"), @("python"), @("python3"))) {
  if (Get-Command $cand[0] -ErrorAction SilentlyContinue) {
    $args0 = @(); if ($cand.Count -gt 1) { $args0 = $cand[1..($cand.Count-1)] }
    try { $p = & $cand[0] @args0 -c "import sys; print(sys.executable)" 2>$null } catch { $p = $null }
    if ($LASTEXITCODE -eq 0 -and $p -and (Test-Path $p) -and ($p -notmatch "WindowsApps")) { $pyExe = $p.Trim(); break }
  }
}
if (-not $pyExe) { Fail "找不到可用的 Python 3：請從 python.org 安裝並勾選 Add to PATH" }
Write-Host "使用 Python：$pyExe"

Write-Host "1/5 安裝 Python 套件..."
& $pyExe -m pip install --user -q -r requirements.txt
if ($LASTEXITCODE -ne 0) { Fail "pip 安裝失敗（公司網路若擋 pypi，請洽 IT 或改用離線安裝）" }

Write-Host "2/5 把 Python 路徑寫入 hook 設定..."
$fwd = $pyExe -replace '\\','/'
Set-Content -Path .githooks/python_path -Value "`"$fwd`"" -NoNewline -Encoding ascii
$settings = Get-Content .claude/settings.json -Raw -Encoding UTF8
$settings = $settings -replace '"command": "python \\"', ('"command": "\"' + $fwd + '\" \"')
[System.IO.File]::WriteAllText("$PSScriptRoot/.claude/settings.json", $settings, (New-Object System.Text.UTF8Encoding $false))

Write-Host "3/5 建立版本控管..."
if (-not (Test-Path .git)) { git init -q; git checkout -q -b main 2>$null }
git config core.hooksPath .githooks
git config core.autocrlf false

Write-Host "4/5 跑回歸守門（驗證通過才安裝）..."
& $pyExe tools/gate.py
if ($LASTEXITCODE -ne 0) { Fail "gate 紅燈，安裝中止，未建立提交" }

Write-Host "5/5 首次提交..."
git add -A
git -c user.name="Amber Lin" -c user.email="hage0725@gmail.com" commit -q -m "paiho-workflow 初版：共用規則庫＋DPR 回歸守門"
if ($LASTEXITCODE -ne 0) { Fail "提交失敗（pre-commit 擋下或 git 設定問題），請截圖給 Claude" }
Write-Host "==> 安裝完成。在本資料夾執行 claude，輸入 /gate 試跑。" -ForegroundColor Green

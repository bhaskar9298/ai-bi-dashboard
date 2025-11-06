# ONE-CLICK FIX - PowerShell Version
# Run this in PowerShell: .\quick_fix.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   ONE-CLICK FIX SCRIPT" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Kill Python processes
Write-Host "Step 1: Stopping Python processes..." -ForegroundColor Green
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2
Write-Host "  Done!" -ForegroundColor White
Write-Host ""

# Step 2: Clean cache
Write-Host "Step 2: Cleaning Python cache..." -ForegroundColor Green
python one_click_fix.py
Write-Host ""

# Done
Write-Host "================================" -ForegroundColor Cyan
Write-Host "   FIX COMPLETE!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Start your server with:" -ForegroundColor Yellow
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""

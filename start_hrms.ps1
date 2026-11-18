# Frappe HRMS Sovereign Native Mode Launcher
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Launching Frappe HRMS Sovereign Mode   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Clear ports 8005 and 8080 if in use
Write-Host "[1/3] Ensuring ports 8005 and 8080 are free..." -ForegroundColor Yellow
$ports = @(8005, 8080)
foreach ($port in $ports) {
    Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | Unique | ForEach-Object {
        Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue
    }
}

# 2. Start Sovereign Backend on port 8005
Write-Host "[2/3] Starting Sovereign Backend (FastAPI + MariaDB)..." -ForegroundColor Yellow
Start-Process python -ArgumentList "c:\HRMS-1\run_backend.py" -WindowStyle Minimized

Start-Sleep -Seconds 2

# 3. Start Frontend Vite Server on port 8080
Write-Host "[3/3] Starting Frontend Server (Vite + Frappe Desk / PWA)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/c cd c:\HRMS-1\hrms\frontend && .\node_modules\.bin\vite.cmd --host 0.0.0.0 --port 8080" -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host "`n✔ All services are online!" -ForegroundColor Green
Write-Host "-----------------------------------------" -ForegroundColor DarkGray
Write-Host "Frappe Desk:      http://localhost:8080/desk" -ForegroundColor White
Write-Host "Department View:  http://localhost:8080/app/department" -ForegroundColor White
Write-Host "Designation View: http://localhost:8080/desk/setup/designation" -ForegroundColor White
Write-Host "Employee Portal:  http://localhost:8080/hrms/home" -ForegroundColor White
Write-Host "Backend API:      http://localhost:8005" -ForegroundColor White
Write-Host "Credentials:      Administrator / admin" -ForegroundColor Yellow
Write-Host "-----------------------------------------" -ForegroundColor DarkGray

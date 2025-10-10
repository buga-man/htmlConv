
Write-Host "Running Ruff..." -ForegroundColor Cyan
ruff check .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ruff check failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Running mypy..." -ForegroundColor Cyan
mypy html_conv/ --ignore-missing-imports

if ($LASTEXITCODE -ne 0) {
    Write-Host "mypy check failed!" -ForegroundColor Red
    exit 1
}

Write-Host "All checks passed!" -ForegroundColor Green

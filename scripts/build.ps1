
# Enable strict mode
$ErrorActionPreference = "Stop"

Write-Host "🔍 Запуск ruff (линт + автоформат)..." -ForegroundColor Cyan
uv run ruff format .
uv run ruff check --fix .

Write-Host "🧹 Очистка старых артефактов..." -ForegroundColor Cyan
# Удаление директорий
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
Get-ChildItem -Path . -Filter "*.egg-info" -Recurse | Remove-Item -Recurse -Force

# Удаление __pycache__
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force

# Удаление .pyc файлов
Get-ChildItem -Path . -Filter "*.pyc" -Recurse -File | Remove-Item -Force

Write-Host "📦 Сборка пакета..." -ForegroundColor Cyan
uv run python -m build

Write-Host "✅ Готово!" -ForegroundColor Green

#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Запуск ruff (линт + автоформат)..."
uv run ruff format .
uv run ruff check --fix .

echo "🧹 Очистка старых артефактов..."
rm -rf dist build *.egg-info
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "📦 Сборка пакета..."
uv run python -m build

echo "✅ Готово!"
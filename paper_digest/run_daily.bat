@echo off
setlocal
cd /d %~dp0
python -m paper_digest --config config.example.json

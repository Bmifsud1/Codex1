@echo off
setlocal

REM Starts a fresh local-rag Windows session:
REM 1) activates .venv
REM 2) ensures Ollama is reachable (starts `ollama serve` if needed)
REM 3) runs bootstrap + ingest + serve-web

set "ROOT_DIR=%~dp0.."
cd /d "%ROOT_DIR%"

set "CONFIG_FILE=%~1"
if "%CONFIG_FILE%"=="" set "CONFIG_FILE=config.windows.yaml"

if not exist ".venv\Scripts\activate.bat" (
  echo [ERROR] Could not find .venv\Scripts\activate.bat
  echo         Create the virtual environment first, then re-run this script.
  exit /b 1
)

call ".venv\Scripts\activate.bat"

where ollama >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Ollama is not on PATH.
  echo         Install Ollama for Windows and open a new terminal session.
  exit /b 1
)

curl.exe -s http://127.0.0.1:11434/api/tags >nul 2>&1
if errorlevel 1 (
  echo [INFO] Ollama API is not reachable on 127.0.0.1:11434.
  echo [INFO] Starting ollama serve in a separate window...
  start "Ollama Server" cmd /k "ollama serve"
  timeout /t 3 /nobreak >nul
)

echo [INFO] Using config: %CONFIG_FILE%
echo [INFO] Running bootstrap checks...
local-rag bootstrap --config "%CONFIG_FILE%"
if errorlevel 1 exit /b 1

echo [INFO] Running ingest...
local-rag ingest --config "%CONFIG_FILE%"
if errorlevel 1 exit /b 1

echo [INFO] Starting web UI server on http://127.0.0.1:3000
local-rag serve-web --config "%CONFIG_FILE%"

endlocal
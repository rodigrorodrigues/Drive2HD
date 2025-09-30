@echo off
echo ========================================
echo Drive2HD - Iniciando aplicacao
echo ========================================
echo.

echo Verificando se Python esta instalado...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, execute install.bat primeiro
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Verificando dependencias...
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo ERRO: Dependencias nao instaladas!
    echo Execute: install.bat
    pause
    exit /b 1
)

echo Dependencias OK!
echo.

echo Iniciando Drive2HD...
python main.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao executar a aplicacao!
    pause
) 
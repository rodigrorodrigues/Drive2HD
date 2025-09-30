@echo off
echo ========================================
echo Drive2HD - Setup Rclone
echo ========================================
echo.

echo Verificando se Rclone esta instalado...
rclone version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Rclone encontrado!
    rclone version
) else (
    echo ❌ Rclone nao encontrado!
    echo.
    echo Instalando Rclone...
    echo.
    echo Baixando Rclone...
    powershell -Command "Invoke-WebRequest -Uri 'https://downloads.rclone.org/rclone-current-windows-amd64.zip' -OutFile 'rclone.zip'"
    
    echo Extraindo...
    powershell -Command "Expand-Archive -Path 'rclone.zip' -DestinationPath '.' -Force"
    
    echo Movendo para PATH...
    for /d %%i in (rclone-*) do (
        copy "%%i\rclone.exe" "%USERPROFILE%\AppData\Local\Microsoft\WinGet\Packages\"
        echo ✅ Rclone instalado em: %%i\rclone.exe
    )
    
    echo Limpando arquivos temporarios...
    del rclone.zip
    rmdir /s /q rclone-*
    
    echo.
    echo ✅ Rclone instalado com sucesso!
)

echo.
echo ========================================
echo CONFIGURACAO DO GOOGLE DRIVE
echo ========================================
echo.
echo Agora vamos configurar o acesso ao Google Drive...
echo.
echo 1. Execute: rclone config
echo 2. Escolha: n (new remote)
echo 3. Nome do remote: gdrive
echo 4. Escolha: drive (Google Drive)
echo 5. Escolha: n (não usar auto config)
echo 6. Client ID: deixe vazio (Enter)
echo 7. Client Secret: deixe vazio (Enter)
echo 8. Escolha: y (sim, usar auto config)
echo 9. Escolha: 1 (My Drive)
echo 10. Escolha: y (sim, confirma)
echo 11. Escolha: q (sair)
echo.
echo Apos configurar, execute: python main_rclone.py
echo.
pause 
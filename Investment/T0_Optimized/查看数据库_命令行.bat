@echo off
chcp 65001 >nul
echo ========================================
echo SQLite 数据库命令行查看工具
echo ========================================
echo.
echo 正在打开数据库...
echo.

REM 检查 sqlite3 是否安装
where sqlite3 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未找到 sqlite3 命令
    echo.
    echo 请安装 SQLite:
    echo   1. 访问 https://www.sqlite.org/download.html
    echo   2. 下载 sqlite-tools-win32-x86.zip
    echo   3. 解压并添加到 PATH
    echo.
    pause
    exit /b
)

REM 打开数据库
sqlite3 db\t0_trading.db

pause

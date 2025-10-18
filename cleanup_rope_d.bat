@echo off

REM Rope D盘清理脚本
REM 当系统不允许直接删除时，您可以在稍后手动运行此脚本

ECHO 此脚本将删除D盘上的Rope安装
ECHO 请确保没有任何程序正在使用D:\Application\Rope目录
ECHO.
PAUSE

ECHO 正在终止可能占用Rope目录的Python进程...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
taskkill /F /IM cmd.exe >nul 2>&1

ECHO 等待2秒...
timeout /t 2 >nul

ECHO 尝试删除Rope目录...
rmdir /s /q "D:\Application\Rope"

IF %ERRORLEVEL% EQU 0 (
    ECHO Rope目录删除成功！
) ELSE (
    ECHO 警告：无法删除Rope目录。请尝试：
    ECHO 1. 重启电脑后再次运行此脚本
    ECHO 2. 或手动删除D:\Application\Rope目录
)

ECHO 尝试删除Conda环境...
D:\Application\Miniconda3\Scripts\conda env remove -n Rope -y

ECHO 清理完成！
PAUSE
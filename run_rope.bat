@echo off

REM Rope AI换脸软件启动脚本
REM 此脚本将激活正确的conda环境并启动Rope应用程序

echo 正在启动Rope AI换脸软件...
echo 请确保您已经下载了模型文件到 D:\Application\Rope\models 目录

echo 激活Conda环境...
call D:\Application\Miniconda3\Scripts\activate Rope

if %errorlevel% neq 0 (
    echo 错误: 无法激活Conda环境。请确保Miniconda安装正确。
    pause
    exit /b 1
)

echo 切换到Rope目录...
cd D:\Application\Rope

if %errorlevel% neq 0 (
    echo 错误: 无法切换到Rope目录。请检查目录是否存在。
    pause
    exit /b 1
)

echo 启动Rope应用程序...
python Rope.py

if %errorlevel% neq 0 (
    echo 错误: Rope应用程序启动失败。
    echo 请检查是否已安装所有依赖项和模型文件。
    pause
    exit /b 1
)

pause
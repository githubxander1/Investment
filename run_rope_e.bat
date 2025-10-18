@echo off

REM 启动E盘已安装的Rope AI换脸软件
REM 路径：E:\AiStartFile\Products\Rope

echo 正在启动Rope AI换脸软件...
echo 使用路径：E:\AiStartFile\Products\Rope

echo 切换到Rope目录...
cd "E:\AiStartFile\Products\Rope"

if %errorlevel% neq 0 (
    echo 错误: 无法切换到Rope目录。请检查路径是否正确。
    echo 路径: E:\AiStartFile\Products\Rope
    pause
    exit /b 1
)

echo 检查Rope.py文件是否存在...
if not exist "Rope.py" (
    echo 错误: 找不到Rope.py文件。请确认Rope软件安装正确。
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
# Rope AI换脸软件管理员权限使用指南

## 问题分析

从您提供的错误信息来看，主要有两个问题：

1. 无法找到虚拟环境路径：`call venv\Scripts\activate.bat` 显示「系统找不到指定的路径」
2. 依赖未正确安装：`ModuleNotFoundError: No module named 'torch'`

这是因为我们之前创建的是conda环境，而不是venv虚拟环境，并且环境可能没有被正确激活或依赖未安装完整。

## 解决方案

我已经为您创建了一个**自动请求管理员权限**的启动脚本：`run_rope_admin.bat`

### 使用方法

1. **双击运行脚本**：
   - 找到 `E:\git_documents\Investment1\run_rope_admin.bat`
   - 双击它，系统会自动弹出UAC管理员权限请求窗口

2. **授权管理员权限**：
   - 在弹出的窗口中点击「是」
   - 脚本将以管理员权限运行并执行以下操作：
     - 激活之前创建的conda环境
     - 自动检查并安装缺失的依赖项
     - 启动Rope应用程序

### 脚本工作原理

1. **自动权限检测**：脚本首先检查当前是否已获得管理员权限
2. **权限提升**：如果没有管理员权限，会自动请求提升权限
3. **环境激活**：使用正确的conda环境路径
4. **依赖修复**：自动安装torch等必要依赖
5. **应用启动**：启动Rope应用程序

## 额外排查步骤

如果仍然遇到问题，请按以下步骤检查：

1. **确认Miniconda安装**：
   - 检查路径 `D:\Application\Miniconda3` 是否存在
   - 如果不存在，请重新安装Miniconda

2. **确认conda环境**：
   - 打开命令提示符，执行：
     ```
     D:\Application\Miniconda3\Scripts\conda env list
     ```
   - 确认列表中包含名为「Rope」的环境

3. **手动安装依赖**：
   - 如果自动安装失败，可以手动执行：
     ```
     D:\Application\Miniconda3\Scripts\activate Rope
     pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html
     pip install -r D:\Application\Rope\requirements.txt
     ```

## 模型文件注意事项

请确保您已下载所有必要的模型文件，并将它们放入 `D:\Application\Rope\models` 目录中。缺少模型文件可能会导致应用程序启动后无法正常工作。

## 技术支持

如果按照以上步骤操作后仍然无法启动Rope软件，请提供详细的错误信息，我可以进一步协助您解决问题。
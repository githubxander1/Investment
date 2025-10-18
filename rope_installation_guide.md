# Rope AI换脸软件安装指南

## 安装状态

✅ **已完成的步骤**：
- [x] 创建安装目录 `D:\Application\Rope`
- [x] 从GitHub克隆Rope源代码
- [x] 创建必要的目录结构（videos, faces, output, models）
- [x] 使用Miniconda创建Python 3.10.13环境
- [x] 安装所有必要的Python依赖包
- [x] 创建启动脚本 `run_rope.bat`

❌ **需要您手动完成的步骤**：
- [ ] 下载模型文件

## 如何下载模型文件

Rope需要预训练模型才能正常工作。请按照以下步骤下载模型文件：

1. 打开您的浏览器
2. 访问模型下载网站（根据原教程，您需要访问特定网站下载模型）
3. 下载所有必需的模型文件
4. 将下载的模型文件解压后放入 `D:\Application\Rope\models` 目录

**注意**：模型文件通常较大，请确保您有足够的磁盘空间和稳定的网络连接。

## 如何使用Rope

1. **准备资源文件**：
   - 将您想要换脸的视频放入 `D:\Application\Rope\videos` 目录
   - 将您想要替换的人脸图片放入 `D:\Application\Rope\faces` 目录

2. **启动应用程序**：
   - 双击运行 `E:\git_documents\Investment1\run_rope.bat`
   - 脚本会自动激活conda环境并启动Rope应用程序

3. **使用界面**：
   - 在应用程序界面中，设置三个路径分别对应videos、faces和output文件夹
   - 选择要处理的视频
   - 选择要替换的人脸图片
   - 调整参数并开始处理
   - 处理完成后的结果将保存在output文件夹中

## 系统要求

- **操作系统**：Windows 10/11
- **GPU**：推荐NVIDIA GPU以获得更好的性能（已安装CUDA支持的依赖）
- **内存**：至少8GB RAM
- **磁盘空间**：至少10GB可用空间（包括模型文件）

## 故障排除

### 常见问题

1. **无法启动应用程序**：
   - 检查Miniconda是否正确安装
   - 确认Rope环境是否存在：`D:\Application\Miniconda3\envs\Rope`

2. **缺少模型错误**：
   - 确保已下载所有模型文件并放入正确目录

3. **CUDA错误**：
   - 如果您的GPU不支持CUDA或没有安装CUDA驱动，程序可能会自动回退到CPU模式，但处理速度会较慢

## 卸载方法

如果您想卸载Rope：

1. 删除 `D:\Application\Rope` 目录
2. 删除conda环境：
   ```
   D:\Application\Miniconda3\Scripts\conda remove -n Rope --all -y
   ```

## 注意事项

- 请合法使用AI换脸技术，尊重他人隐私和版权
- 不要将生成的内容用于非法或不道德的目的
- 模型文件可能需要定期更新以获得最佳效果
# Rope软件安装与清理说明

## 情况说明

根据您的要求，我已发现E盘已经有一个预先安装好的Rope软件（路径：`E:\AiStartFile\Products\Rope`）。由于系统限制，我们无法直接删除D盘上的Rope安装（可能有其他程序正在使用该目录）。

## 已完成的操作

1. **创建清理脚本**：
   - 文件：`E:\git_documents\Investment1\cleanup_rope_d.bat`
   - 功能：用于稍后手动删除D盘上的Rope安装

2. **创建E盘Rope启动脚本**：
   - 文件：`E:\git_documents\Investment1\run_rope_e.bat`
   - 功能：直接启动E盘已安装的Rope软件

## 使用方法

### 启动Rope软件

1. 直接双击运行 `run_rope_e.bat` 脚本
2. 脚本会自动导航到E盘的Rope安装目录并启动程序

### 清理D盘安装（可选）

如果您希望完全清理D盘上的Rope安装：

1. **关闭所有可能正在使用D盘Rope目录的程序**
2. 重启您的电脑
3. 电脑重启后，立即运行 `cleanup_rope_d.bat` 脚本
4. 脚本会尝试删除D盘Rope目录和相关的conda环境

## 注意事项

- 如果清理脚本仍然无法删除D盘目录，您可以手动删除 `D:\Application\Rope` 文件夹
- 确保在使用Rope软件前已下载所有必要的模型文件
- E盘的Rope安装可能已经配置好了所有环境和依赖，您可以直接使用

如有任何问题，请随时告知！
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
T0数据可视化工具 - 启动脚本
"""

import sys
import logging
import tkinter as tk
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from visualizer_ui import T0DataVisualizer


def main():
    """主函数"""
    logger.info("启动T0交易系统分时数据可视化工具")
    
    root = tk.Tk()
    app = T0DataVisualizer(root)

    # 添加窗口关闭事件处理
    def on_closing():
        logger.info("关闭应用程序")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()

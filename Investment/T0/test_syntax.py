#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单语法测试脚本，只检查ths_trade_wrapper.py的语法和结构
不导入实际的THS交易适配器
"""
import logging
import os
import sys
import ast
import inspect

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_syntax')

def check_syntax(file_path):
    """
    检查Python文件的语法是否正确
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 使用ast模块解析文件内容，检查语法
        ast.parse(content)
        logger.info(f"✅ 文件语法检查通过: {os.path.basename(file_path)}")
        return True
    except SyntaxError as e:
        logger.error(f"❌ 文件语法错误: {os.path.basename(file_path)} 第{e.lineno}行: {e.msg}")
        logger.error(f"错误行: {e.text}")
        return False
    except Exception as e:
        logger.error(f"❌ 检查文件语法时出错: {e}")
        return False

def check_indentation(file_path):
    """
    检查Python文件的缩进是否一致
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        indent_errors = []
        for i, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if stripped and not stripped.startswith('#'):
                # 计算缩进空格数
                indent = len(line) - len(stripped)
                # 检查缩进是否是4的倍数
                if indent % 4 != 0:
                    indent_errors.append((i, line, indent))
        
        if indent_errors:
            logger.warning(f"⚠️  发现{len(indent_errors)}处缩进不一致:")
            for line_num, line_content, indent in indent_errors[:5]:  # 只显示前5个
                logger.warning(f"  第{line_num}行: 缩进{indent}个空格: {line_content.rstrip()}")
            if len(indent_errors) > 5:
                logger.warning(f"  ... 还有{len(indent_errors) - 5}处错误")
            return False
        else:
            logger.info(f"✅ 文件缩进检查通过: {os.path.basename(file_path)}")
            return True
    except Exception as e:
        logger.error(f"❌ 检查文件缩进时出错: {e}")
        return False

def check_comments(file_path):
    """
    检查Python文件中的注释是否正确
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        comment_errors = []
        for i, line in enumerate(lines, 1):
            # 检查是否有非注释行中的中文未被正确注释
            if '初始化T0交易包装器' in line and not line.strip().startswith('#'):
                comment_errors.append((i, line))
        
        if comment_errors:
            logger.error(f"❌ 发现{len(comment_errors)}处注释问题:")
            for line_num, line_content in comment_errors:
                logger.error(f"  第{line_num}行: {line_content.rstrip()}")
            return False
        else:
            logger.info(f"✅ 文件注释检查通过: {os.path.basename(file_path)}")
            return True
    except Exception as e:
        logger.error(f"❌ 检查文件注释时出错: {e}")
        return False

def main():
    try:
        # 获取ths_trade_wrapper.py的路径
        wrapper_file = os.path.join(os.path.dirname(__file__), 'trading', 'ths_trade_wrapper.py')
        
        if not os.path.exists(wrapper_file):
            logger.error(f"❌ 文件不存在: {wrapper_file}")
            return 1
        
        logger.info(f"开始检查文件: {wrapper_file}")
        
        # 执行各项检查
        syntax_ok = check_syntax(wrapper_file)
        indent_ok = check_indentation(wrapper_file)
        comment_ok = check_comments(wrapper_file)
        
        # 总结
        if syntax_ok and indent_ok and comment_ok:
            logger.info("✅ 所有检查通过！文件语法、缩进和注释都正确。")
            return 0
        else:
            logger.error("❌ 检查未通过，请查看详细错误信息。")
            return 1
            
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
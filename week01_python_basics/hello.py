# -*- coding: utf-8 -*-
"""FDE S1 第 1 周 · Hello World：第一个 Python 脚本。

目标：
  1. 确认 Python 环境就绪（能被外部脚本解释运行）
  2. 跑通基础语法：print / 变量 / 字符串 / f-string
  3. 熟悉命令行参数：sys.argv
"""
import sys, platform
from datetime import datetime

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "陈驰"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"你好，{name}！")
    print(f"当前时间：{now}")
    print(f"Python 版本：{platform.python_version()}")
    print(f"运行平台：{platform.system()} {platform.release()}")
    print()
    print("✅ FDE S1 第 1 周任务 0 已完成。下一步：30 道 Python 基础语法题。")

if __name__ == "__main__":
    main()

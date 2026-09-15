# -*- coding: utf-8 -*-
"""05_file_io.py | S1 第 1 周 · 第 5 天（2026-09-19 周六）

主题：读文件 / 写文件 / 读 CSV / 写 JSON / 路径处理

今天开始真正处理你的工作数据了。三个动作学会就够用一周：
  读 → 处理 → 写出新文件。

★ 一个必须先讲清的知识点：路径
  「相对路径」是相对「当前工作目录」，而不是相对脚本文件。
  所以脚本一换地方跑，就可能报 FileNotFoundError。
  稳妥做法：用 Path(__file__).parent 拿到脚本自己所在的目录，再拼路径。
  下面第 0 节就是这么写的，照抄这个模式即可。

预计耗时：90–120 分钟（周末时间多，建议边做边改）。
"""

import csv
import json
from pathlib import Path

# ============================================================
# 0. 先把路径搞对（照抄这个模式）
# ============================================================
BASE_DIR = Path(__file__).resolve().parent          # 本文件所在目录
DATA_FILE = BASE_DIR / "data" / "教育政策清单_示例.csv"
OUTPUT_DIR = BASE_DIR / "output"

print("=" * 50)
print("【0】路径")
print(f"脚本所在目录：{BASE_DIR}")
print(f"数据文件：{DATA_FILE}")
print(f"数据文件存在吗：{DATA_FILE.exists()}")
# 如果这里是 False，先检查 data 目录和文件是否在（正常应该在）。

OUTPUT_DIR.mkdir(exist_ok=True)     # 不存在就创建，已存在也不报错
print(f"输出目录：{OUTPUT_DIR}")


# ============================================================
# 1. 读纯文本文件
# ============================================================
# with open(...) as f: 这种写法会在代码块结束时自动关闭文件，别用 f = open() 那种老写法。

demo_txt = OUTPUT_DIR / "demo.txt"
demo_txt.write_text("第一行内容\n第二行内容\n", encoding="utf-8")

print("=" * 50)
print("【1】读文本")
with open(demo_txt, encoding="utf-8") as f:
    content = f.read()               # 一次性读全部
print(f"整段读：{content!r}")

with open(demo_txt, encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):    # 逐行读，大文件用这种
        print(f"  第 {i} 行：{line.strip()}")
# 提醒：read() 拿到的每行末尾都带换行符 \n，打印时一般 .strip() 掉。


# ============================================================
# 2. 读 CSV：用 DictReader，每行变成「字典」
# ============================================================
print("=" * 50)
print("【2】读 CSV")

rows = []
# encoding="utf-8-sig"：用 Excel 另存的 CSV 带 BOM 头，这个编码能自动处理掉。
with open(DATA_FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"读进来 {len(rows)} 条记录")
print(f"表头：{list(rows[0].keys())}")
print("前 2 条：")
for row in rows[:2]:
    print(f"  {row}")
# 注意：读进来的所有值都是字符串！"2018" 不是数字 2018，
# 要参与计算必须 int(row["发布年份"])。

print("转成数字后按年份排序：")
rows_by_year = sorted(rows, key=lambda r: int(r["发布年份"]))
for row in rows_by_year:
    print(f"  {row['发布年份']}  {row['政策名称']}")


# ============================================================
# 3. 写文本文件：生成一份 Markdown 摘要
# ============================================================
print("=" * 50)
print("【3】写文本")

report = OUTPUT_DIR / "政策清单摘要.md"
lines = ["# 教育政策清单摘要（自动生成）", ""]
for row in rows_by_year:
    lines.append(f"- {row['发布年份']} | {row['政策名称']} | {row['发文机关']}")
report.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"已写出：{report}")
print(f"文件大小：{report.stat().st_size} 字节")


# ============================================================
# 4. 写 JSON：给程序读的结构化格式
# ============================================================
print("=" * 50)
print("【4】写 JSON")

summary = {
    "生成时间": "自动生成",
    "记录总数": len(rows),
    "发文机关种类": sorted({r["发文机关"] for r in rows}),   # 集合推导式去重
    "最早年份": min(int(r["发布年份"]) for r in rows),
    "最晚年份": max(int(r["发布年份"]) for r in rows),
}

json_file = OUTPUT_DIR / "政策清单摘要.json"
# ensure_ascii=False：让中文正常显示而不是 \uXXXX
# indent=2：缩进美化，人能看懂
json_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"已写出：{json_file}")
print(json.dumps(summary, ensure_ascii=False, indent=2))

# 反过来：读回 JSON
with open(json_file, encoding="utf-8") as f:
    loaded = json.load(f)
print(f"\n读回来验证，记录总数 = {loaded['记录总数']}")

print()


# ============================================================
#  动手练习（先自己写）
# ============================================================
print("=" * 50)
print("练习开始，共 4 题")

# 【1】统计这份清单里每个「关键词」出现几次，打印成「关键词: 次数」。
#      提示：可以用一个空字典当计数器：counts[key] = counts.get(key, 0) + 1

# 你的代码 ↓


# 【2】只保留「发文机关」是「教育部」的记录，写到一个新文件 output/教育部发文.md，
#      每行一条：- 年份 名称

# 你的代码 ↓


# 【3】把 rows 里所有记录的「发布年份」汇总成一个整数列表，打印出来并求平均值
#      （保留 1 位小数）。

# 你的代码 ↓


# 【4】把 rows 按「关键词」分组，存成 JSON：{"教育信息化": [政策名1, 政策名2], ...}
#      写到 output/按关键词分组.json。

# 你的代码 ↓


print("练习结束")
print("=" * 50)


# ============================================================
#  参考答案（自己写完再看！）
# ============================================================
"""参考实现：

【1】
counts = {}
for row in rows:
    key = row["关键词"]
    counts[key] = counts.get(key, 0) + 1
for k, v in counts.items():
    print(f"{k}: {v}")


【2】
moe_rows = [r for r in rows if r["发文机关"] == "教育部"]
moe_file = OUTPUT_DIR / "教育部发文.md"
text = "\\n".join(f"- {r['发布年份']} {r['政策名称']}" for r in moe_rows)
moe_file.write_text(text + "\\n", encoding="utf-8")
print(moe_file, len(moe_rows), "条")


【3】
years = [int(r["发布年份"]) for r in rows]
print(years)
print(round(sum(years) / len(years), 1))


【4】
grouped = {}
for row in rows:
    grouped.setdefault(row["关键词"], []).append(row["政策名称"])
# setdefault：键不存在就先用空列表占位，比 if 判断少一层缩进
out = OUTPUT_DIR / "按关键词分组.json"
out.write_text(json.dumps(grouped, ensure_ascii=False, indent=2), encoding="utf-8")
print(out)
print(json.dumps(grouped, ensure_ascii=False, indent=2))


常见报错对照：
  FileNotFoundError      → 路径不对，先 print(路径) 看看指向哪里
  UnicodeDecodeError     → 编码不对，中文文件先试 utf-8，再试 utf-8-sig / gbk
  KeyError: '发布年份'    → 列名对不上，print(row) 看真实表头（可能多了空格）

复盘自检：
  □ 我知道 with open() 为什么要这么写吗？
  □ 我能说清 CSV 读进来的数字为什么是字符串吗？
  □ 我知道自己的脚本哪里该用相对路径、哪里该用 __file__ 拼路径吗？
"""

# -*- coding: utf-8 -*-
"""06_mini_project.py | S1 第 1 周 · 第 6 天（2026-09-20 周日）

小项目：教育政策清单统计分析 → 自动生成 Markdown 报告

这是本周的收口任务，用到的全是前 5 天学的东西：
  变量 / 字典 / 列表  →  循环 + 判断  →  函数封装  →  读 CSV / 写文件

目标不是写出多漂亮的代码，而是第一次完整体验「读数据 → 加工 → 产出文件」这条链路。
跑通之后，把输出目录里的报告用 Word 打开看一眼，你会对「脚本能替我干活」这件事有实感。

用法：直接运行本文件，然后去 week01_python_basics/output/ 看产出。
预计耗时：90–120 分钟（含下面的 3 个改造任务）。
"""

import csv
import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "教育政策清单_示例.csv"
OUTPUT_DIR = BASE_DIR / "output"

# 数据来源说明：本文件为练习用示例数据，条目信息未逐条核校，如需引用请以教育部官网原文为准。
DATA_NOTE = "本文数据为练习用示例数据，未逐条核校，引用请以教育部官网原文为准。"


# ============================================================
#  1. 读取：把 CSV 变成「列表套字典」
# ============================================================
def load_policies(path):
    """读取政策清单 CSV，返回记录列表。

    每一条记录形如：
        {'序号': '3', '政策名称': '教育信息化2.0行动计划',
         '发布年份': '2018', '发文机关': '教育部', '关键词': '教育信息化'}
    """
    if not path.exists():
        raise FileNotFoundError(f"找不到数据文件：{path}")

    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


# ============================================================
#  2. 清洗：CSV 读进来的年份是字符串，转成数字，坏的丢掉
# ============================================================
def to_year(text):
    """把 '2018' 转成 2018；脏数据返回 None。"""
    try:
        return int(str(text).strip())
    except (ValueError, TypeError):
        return None


def clean_policies(rows):
    """补上 year（整数）字段，并过滤掉年份不合法的记录。"""
    cleaned = []
    for row in rows:
        year = to_year(row.get("发布年份"))
        if year is None:
            print(f"  [跳过] 年份无法识别：{row.get('政策名称')} | {row.get('发布年份')!r}")
            continue
        row["year"] = year          # 新增一个字段，原字段不动
        cleaned.append(row)
    return cleaned


# ============================================================
#  3. 统计：几个常用维度
# ============================================================
def stats_by_field(rows, field):
    """按某个字段计数，返回 {字段值: 条数}，按条数从多到少排序。"""
    counter = Counter(row[field] for row in rows)
    return dict(counter.most_common())


def group_names_by_keyword(rows):
    """按关键词分组，返回 {关键词: [政策名称, ...]}。"""
    grouped = {}
    for row in rows:
        grouped.setdefault(row["关键词"], []).append(row["政策名称"])
    return grouped


def pick(rows, **conditions):
    """按条件筛选记录。用法：pick(rows, 发文机关='教育部')"""
    result = []
    for row in rows:
        if all(row.get(k) == v for k, v in conditions.items()):
            result.append(row)
    return result


# ============================================================
#  4. 产出：拼一份 Markdown 报告
# ============================================================
def build_report(rows, by_keyword, by_agency, by_year):
    """把统计结果拼成 Markdown 文本。"""
    lines = []
    lines.append("# 教育政策清单分析报告")
    lines.append("")
    lines.append(f"> {DATA_NOTE}")
    lines.append("")
    lines.append(f"- 记录总数：**{len(rows)}** 条")
    lines.append(f"- 年份跨度：**{min(r['year'] for r in rows)} – {max(r['year'] for r in rows)}**")
    lines.append(f"- 发文机关数：**{len(by_agency)}** 个")
    lines.append("")

    lines.append("## 一、按关键词分布")
    lines.append("")
    lines.append("| 关键词 | 政策数量 |")
    lines.append("|--------|---------|")
    for key, count in by_keyword.items():
        lines.append(f"| {key} | {count} |")
    lines.append("")

    lines.append("## 二、按发文年份分布")
    lines.append("")
    lines.append("| 年份 | 政策数量 | 政策名称 |")
    lines.append("|------|---------|---------|")
    for year in sorted(by_year):
        names = "；".join(r["政策名称"] for r in rows if r["year"] == year)
        lines.append(f"| {year} | {by_year[year]} | {names} |")
    lines.append("")

    lines.append("## 三、按发文机关分布")
    lines.append("")
    lines.append("| 发文机关 | 政策数量 |")
    lines.append("|---------|---------|")
    for agency, count in by_agency.items():
        lines.append(f"| {agency} | {count} |")
    lines.append("")

    lines.append("## 四、政策清单明细")
    lines.append("")
    lines.append("| 序号 | 政策名称 | 发布年份 | 发文机关 | 关键词 |")
    lines.append("|------|---------|---------|---------|--------|")
    for row in sorted(rows, key=lambda r: r["year"]):
        lines.append(
            f"| {row['序号']} | {row['政策名称']} | {row['year']} "
            f"| {row['发文机关']} | {row['关键词']} |"
        )
    lines.append("")
    return "\n".join(lines)


# ============================================================
#  5. 主流程
# ============================================================
def main():
    print("=" * 50)
    print("教育政策清单分析")
    print("=" * 50)

    # 读
    rows = load_policies(DATA_FILE)
    print(f"读取成功：{len(rows)} 条记录")

    # 清洗
    rows = clean_policies(rows)
    print(f"清洗后：{len(rows)} 条记录")

    # 统计
    by_keyword = stats_by_field(rows, "关键词")
    by_agency = stats_by_field(rows, "发文机关")
    by_year = stats_by_field(rows, "year")

    # 产出
    OUTPUT_DIR.mkdir(exist_ok=True)

    report_text = build_report(rows, by_keyword, by_agency, by_year)
    report_file = OUTPUT_DIR / "政策清单分析报告.md"
    report_file.write_text(report_text, encoding="utf-8")

    json_file = OUTPUT_DIR / "政策清单分析结果.json"
    json_file.write_text(
        json.dumps(
            {
                "记录总数": len(rows),
                "按关键词": by_keyword,
                "按发文机关": by_agency,
                "按年份": by_year,
                "按关键词分组": group_names_by_keyword(rows),
                "教育部发文": [r["政策名称"] for r in pick(rows, 发文机关="教育部")],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # 终端摘要
    print("-" * 50)
    print("按关键词：")
    for key, count in by_keyword.items():
        print(f"  {key:<10} {count}")
    print("按年份：")
    for year, count in sorted(by_year.items()):
        print(f"  {year}  {count}")
    print("-" * 50)
    print(f"报告已生成：{report_file}")
    print(f"结构化结果：{json_file}")
    print("打开报告看一眼，再回来做下面的改造任务。")


if __name__ == "__main__":
    main()


# ============================================================
#  改造任务（做完才算完成今天的量）
# ============================================================
"""
【任务 1 · 换数据】
  用你自己的真实数据替换掉 data/教育政策清单_示例.csv。
  来源建议：从你手头的 Excel 里另存为 CSV，列名保持
  「序号, 政策名称, 发布年份, 发文机关, 关键词」即可直接跑。
  列名不一样时，改 build_report 里用到的字段名就行（报 KeyError 时按它提示的那个字段改）。

【任务 2 · 加一列统计】
  在报告里加一节「按 5 年一个阶段统计」：
    - 2011–2015 / 2016–2020 / 2021–2025 三档，各有多少条
  提示：写一个 stage_of(year) 函数，用 if / elif 判断年份落在哪一档，
       再用 stats_by_field 类似的方式计数。

【任务 3 · 输出成 Word 能直接看的文件】
  报告现在是 .md。最快做法：用 VS Code 打开 .md 文件，
  点右上角「打开预览」，全选复制，粘到 Word 里，套上你的常规排版
  （宋体小四 / 1.5 倍行距 / 黑体标题），就是一份能发出去的文档。

完成后：
  1. 在 VS Code 源代码管理里 commit：feat: W1D6 政策清单分析小项目
  2. 同步到 GitHub
  3. 去 README.md 的打卡表里给 D6 打勾

卡住的时候先看报错的最后一行——它会直接告诉你哪个文件哪一行、什么类型的错。
"""

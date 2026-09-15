# -*- coding: utf-8 -*-
"""07_self_check.py | S1 第 1 周 · 第 7 天（2026-09-21 周一晚）

主题：自测 + 复盘

这是一个「会自己判分」的脚本。
下面有 8 道题，每题给了一个函数骨架，你的任务是把 TODO 那几行填上。
填完直接运行，脚本会逐题检查并给出得分。

规则：不要改「检查区」的代码，只改 TODO 部分。
看不懂某题的检查逻辑是正常的——那就是你下周要学的东西。

预计耗时：45–60 分钟。
"""

# ============================================================
#  待完成的 8 个函数（只改 TODO 下面那几行）
# ============================================================

def q1_greet(name):
    """返回字符串「你好，{name}！」（用全角感叹号）"""
    # TODO ↓
    pass


def q2_to_wan(amount):
    """把「元」换成「万元」，保留 1 位小数。
    例：35000 → 3.5     1000000 → 100.0"""
    # TODO ↓
    pass


def q3_count_by_status(rows, status):
    """返回 rows 里「状态」等于 status 的记录条数（整数）"""
    # TODO ↓
    pass


def q4_pick_ids(rows, priority):
    """返回 rows 里「优先级」等于 priority 的所有「编号」，组成列表"""
    # TODO ↓
    pass


def q5_unique_tags(tags):
    """去掉重复项，返回排序后的列表。
    例：["b", "a", "b"] → ["a", "b"]"""
    # TODO ↓
    pass


def q6_safe_int(text, default=0):
    """把 text 转成整数；转不了就返回 default（不许让程序报错）"""
    # TODO ↓
    pass


def q7_year_stage(year):
    """按年份返回阶段名：
    year < 2016        → "早期"
    2016 <= year <= 2020 → "中期"
    year > 2020        → "近期"
    注意：返回值必须是这三个字符串之一，不要带空格。"""
    # TODO ↓
    pass


def q8_make_row(pid, name, status="进行中"):
    """返回字典：{"编号": pid, "事项": name, "状态": status}"""
    # TODO ↓
    pass


# ============================================================
#  检查区（不用改，也先不用看懂）
# ============================================================

SAMPLE_ROWS = [
    {"编号": "A003", "事项": "小奔体育商机", "状态": "进行中", "优先级": "P1"},
    {"编号": "A005", "事项": "租房合同归档", "状态": "已闭环", "优先级": "P2"},
    {"编号": "A011", "事项": "北湖第 2 批报账", "状态": "进行中", "优先级": "P0"},
    {"编号": "A012", "事项": "数智安防试点", "状态": "待确认", "优先级": "P0"},
]


def _check(label, fn, expected, *args, **kwargs):
    """跑一个题，比对结果。返回 True / False。"""
    try:
        actual = fn(*args, **kwargs)
    except NotImplementedError:
        print(f"[未完成] {label}：还没写")
        return False
    except Exception as e:
        print(f"[报错]   {label}：{type(e).__name__}: {e}")
        return False

    if actual is None and expected is not None:
        print(f"[未完成] {label}：函数还返回 None，说明 TODO 没填")
        return False

    if actual == expected:
        print(f"[通过]   {label}  结果：{actual!r}")
        return True
    print(f"[未通过] {label}")
    print(f"         期望：{expected!r}")
    print(f"         实际：{actual!r}")
    return False


def run_all():
    print("=" * 56)
    print("W1 自测 · 共 8 题")
    print("=" * 56)

    results = [
        _check("Q1 问候语", q1_greet, "你好，世界！", "世界"),
        _check("Q2 换算万元", q2_to_wan, 3.5, 35000),
        _check("Q2 换算万元（大额）", q2_to_wan, 100.0, 1000000),
        _check("Q3 统计进行中", q3_count_by_status, 2, SAMPLE_ROWS, "进行中"),
        _check("Q3 统计待确认", q3_count_by_status, 1, SAMPLE_ROWS, "待确认"),
        _check("Q4 筛 P0 编号", q4_pick_ids, ["A011", "A012"], SAMPLE_ROWS, "P0"),
        _check("Q5 去重排序", q5_unique_tags, ["a", "b", "c"], ["b", "a", "b", "c"]),
        _check("Q6 安全转整数", q6_safe_int, 120, "120"),
        _check("Q6 脏数据兜底", q6_safe_int, 0, "abc"),
        _check("Q6 自定义兜底值", q6_safe_int, -1, "abc", -1),
        _check("Q7 年份分档（早期）", q7_year_stage, "早期", 2012),
        _check("Q7 年份分档（中期）", q7_year_stage, "中期", 2018),
        _check("Q7 年份分档（近期）", q7_year_stage, "近期", 2022),
        _check(
            "Q8 生成记录",
            q8_make_row,
            {"编号": "A005", "事项": "租房合同归档", "状态": "进行中"},
            "A005",
            "租房合同归档",
        ),
    ]

    passed = sum(1 for r in results if r)
    total = len(results)
    print("-" * 56)
    print(f"得分：{passed} / {total}")
    print("-" * 56)

    if passed == total:
        print("全部通过。W1 可以收工，下一周进 W2：更多基础语法 + 小工具练习。")
    elif passed >= total * 0.7:
        print("基本过关。把没通过的题对应的那天的文件重读一遍再改，然后重新运行本文件。")
    else:
        print("建议把 01–05 按顺序再跑一遍。不用急，这一周的任务不是全对，是「见过」。")
    print()
    print("不管得分多少，请做下面三件事：")
    print("  1. 把这周的代码 commit 并推到 GitHub")
    print("  2. 在 notes/ 下写一篇学习笔记（下面列了要写什么）")
    print("  3. 在 week01_python_basics/README.md 的打卡表里把 D7 打勾")
    return passed, total


# ============================================================
#  学习笔记模板（复制到 notes/W1.md 里填）
# ============================================================
NOTE_TEMPLATE = """
# W1 学习笔记（2026-09-15 ~ 2026-09-21）

## 1. 这周我实际花了多少时间
（每晚大概多少分钟，哪天没做、为什么）

## 2. 最卡我的 3 个点
（写具体报错信息或具体概念，不用写"都很难"）

## 3. 现在我能独立做出来的事
（例：能读一个 CSV，按条件筛出想要的记录，写出新文件）

## 4. 还没搞懂、留到下周的
（如实写，后面 W2/W3 会覆盖到）

## 5. 下周调整
（时间安排上要改什么？比如周三晚上固定有事，就挪到周四）
"""


if __name__ == "__main__":
    run_all()
    print()
    print("=" * 56)
    print("学习笔记模板（复制到 week01_python_basics/../notes/W1.md）")
    print("=" * 56)
    print(NOTE_TEMPLATE)

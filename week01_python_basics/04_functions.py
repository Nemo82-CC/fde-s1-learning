# -*- coding: utf-8 -*-
"""04_functions.py | S1 第 1 周 · 第 4 天（2026-09-18 周五晚）

主题：函数定义与调用 / 参数与返回值 / 模块导入 / 主程序入口

为什么函数重要：昨天写的逻辑如果复制粘贴三遍，改一处就会漏两处。
函数 = 把一段逻辑打包起个名字，写一次、到处调用。

预计耗时：45–60 分钟。
"""

# ============================================================
# 0. 先导入标准库（Python 自带，不用安装）
# ============================================================
import datetime          # 日期时间
from pathlib import Path  # 路径处理，比拼字符串靠谱

print("=" * 50)
print("【0】导入模块")
print(f"今天的日期：{datetime.date.today()}")


# ============================================================
# 1. 最简单的函数：有入参、有返回值
# ============================================================
def format_amount(amount):
    """把金额格式化成「XX.X 万元」的形式。"""
    return f"{amount / 10000:.1f} 万元"


print("=" * 50)
print("【1】函数基本结构")
print(format_amount(1000000))   # 100.0 万元
print(format_amount(35000))     # 3.5 万元
# 三个关键点：
#   1) def 开头、冒号结尾、函数体缩进
#   2) 参数写在括号里
#   3) return 把结果交回去；没有 return 就返回 None


# ============================================================
# 2. 默认参数：调用时不传就用默认值
# ============================================================
def make_item(pid, status="进行中", owner="陈驰"):
    """生成一条台账记录的字典。"""
    return {"编号": pid, "状态": status, "负责人": owner}


print("=" * 50)
print("【2】默认参数")
print(make_item("A003"))                            # 用两个默认值
print(make_item("A005", "已闭环"))                   # 只覆盖状态
print(make_item("A011", owner="刘珂含"))             # 按名字传参，更清楚
# 规范：所有带默认值的参数，必须排在没默认值的参数后面。


# ============================================================
# 3. 返回多个值
# ============================================================
def count_status(rows):
    """返回 (进行中条数, 已闭环条数)。"""
    doing = 0
    closed = 0
    for row in rows:
        if row["状态"] == "进行中":
            doing += 1
        elif row["状态"] == "已闭环":
            closed += 1
    return doing, closed


ledger = [
    {"编号": "A003", "状态": "进行中", "优先级": "P1"},
    {"编号": "A005", "状态": "已闭环", "优先级": "P2"},
    {"编号": "A011", "状态": "进行中", "优先级": "P0"},
    {"编号": "A012", "状态": "待确认", "优先级": "P1"},
]

print("=" * 50)
print("【3】返回多个值")
doing_count, closed_count = count_status(ledger)     # 一次接两个
print(f"进行中 {doing_count} 条，已闭环 {closed_count} 条")
# 本质是返回了一个元组，左边用两个变量接住，这叫「解包」。


# ============================================================
# 4. 判断 + 早返回：写逻辑更清爽的写法
# ============================================================
def priority_of(row):
    """按优先级返回处理建议。"""
    if row.get("状态") == "已闭环":
        return "无需处理"          # 不满足条件就早早 return，后面的逻辑不用再套 if
    if row["优先级"] == "P0":
        return "今天必须处理"
    return "本周内安排"


print("=" * 50)
print("【4】早返回")
for row in ledger:
    print(f"  {row['编号']} → {priority_of(row)}")


# ============================================================
# 5. 作用域：函数内部的变量，外面拿不到
# ============================================================
counter = 0          # 全局变量（模块级）


def bad_increase():
    """这段是错的示范：函数里改全局变量必须声明 global。"""
    global counter   # 真实项目里尽量避免这样写
    counter += 1


print("=" * 50)
print("【5】作用域")
bad_increase()
print(f"全局 counter 现在是：{counter}")
# 你在这份文件里看到的 `ledger` 能进函数，是因为它是只读使用的。
# 规则：函数里的变量出不了函数；要用外面的变量就当作参数传进去，别用 global。


# ============================================================
# 6. 主程序入口：if __name__ == "__main__"
# ============================================================
def main():
    """脚本的主流程都写在这里。"""
    print("=" * 50)
    print("【6】主程序入口")
    print(f"  台账共 {len(ledger)} 条，今天 {datetime.date.today()}")
    print(f"  数据文件目录是否存在于本机：{Path('data').exists()}")


if __name__ == "__main__":
    main()

# 为什么要这两行？（起作用的就是 if 判断那行 + main() 调用那行，别去凑"四行"）
#   别人 import 你的文件时，不应该顺手跑一遍主流程。
#   __name__ == "__main__" 表示「这个文件是被直接运行的」，此时才跑 main()。


print()


# ============================================================
#  动手练习（先自己写）
# ============================================================
print("=" * 50)
print("练习开始，共 4 题")

# 【1】写一个函数 greet(name)，返回字符串「你好，{name}！」。用两个不同的名字各调用一次。

# 你的代码 ↓
def greet(name):
    return(f"你好，{name}！")

print(greet("陈驰"))
print(greet("hcky"))


# 【2】写一个函数 is_overdue(days)，参数 days 是已逾期天数：
#      days > 0 返回 True，否则返回 False。用 3 和 0 各测一次。

# 你的代码 ↓
def is_overdue(days):
    if days > 0:
        return True
    else:
        return False

print(is_overdue(3))
print(is_overdue(0))



# 【3】写一个函数 pick_by_status(rows, status="进行中")，
#      返回所有符合该状态的「事项」列表（没有事项字段就返回编号）。
#      用 ledger 调用两次：一次默认，一次传 "已闭环"。

# 你的代码 ↓
def pick_by_status(rows, status="进行中"):
    result = []
    for row in rows:
        if row["状态"]== status:
            result.append(row.get("事项", row["编号"]))
    return result

print(pick_by_status(ledger))
print(pick_by_status(ledger, "已闭环"))


# 【4】把「练习 1 和练习 2 的函数」放进一个 main2() 里调用，
#      并用 if __name__ == "__main__": 的方式运行它。

# 你的代码 ↓
def main2():
    print(greet("陈驰"))
    print(is_overdue(3))
    print(is_overdue(0))

if __name__ == "__main__":
    main2()


print("练习结束")
print("=" * 50)


# ============================================================
#  参考答案（自己写完再看！）
# ============================================================
"""参考实现：

【1】
def greet(name):
    return f"你好，{name}！"

print(greet("陈驰"))
print(greet("刘珂含"))


【2】
def is_overdue(days):
    return days > 0

print(is_overdue(3))    # True
print(is_overdue(0))    # False
# 说明：days > 0 本身就是一个布尔值，所以可以直接 return，不必写 if。


【3】
def pick_by_status(rows, status="进行中"):
    result = []
    for row in rows:
        if row["状态"] == status:
            result.append(row.get("事项", row["编号"]))
    return result

print(pick_by_status(ledger))              # ['A003', 'A011']
print(pick_by_status(ledger, "已闭环"))     # ['A005']


【4】
def main2():
    print(greet("陈驰"))
    print(is_overdue(3))

if __name__ == "__main__":
    main2()
# 注意：这份文件里已经有一个 if __name__ == "__main__" 了，
# 你写了第二个的话，两个都会跑（顺序按出现先后）。这是正常的，不用删原来的。


复盘自检：
  □ 我知道有没有 return 的区别吗？（没有就返回 None）
  □ 我知道带默认值的参数要放在哪个位置吗？
  □ 我能说清「参数」和「返回值」在函数两端各起什么作用吗？
  □ 为什么真实项目里要避免用 global？
"""

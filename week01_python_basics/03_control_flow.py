# -*- coding: utf-8 -*-
"""03_control_flow.py | S1 第 1 周 · 第 3 天（原定 09-17 周四，09-17 加班顺延，实际 09-19 周六）

主题：if 判断 / for 循环 / while 循环 / break & continue / 异常处理

学会这一节，你就能写「有逻辑」的脚本了——之前都只是在打印。

★ 关键认知：Python 靠「缩进」判断代码属于哪一层。
  一行末尾有冒号 : → 下一行必须缩进（4 个空格）。
  缩进错了程序就报 IndentationError，这是最常见的报错，看到别慌，检查空格。

预计耗时：45–60 分钟。
"""

print("=" * 50)
print("【1】if / elif / else：按条件走不同分支")

priority = "P0"

if priority == "P0":
    action = "今天必须处理，先发提醒"
elif priority == "P1":
    action = "本周内安排"
else:
    action = "进待办池，不设截止"

print(f"优先级 {priority} → {action}")

# 常见条件写法
amount = 1000000
print(f"金额是否 ≥ 100 万：{amount >= 1000000}")
print(f"是否在区间内：{500000 < amount <= 2000000}")   # 可以链式比较
print(f"状态是否属于进行类：{'进行中' in ['进行中', '待确认', '待反馈']}")


print("=" * 50)
print("【2】for 循环：把一堆东西挨个过一遍")

ledger = [
    {"编号": "A003", "事项": "小奔体育商机", "状态": "进行中", "优先级": "P1"},
    {"编号": "A005", "事项": "租房合同归档", "状态": "已闭环", "优先级": "P2"},
    {"编号": "A011", "事项": "北湖第 2 批报账", "状态": "进行中", "优先级": "P0"},
]

for row in ledger:
    print(f"  {row['编号']}  {row['事项']}  [{row['状态']}]")

# 只要编号，用序号配合，range() 生成数字序列
print("--- 带序号的写法 ---")
for i in range(len(ledger)):
    print(f"  {i + 1}. {ledger[i]['编号']}")

# 更 Python 的写法：enumerate 直接拿到序号和内容
print("--- enumerate 写法 ---")
for i, row in enumerate(ledger, start=1):        #“for i,row”表明的是「每一轮循环要拿到两个东西：序号 i 和内容 row」；“start=1”表示序号从 1 开始（默认是 0）。
    print(f" {i}. {row['编号']}")

# 只遍历字典的键
print("--- 遍历字典 ---")
for k, v in ledger[0].items():
    print(f"  {k} = {v}")


print("=" * 50)
print("【3】for + if：筛选（最常用的组合）")

doing = []         ##就是「先建一个空列表」,[]表示空列表;doing 这个名字必须在循环之前就建好
for row in ledger:
    if row["状态"] == "进行中":
        doing.append(row["编号"])
print(f"进行中：{doing}")

# 等效的「列表推导式」写法，一行搞定
doing2 = [row["编号"] for row in ledger if row["状态"] == "进行中"]
print(f"推导式写法：{doing2}")
# 读法：把「对每个 row 做什么」写在最前面，后面跟 for（从哪来）和 if（要哪些）。
# 建议：先写清楚的多行版，跑通了再考虑改成推导式。


print("=" * 50)
print("【4】while 循环 / break / continue")

n = 0
while n < 3:
    n += 1
    print(f"  第 {n} 次尝试")
# while 用在「不知道要转几圈」的场景，比如反复尝试直到成功。

print("--- break：满足条件就直接跳出 ---")
for row in ledger:
    if row["优先级"] == "P0":
        print(f"  找到 P0 了，是 {row['编号']}，不用再找了")
        break

print("--- continue：这一条跳过，继续下一条 ---")
for row in ledger:
    if row["状态"] == "已闭环":
        continue                      # 已闭环的不要，直接跳过去
    print(f"  待跟进：{row['编号']}")

# ⚠️ 死循环警告：while 后面的条件如果永远为真，程序会卡死。
# 若不小心跑出死循环，在终端里按 Ctrl + C 强制停止。


print("=" * 50)
print("【5】异常处理 try / except：让程序不因为一条脏数据崩掉")

texts = ["1000000", "abc", "3850"]

for t in texts:
    try:
        value = int(t)
        print(f"  {t!r} → 转换成功：{value}")
    except ValueError:
        print(f"  {t!r} → 不是数字，跳过（程序没有崩）")

# 为什么必须学这个：
# 真实数据里总有脏值（空格、中文、空单元格）。
# 没有 try，一条坏数据就让整个脚本中断；有了 try，脚本能跑完并告诉你哪条有问题。

# 兜底写法：不确定会抛什么错时
try:
    result = 10 / 0
except Exception as e:
    print(f"  出错了但被接住：{type(e).__name__}: {e}")
# 但不要滥用兜底——接住之后要么处理，要么打印出来，别静默吞掉错误。

print()


# ============================================================
#  动手练习（先自己写）
# ============================================================
print("=" * 50)
print("练习开始，共 5 题")

# 【1】按金额分档：≥100 万输出「大额」；1 万 ~ 100 万输出「常规」；<1 万输出「小额」。
#      用 if / elif / else 写，分别用 2000000、50000、3000 三个值测一遍。
test_amounts = [2000000, 50000, 3000]

# 你的代码 ↓
nemo = "p0"

if nemo =="p0":
    print("大额")
elif nemo  == "p1":
    print("常规")
else:
    print("小额")  

print(f"nemo>= 100万：{test_amounts[0]} → 大额")
print(f"nemo>=1万：<{test_amounts[1]} → 常规")
print(f"nemo<1万：{test_amounts[2]} → 小额")



# 【2】遍历 ledger，把所有「进行中」的事项名称打印出来（只打事项，不打编号）。

# 你的代码 ↓


# 【3】统计 ledger 里「进行中」的记录有几条，打印数量。
#      提示：这一题是「先建 X，再用 Y」型——计数用的变量要在循环开始之前先建好，
#            不要等到循环里才想起它。

# 你的代码 ↓


# 【4】用 while 循环打印 1 到 5（每个数字占一行）。

# 你的代码 ↓


# 【5】下面的列表里混了不能转成数字的脏数据，
#      请用 try / except 逐条转换，能转的放进新列表，不能转的打印出来。

raw = ["1200", "800", "未知", "3500", ""]

# 你的代码 ↓


print("练习结束")
print("=" * 50)


# ============================================================
#  参考答案（自己写完再看！）
# ============================================================
"""参考实现：

【1】
for amt in test_amounts:
    if amt >= 1000000:
        level = "大额"
    elif amt >= 10000:
        level = "常规"
    else:
        level = "小额"
    print(f"{amt} → {level}")


【2】
for row in ledger:
    if row["状态"] == "进行中":
        print(row["事项"])


【3】
count = 0
for row in ledger:
    if row["状态"] == "进行中":
        count += 1
print(count)          # 2
# 也可以用 sum 一行搞定：
# print(sum(1 for row in ledger if row["状态"] == "进行中"))


【4】
i = 1
while i <= 5:
    print(i)
    i += 1
# 别忘了 i += 1，忘了就是死循环。


【5】
good = []
for item in raw:
    try:
        good.append(int(item))
    except ValueError:
        print(f"跳过脏数据：{item!r}")
print(good)           # [1200, 800, 3500]
# 注意：int("") 抛的也是 ValueError，所以一条 except 就够。
# int(" 12 ") 是能成功的（Python 会自动去空格），int("3.5") 会失败，要用 float()。


复盘自检：
  □ 我能说出 if 后面那一行必须做什么（缩进）吗？
  □ 我知道 for 和 while 各自适合什么场景吗？
  □ 我知道 break 和 continue 的区别吗？
  □ 我写的脚本现在遇到脏数据会不会整体崩掉？
"""

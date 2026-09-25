# D4 速查卡 · 函数 / 作用域 / 主程序入口

> 用法：开工前滚动复习轮到 D4 时看这份，3–10 分钟，不重读 `04_functions.py`。
> 默写题先自己写，写完再对 `.py` 底部的参考答案。

---

## 1. 函数三要素

```python
def format_amount(amount):        # ① def 开头、冒号结尾
    """把金额格式化成万元"""        # ② docstring（鼠标悬停时看到的就是它）
    return f"{amount/10000:.1f} 万元"   # ③ return 把结果交回去
```

- 没有 `return` → 函数返回 `None`（屏幕上会打印出 `None`）
- 调用时括号必须写：`format_amount` 是名字，`format_amount()` 才是动作

---

## 2. 参数的规则

| 规则 | 说明 |
|------|------|
| 括号必须写，里面可以空 | `def main():` 合法，表示"不要原材料" |
| 要不要参数 | 这个函数需不需要**对不同的东西**干活？要 → 写参数；只跑固定流程 → 空括号 |
| 默认参数排最后 | `def make_item(pid, status="进行中", owner="陈驰")` —— 带默认值的必须排在没有默认值的**后面** |
| 可以按名字传 | `make_item("A011", owner="刘珂含")` —— 跳着传时用名字，清楚 |
| 个数要对上 | 多给：`main() takes 0 positional arguments but 1 was given`<br>少给：`greet() missing 1 required positional argument: 'name'` |

---

## 3. return 的三个用法

```python
return doing, closed          # ① 返回多个值：实际是一个元组，左边用两个变量接住（解包）
return "无需处理"              # ② 早返回：命中立刻走人，后面不用再套 if
                              # ③ 没有 return / 分支都没走到 → 返回 None
```

**早返回 vs 赋值**：写成 `result = "无需处理"` 不算数——函数不会离开，会被后面的 if 覆盖。该 `return` 就 `return`。

---

## 4. 作用域：三种情况

| 情况 | 要不要 `global` | 例子 |
|------|:---:|------|
| 函数里**只读**外面的变量 | 不需要 | `len(ledger)` 直接用 |
| 函数里**给**外面的变量赋值 | **必须写** `global counter` | 不写就报错 |
| 函数里起**同名**变量 | 不需要 | 里 `x=99`、外 `x=10`，互不影响 |

- 不写 `global` 就赋值 → `UnboundLocalError: cannot access local variable 'counter' where it is not associated with a value`
- **为什么不建议 `global`**：函数就不独立了，结果取决于外部变量当时是多少。要用外面的值，**当参数传进去**。

---

## 5. 主程序入口（两行，不是四行）

```python
if __name__ == "__main__":
    main()
```

- 直接运行这个文件 → `__name__` 是 `"__main__"` → `main()` 跑
- 被别的文件 `import` → `__name__` 是模块名 → `main()` **不跑**
- 防的是"别人 import 你的时候，顺手把演示输出全打一遍"
- 下划线前后各两个：`__name__`；`==` 是比较，`=` 是赋值

---

## 6. 最易混的 4 组

| # | 易混 | 区别 |
|---|------|------|
| 1 | `return` vs `print` | 把结果交回去（别人能用）/ 打到屏幕上（交不回去） |
| 2 | `return days > 0` vs `if...return True else...return False` | 都对，前者更短；`days > 0` 本身就算出布尔值 |
| 3 | `return` 在**循环里** vs 在**循环外** | 里：第一次命中就走人，只处理第一个 / 外：跑完全部再返回 |
| 4 | `d.get("状态")` vs `d["状态"]` | 缺键时不报错返回 None（危险）/ 缺键时报错（安全） |

---

## 7. D4 踩过的坑

| 现象 | 原因 | 修法 |
|------|------|------|
| 练习【3】只返回 `['A003']`，漏了 A011 | `return result` 缩进在 `if` 里，第一次命中就返回 | 把 `return` 移到与 `for` 对齐 |
| 屏幕上打印出 `None` | 所有分支都没走到 `return` | 末尾补兜底 `return` |
| 已闭环的记录输出了「本周内安排」 | 早返回写成了赋值 `result = ...`，被后面覆盖 | 改回 `return` |
| 删了某条记录的「状态」字段，结论是错的但不报错 | `.get` 返回 `None` 不炸 | 关键字段用 `["状态"]` 让它炸出来 |
| 删掉 `global counter` 后报错 `UnboundLocalError` | 函数里给外部变量赋值必须声明 | 加回 `global`（更好的做法是改成传参数） |

---

## 8. 3 分钟默写自测（不看文件，写完再对）

1. 写一个函数 `is_overdue(days)`：`days > 0` 返回 `True`，否则 `False`。
2. 写一个带默认参数的函数 `pick_by_status(rows, status="进行中")`，返回符合条件的编号列表（注意 `return` 的位置）。
3. 默写主程序入口那两行，并写出 `__name__` 在两种情况下分别是什么。
4. 说出三种作用域情况里，哪种必须写 `global`。

**答不上来的题号 → 回 `04_functions.py` 只跑那一节，不用整份重读。**

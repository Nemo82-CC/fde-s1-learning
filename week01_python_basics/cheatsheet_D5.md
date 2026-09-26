# D5 速查卡（文件读写 / CSV / JSON）

> 状态：**D5 进行中**，随块推进补充。
> 已完成：第 1 块 = 【0】路径 + 【1】读文本（2026-09-26）。
> 未完成：【2】读 CSV / 【3】写文本 / 【4】写 JSON / 4 题练习。
> 本卡里所有数值都是实跑过的，可以对着当答案。

**今晚这几个点串起来看，其实是一条线：先找到文件在哪 → 用对的编码打开 → 按大小决定怎么读 → 读进来处理。**

---

## 1. 路径：照抄这三行（最重要）

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent              # 脚本所在目录
DATA_FILE = BASE_DIR / "data" / "教育政策清单_示例.csv"   # 往下拼
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)                          # 没有就建，有了也不报错
```

| 写法 | 含义 |
|------|------|
| `__file__` | 这个脚本文件自己的路径（Python 自动创建，不用赋值） |
| `.resolve()` | 转成完整绝对路径，理顺 `..` 之类 |
| `.parent` | 取上一层目录 = 脚本所在文件夹 |
| `/`（Path 之间） | **拼路径**，不是除法 |

**为什么不能用裸相对路径 `"data/xxx.csv"`**：相对路径相对的是**当前工作目录 cwd**，不是脚本文件。
VS Code 里 cwd 是工作区根 `fde_s1`，于是会去找 `fde_s1/data/...` → `FileNotFoundError`。
实测：`Path("data/教育政策清单_示例.csv").resolve()` → `D:\...\fde_s1\data\教育政策清单_示例.csv`（不存在）。

---

## 2. dunder：为什么 `__file__` 两边各两个下划线

- **不是语法强制，是命名约定**。双下划线前后包围的名字 = Python 给自己留的"专用车位"，叫 dunder。
- 目的：防止和你自己起的普通变量名撞车。
- 实测：自定义 `__我自己造的双下划线__ = 1` **能跑**——所以是约定不是强制；但规矩是别自己发明。
- `__file__` 只在**从 .py 文件运行**时存在；`python -c` 模式下没有文件可指，报
  `NameError: name '__file__' is not defined`。
- 同族的 `__name__`：直接运行时值是字符串 `"__main__"`（D4 学的主程序入口就是判它）。

---

## 3. 读文本

```python
# 小文件：一次读完
with open(文件路径, encoding="utf-8") as f:
    content = f.read()

# 大文件：逐行读
with open(文件路径, encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"  第 {i} 行：{line.strip()}")
```

| 写法 | 说明 |
|------|------|
| `with open(...) as f:` | 代码块结束**自动关文件**，不用 `f.close()`；别用老写法 `f = open()` |
| `encoding="utf-8"` | **读中文必须写**，别依赖系统默认编码 |
| `f.read()` | 一次读全部，返回字符串 |
| `.write_text("...", encoding="utf-8")` | Path 对象一次性写文本；`\n` 是换行符 |
| `{content!r}` | `!r` = 原样显示，能看见引号和 `\n` |
| `line.strip()` | 去掉每行末尾的换行符 `\n` |

**`!r` 实测对比**（`demo.txt` 内容）：
- 无 `!r`：`第一行内容` ⏎ `第二行内容`
- 有 `!r`：`'第一行内容\n第二行内容\n'`

**编码实测**：用 `encoding="gbk"` 读 UTF-8 中文文件 →
`UnicodeDecodeError: 'gbk' codec can't decode byte 0xac in position 2: illegal multibyte sequence`

---

## 4. 文件大小：怎么判、怎么读

```python
size = 路径.stat().st_size                 # 字节
print(f"{size} 字节 / {size/1024:.2f} KB / {size/1024/1024:.2f} MB")
```

| 文件（实测） | 大小 |
|------|------|
| `output/demo.txt` | 34 字节 |
| `data/教育政策清单_示例.csv` | 663 字节 = 0.65 KB |

- **字节数 ≠ 字符数**：UTF-8 下一个汉字 3 字节。实测 `demo.txt` 内容 12 个字符、32 字节。
- 数行数：`len(content.splitlines())`。
- 读法取舍：< 1 MB 直接 `read()`；几十 MB 逐行读；再大考虑分块。日常政策文本、CSV、台账导出都在 KB~几 MB 级，`read()` 完全够。

---

## 5. 括号分工 + f-string（2026-09-26 补，详见 `cheatsheet_D1-D3.md` 第 0.5 节）

**口诀：动手用圆、取东西用方、造容器用大。**

| 括号 | 角色 | 例子 |
|------|------|------|
| `()` | 做动作：函数 / 方法调用 | `print(...)`、`int("35")`、`len(rows)`、`title.strip()` |
| `[]` | 取东西：下标 / 键 / 切片 | `rows[0]`、`lines[-1]`、`nums[1:3]`、`row["发布年份"]` |
| `{}` | 造容器：字典、集合 | `{"状态": "进行中"}`、`{"教育部", "财政部"}` |

- 动作后面只能用 `()`：`print {int(3.5)}` → `SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?`
- **字典用 `{}` 造、用 `[]` 取**：`row{"政策名称"}` → `SyntaxError: invalid syntax. Perhaps you forgot a comma?`
- **f-string 的 `{}` 是占位开关**：没包进 `{}` 的就是普通文字。
  `print(f"最后6个字： sentence[-6:]")` 输出字面量；写成 `{sentence[-6:]}` 才输出 `解到工程实现`。

---

## 6. 还没学的（后续块补进来）

| 节 | 内容 | 行号 |
|----|------|------|
| 【2】 | 读 CSV（`csv.DictReader`）、`encoding="utf-8-sig"` | 第 60 行起 |
| 【3】 | 写文本文件（生成 Markdown 摘要） | 第 88 行起 |
| 【4】 | 写 JSON（`json.dumps(..., ensure_ascii=False, indent=2)`） | 第 102 行起 |
| 练习 | 4 题 | 第 132 行起 |

# Anki Modern 卡片模板说明

本项目提供 5 种现代化 Anki 笔记类型，支持 Markdown、LaTeX 数学公式和代码高亮。

---

## 📋 笔记类型一览

| 笔记类型 | 字段 | 生成卡片数 | 适用场景 |
|---------|------|-----------|---------|
| Cloze-Modern | Text, Extra | 按填空数 | 填空记忆 |
| Cloze-Modern-Typing | Text, Extra | 按填空数 | 填空+打字 |
| Basic-Modern | Front, Back | 1 | 问答 |
| Basic-Modern-Reversed | Front, Back | 2 | 双向问答 |
| Basic-Modern-Typing | Front, Back | 1 | 问答+打字 |

---

## 🔲 Cloze-Modern

**填空题模板** - 最常用的记忆模板

### 字段

| 字段 | 必填 | 说明 |
|-----|-----|------|
| **Text** | ✅ | 正文内容，使用 `{{c1::答案}}` 创建填空 |
| **Extra** | ❌ | 补充说明（目前未在卡片中显示） |

### 用法示例

```markdown
## 拉格朗日中值定理

函数 $f(x)$ 在闭区间上{{c1::连续}}，在开区间内{{c2::可导}}，
则存在 $\xi$ 使得：$${{c3::f'(\xi) = \frac{f(b)-f(a)}{b-a}}}$$
```

### 效果
- 每个 `{{c1::...}}` 生成一张独立的卡片
- 正面显示 `[...]` 遮盖
- 背面显示完整答案

---

## ⌨️ Cloze-Modern-Typing

**填空打字模板** - 需要手动输入答案

### 字段

与 Cloze-Modern 相同

### 特点
- 正面包含输入框，需要打字输入答案
- 背面显示 diff 对比（正确/错误/缺失）
- 适合拼写练习、公式记忆

---

## 📝 Basic-Modern

**基础问答模板** - 最简单的正反面卡片

### 字段

| 字段 | 必填 | 说明 |
|-----|-----|------|
| **Front** | ✅ | 正面内容（问题） |
| **Back** | ✅ | 背面内容（答案） |

### 用法示例

**Front:**
```markdown
## 简答题
请解释 Python 中 `*args` 和 `**kwargs` 的区别。
```

**Back:**
```markdown
- `*args`：接收任意数量的**位置参数**，打包为元组
- `**kwargs`：接收任意数量的**关键字参数**，打包为字典

\```python
def example(*args, **kwargs):
    print(args)    # (1, 2, 3)
    print(kwargs)  # {'a': 1, 'b': 2}
\```
```

---

## 🔄 Basic-Modern-Reversed

**双向问答模板** - 一个笔记生成两张卡片

### 字段

与 Basic-Modern 相同

### 生成的卡片

| 卡片 | 正面 | 背面 |
|-----|------|------|
| Card 1 | Front | Front + Back |
| Card 2 (Reversed) | Back | Back + Front |

### 适用场景

- **词汇学习**：英文 ↔ 中文
- **名词解释**：术语 ↔ 定义
- **人物事件**：姓名 ↔ 成就

### 用法示例

**Front:**
```markdown
## Photosynthesis
```

**Back:**
```markdown
**光合作用** 🌱

植物利用光能将二氧化碳和水转化为葡萄糖和氧气的过程。

$$6CO_2 + 6H_2O \xrightarrow{光能} C_6H_{12}O_6 + 6O_2$$
```

---

## ✍️ Basic-Modern-Typing

**打字问答模板** - 需要手动输入答案

### 字段

与 Basic-Modern 相同

### 特点
- 正面显示问题 + 输入框
- 需要完整输入 Back 字段内容
- 适合简短答案的精确记忆

### 注意事项
- Back 字段应保持**简短**（单词、短语、数字等）
- 不适合长段落答案

---

## 🎨 通用特性

所有模板都支持：

### Markdown 语法
- 标题：`# H1` `## H2` `### H3`
- 加粗：`**粗体**`
- 斜体：`*斜体*`
- 列表：`- item` 或 `1. item`
- 引用：`> 引用内容`
- 代码：`` `inline` `` 或代码块
- 表格、链接、图片等

### LaTeX 公式
- 行内公式：`$E=mc^2$`
- 块级公式：`$$\int_0^\infty e^{-x^2} dx$$`

### 代码高亮
````markdown
```python
def hello():
    print("Hello, Anki!")
```
````

支持语言：Python, JavaScript, C++, Java, Go, Rust 等

### 深色模式
- 自动跟随系统主题
- 支持 Anki 内置夜间模式

---

## 📱 平台兼容性

| 平台 | 状态 |
|-----|------|
| Anki Desktop (macOS/Windows/Linux) | ✅ 完全支持 |
| AnkiMobile (iOS) | ✅ 完全支持 |
| AnkiDroid (Android) | ✅ 完全支持 |
| AnkiWeb | ⚠️ 部分支持（无 JS） |

---

## 🚀 快速开始

1. 确保 Anki 已安装 [AnkiConnect](https://ankiweb.net/shared/info/2055492159) 插件
2. 运行资源脚本和同步脚本：
   ```bash
   bash sync_font.sh
   bash sync_libs.sh
   python3 anki_connect.py
   ```
3. 在 Anki 中选择对应的笔记类型创建卡片

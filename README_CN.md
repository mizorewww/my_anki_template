# Anki 现代填空模板 (Anki Cloze Modern Template)

[English](README.md) | **中文**

专为追求审美与功能的学习者打造的 Anki 模板，完美支持 Markdown、LaTeX 公式、代码高亮，并包含 4 种专用笔记类型。

## ✨ 功能特性

- 🎨 **现代设计**:
  - **字体**: 正文默认使用 **LXGW WenKai (霞鹜文楷)**，代码使用 **Maple Mono**，阅读体验极佳。
  - **主题**: 自动支持 **浅色/深色模式** (跟随系统或 Anki 设置)。
  - **响应式**: 针对桌面端和移动端 (iOS/Android) 进行了深度优化。

- 📝 **Markdown & LaTeX**:
  - **Markdown**: 支持表格、列表、引用、粗体/斜体等标准语法。
  - **纯净 LaTeX**: 公式使用 KaTeX 渲染。
    - **零侵入**: 绝不修改公式源代码。
    - **智能标注**: 公式内的填空（Cloze）通过**外部蓝色虚线**（公式块下方或行内下方）进行视觉标注，既明确了填空位置，又保持了数学公式的纯粹性。

- 💻 **代码高亮**:
  - 自动识别并高亮代码块 (Python, JS, C++, 等)，使用 Highlight.js 驱动。
  - 拥有独立的激活/非激活样式，阅读舒适。

- ⌨️ **拼写模式 (Typing)**:
  - 提供专门的拼写模板。
  - 提交答案后显示 **Diff 对比**（绿色/红色背景），帮助你精准校对拼写错误。

## 🗂 笔记类型

运行同步脚本后，Anki 中会自动创建以下 **5** 种笔记类型：

### 1. Cloze-Modern (标准填空)
- **类型**: 填空题 (Cloze)
- **描述**: 经典的填空体验，增强了 Markdown 和 LaTeX 支持。
- **字段**:
  - `Text`: 包含挖空的内容 (例如: `法国的首都是 {{c1::巴黎}}。`)。
  - `Extra`: 背面显示的额外信息。

### 2. Cloze-Modern-Typing (拼写填空)
- **类型**: 填空题 (Cloze)
- **描述**: 挖空部分显示为输入框，强制要求手动输入答案。背面显示正误对比。
- **适用场景**: 单词拼写记忆、编程语法练习。

### 3. Basic-Modern (简答题)
- **类型**: 问答题 (Basic)
- **描述**: 标准的 正面/背面 卡片。
- **字段**:
  - `Front`: 问题。
  - `Back`: 答案。
- **适用场景**: 概念定义、开放式问题。

### 4. Basic-Modern-Reversed (双向问答)
- **类型**: 问答题 (Basic)
- **描述**: 一个笔记自动生成 **两张卡片**：正向 (Front→Back) 和反向 (Back→Front)。
- **字段**: 与 Basic-Modern 相同。
- **适用场景**: 词汇双向记忆（英文 ↔ 中文）、术语与定义互记。

### 5. Basic-Modern-Typing (问答拼写)
- **类型**: 问答题 (Basic)
- **描述**: 正面显示问题和输入框，要求输入完整答案。背面显示与标准答案的 Diff 对比。
- **适用场景**: 精确记忆定义、背诵代码片段。

## 🚀 安装指南

### 前置要求
1. **Anki Desktop** (建议使用最新版)。
2. **AnkiConnect 插件**:
   - 打开 Anki -> 工具 -> 插件 -> 获取插件。
   - 输入代码: `2055492159`
   - 安装完成后 **重启 Anki**。

### 配置步骤
1. 克隆或下载本仓库。
2. **下载资源文件** (运行提供的 Shell 脚本):
   ```bash
   # 1. 下载字体 (LXGW WenKai, Maple Mono)
   bash sync_font.sh
   
   # 2. 下载 JS/CSS 依赖库 (Marked, KaTeX, Highlight.js)
   bash sync_libs.sh
   ```
   *(Windows 用户请使用 Git Bash 或 WSL 运行上述命令)*

3. **同步到 Anki**:
   ```bash
   python3 anki_connect.py
   ```
   脚本将自动完成以下操作:
   - ✅ 自动检查更新 (git pull)
   - ✅ 将下载的字体和库文件同步到 Anki 媒体文件夹。
   - ✅ 在 Anki 中创建/更新 5 种笔记类型。
   - ✅ 在 "Default" 牌组中创建示例卡片。

## ✍️ 书写示例

### Markdown
直接在字段中书写 Markdown:

```markdown
# 标题
- 列表项 1
- 列表项 2

**粗体** 和 *斜体*。
```

### LaTeX 公式
使用 `$$...$$` 包裹块级公式，`$...$` 包裹行内公式。

```latex
二次方程求根公式:
$${{c1::x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}}}$$
```
*(注: 背面会用蓝色虚线通过 CSS 标注答案位置，公式内容保持纯文本渲染)*

### 代码块

```python
def hello():
    print("Hello Anki")
```



## 📸 截图展示

### 1. LaTeX 公式渲染
*(纯净渲染，支持行内/块级公式，答案通过蓝色虚线标注)*

![LaTeX Demo](screenshots/latex.png)

### 2. 代码高亮
*(支持多种语言，日间/夜间模式自动切换)*

![Code Demo](screenshots/highlight.png)

### 3. 拼写检查 (Diff)
*(Basic-Typing 和 Cloze-Typing 模板均支持)*

![Diff Demo](screenshots/basic_input_show_diff.png)

---
**祝学习愉快！**

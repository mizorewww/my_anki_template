# Anki Cloze Modern Template / Anki 现代填空模板

[English] A beautiful, modern Anki template supporting Markdown, LaTeX, code highlighting, and 4 specialized note types. Built for serious learners who care about aesthetics and functionality.

[中文] 一个美观、现代的 Anki 模板，完美支持 Markdown、LaTeX 公式、代码高亮。专为追求审美与功能的学习者打造，包含 4 种专用笔记类型。

## ✨ Features / 功能特性

- 🎨 **Modern Design / 现代设计**:
  - **Typography**: Uses **LXGW WenKai (霞鹜文楷)** for body text and **Maple Mono** for code.
  - **Theming**: Automatic Light/Dark mode support (跟随系统或 Anki 设置).
  - **Responsive**: Optimized for Desktop and Mobile (iOS/Android).

- 📝 **Markdown & LaTeX**:
  - Write cards using standard Markdown (tables, lists, quotes, bold/italic).
  - **Pure LaTeX**: Math formulas are rendered using KaTeX. **Active clozes in LaTeX are NOT modified inside the formula**. instead, they are visually marked with a **blue dashed line** (below for blocks, underline for inline) to indicate the answer position without altering the math itself.
  - **纯净 LaTeX**: 公式渲染保持 100% 源码纯净。填空位置通过**外部蓝色虚线**标注，绝不修改公式内部字符。

- 💻 **Code Highlighting / 代码高亮**:
  - Automatically highlights code blocks (Python, JS, C++, etc.) using Highlight.js.
  - Distinct active/inactive styles.

- ⌨️ **Typing Support / 拼写模式**:
  - Dedicated templates for typing answers.
  - Visual Diff (Green/Red background) to check your spelling accuracy.

## 🗂 Note Types / 笔记类型

The script automatically creates these 4 note types in your Anki:

### 1. Cloze-Modern (Standard Cloze / 标准填空)
- **Type**: Cloze
- **Description**: The classic fill-in-the-blank experience supercharged with Markdown/LaTeX.
- **Fields**:
  - `Text`: The content with clozes (e.g., `The capital of France is {{c1::Paris}}.`).
  - `Extra`: Additional info shown on the back.

### 2. Cloze-Modern-Typing (Typing Cloze / 拼写填空)
- **Type**: Cloze
- **Description**: Input box appears for the active cloze. You must type the answer. Back side shows a diff comparison.
- **Fields**: `Text`, `Extra`
- **Use Case**: Language learning (spelling words), programming syntax.

### 3. Basic-Modern (Q&A / 简答题)
- **Type**: Basic (Non-Cloze)
- **Description**: Standard front/back card.
- **Fields**:
  - `Front`: Visible question.
  - `Back`: Answer shown after flipping.
- **Use Case**: Concept definitions, open-ended questions.

### 4. Basic-Modern-Typing (Typing Q&A / 问答拼写)
- **Type**: Basic
- **Description**: Question on front with an input box. Type the full answer to check against the Back field.
- **Fields**: `Front`, `Back`
- **Use Case**: Memorizing exact definitions or code snippets.

## 🚀 Installation / 安装指南

### Prerequisites / 前置要求
1. **Anki Desktop** (latest version recommended).
2. **AnkiConnect Plugin**:
   - Open Anki -> Tools -> Add-ons -> Get Add-ons.
   - Code: `2055492159`
   - **Restart Anki** after installation.

### Setup / 如果配置
1. Clone or download this repository.
2. Run the sync script:
   ```bash
   python3 anki_connect.py
   ```
   This script will:
   - ✅ Download necessary fonts (LXGW WenKai, Maple Mono).
   - ✅ Download JS/CSS libraries (Marked, KaTeX, Highlight.js).
   - ✅ Create/Update the 4 Note Types in Anki.
   - ✅ Create Example Cards in the "Default" deck.

## ✍️ Usage Examples / 书写示例

### Markdown
Simply write Markdown in the fields:

```markdown
# Heading
- List item 1
- List item 2

**Bold text** and *Italic text*.
```

### LaTeX Math
Use `$$...$$` for block math and `$...$` for inline math.

```latex
The quadratic formula is:
$${{c1::x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}}}$$
```
*(Note: The active part will be marked with a blue dashed line on the back)*

### Code Block
```markdown
```python
def hello():
    print("Hello Anki")
```
```

---
**Enjoy your learning!**

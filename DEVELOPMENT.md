# Anki 模板开发指南

本文档为开发新的 Anki 卡片模板提供指导，基于 Cloze-Modern 模板的架构和最佳实践。

## 目录

- [项目架构](#项目架构)
- [五阶段令牌化渲染器](#五阶段令牌化渲染器)
- [创建新模板](#创建新模板)
- [样式系统](#样式系统)
- [媒体文件管理](#媒体文件管理)
- [常见问题](#常见问题)

---

## 项目架构

```
my_anki_template/
├── anki_connect.py           # Anki Connect 同步脚本
├── sync_libs.sh              # 下载 JS/CSS 依赖
├── sync_font.sh              # 下载字体文件
├── templates/
│   ├── cloze/                # 填空题模板
│   │   ├── front.html
│   │   ├── back.html
│   │   └── style.css
│   ├── basic/                # [示例] 基础问答模板
│   │   ├── front.html
│   │   ├── back.html
│   │   └── style.css
│   └── vendor/               # 第三方库 (自动生成)
└── fonts/                    # 字体文件 (自动生成)
```

---

## 五阶段令牌化渲染器

这是本项目的核心技术，解决了 Anki 标签与 Markdown/LaTeX 的兼容性冲突。

### 处理流程

```
原始内容 → [阶段1] 保护 Cloze 标签
         → [阶段2] 保护 LaTeX 公式
         → [阶段3] Markdown 渲染
         → [阶段4] 还原并渲染 LaTeX
         → [阶段5] 还原 Cloze 标签
         → 最终 HTML
```

### 为什么需要这个？

Anki 的填空标签 `{{c1::答案}}` 会被转换为 `<span class="cloze">...</span>`，如果直接用 Markdown 渲染器处理，会导致：
- HTML 标签被转义
- LaTeX 公式中的特殊字符被错误处理
- 代码块中的内容被误解析

### 关键代码模式

```javascript
// 从隐藏 div 获取内容（避免反引号问题）
const rawContent = document.getElementById('raw-content').innerHTML;

// 阶段1: 保护 Anki 填空标签
const clozeTokens = [];
let tokenized = rawContent.replace(
    /<span class="cloze[^"]*"[^>]*>[\s\S]*?<\/span>/gi, 
    function(match) {
        const token = '%%CLOZE_' + clozeTokens.length + '%%';
        clozeTokens.push(match);
        return token;
    }
);
```

---

## 创建新模板

### 步骤 1: 创建模板目录

```bash
mkdir -p templates/your-template-name
```

### 步骤 2: 创建模板文件

**front.html** 必须包含以下结构：

```html
<!-- 样式引用 -->
<link rel="stylesheet" href="_katex.min.css">
<link rel="stylesheet" href="_github.min.css" media="(prefers-color-scheme: light)">
<link rel="stylesheet" href="_github-dark.min.css" media="(prefers-color-scheme: dark)">

<!-- 渲染容器 -->
<div class="content-wrapper">
    <div id="rendered-content"></div>
</div>

<!-- ⚠️ 关键: 使用隐藏 div 存储原始内容 -->
<div id="raw-content" style="display:none;">{{你的字段}}</div>

<!-- 脚本引用 (必须在内容 div 之后) -->
<script src="_marked.min.js"></script>
<script src="_katex.min.js"></script>
<script src="_highlight.min.js"></script>

<!-- 渲染脚本 -->
<script>
(function() {
    // 复制 cloze 模板的渲染逻辑
})();
</script>
```

### 步骤 3: 创建样式文件

可以基于 `templates/cloze/style.css` 修改，关键是保持 CSS 变量体系：

```css
:root {
    --bg-primary: #fafafa;
    --text-primary: #1a1a2e;
    /* ... */
}

.nightMode {
    --bg-primary: #0f0f1a;
    --text-primary: #e8e8f0;
    /* ... */
}
```

### 步骤 4: 注册到 anki_connect.py

在 `anki_connect.py` 中添加新模板的配置：

```python
# 在文件顶部添加
YOUR_MODEL_NAME = "Your-Model-Name"
YOUR_TEMPLATE_DIR = SCRIPT_DIR / "templates" / "your-template-name"

# 添加创建函数
def create_your_model():
    # 参考 create_or_update_model() 实现
    pass
```

---

## 样式系统

### CSS 变量

所有颜色和尺寸都应使用 CSS 变量，便于主题切换：

| 变量 | 用途 |
|------|------|
| `--bg-primary` | 主背景色 |
| `--bg-secondary` | 次要背景色 |
| `--text-primary` | 主要文本颜色 |
| `--text-secondary` | 次要文本颜色 |
| `--accent-color` | 强调色 |
| `--cloze-color` | 填空高亮颜色 |
| `--code-bg` | 代码块背景 |

### 字体

```css
/* 正文 */
font-family: 'LXGW WenKai', sans-serif;

/* 代码 */
font-family: 'Maple Mono', monospace;
```

### 深色模式

支持三种触发方式：
1. **系统级**: `@media (prefers-color-scheme: dark)`
2. **Anki 类**: `.nightMode`
3. **手动类**: `.night_mode` 或 `[data-theme="dark"]`

---

## 媒体文件管理

### 命名规范

所有上传到 Anki 的媒体文件必须以 `_` 开头：

| 本地文件 | Anki 媒体文件名 |
|----------|-----------------|
| `marked.min.js` | `_marked.min.js` |
| `LXGWWenKai-Regular.ttf` | `_LXGWWenKai-Regular.ttf` |

### 添加新的媒体文件

在 `anki_connect.py` 的 `sync_all_media()` 函数中添加：

```python
new_files = [
    ("_your-file.js", "your-file.js"),
]

for anki_name, local_name in new_files:
    filepath = VENDOR_DIR / local_name
    result = sync_media_file(anki_name, filepath, force=force)
    # ...
```

### 强制重新上传

当需要更新媒体文件时，修改 main 函数调用：

```python
sync_all_media(force=True)
```

---

## 常见问题

### Q: 卡片显示空白

**原因**: JavaScript 语法错误，通常是内容中的反引号导致模板字符串破坏。

**解决方案**: 使用隐藏 div 存储内容，而不是 JavaScript 模板字符串：

```html
<!-- ✗ 错误 -->
<script>
const content = `{{Field}}`;  // 如果 Field 包含反引号会出错
</script>

<!-- ✓ 正确 -->
<div id="raw-content" style="display:none;">{{Field}}</div>
<script>
const content = document.getElementById('raw-content').innerHTML;
</script>
```

### Q: 库文件未加载

**检查步骤**:
1. 运行 `./sync_libs.sh` 确保库文件存在
2. 运行 `python anki_connect.py` 同步到 Anki
3. 在模板中添加加载检查：

```javascript
if (typeof marked === 'undefined') {
    document.getElementById('rendered-content').innerHTML = 
        '<p style="color:red;">错误: marked.js 未加载</p>';
    return;
}
```

### Q: LaTeX 公式不渲染

**检查**:
1. 确保 `_katex.min.js` 和 `_katex.min.css` 已上传
2. 检查公式语法：
   - 行内: `$E=mc^2$`
   - 块级: `$$E=mc^2$$`

### Q: 代码高亮不工作

**检查**:
1. 确保使用正确的代码块语法：
   ````markdown
   ```python
   print("hello")
   ```
   ````
2. 确保 `_highlight.min.js` 已加载

---

## 调试技巧

### 使用调试脚本

```bash
python debug_cards.py
```

### 在浏览器中预览

创建一个测试 HTML 文件，模拟 Anki 环境：

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="templates/vendor/katex.min.css">
</head>
<body class="nightMode">
    <!-- 粘贴你的模板内容 -->
</body>
</html>
```

### Anki Console

在 Anki 中按 `Ctrl+Shift+;` 打开调试控制台，查看 JavaScript 错误。

---

## 贡献新模板

1. Fork 本项目
2. 创建新模板目录和文件
3. 更新 `anki_connect.py` 添加模板支持
4. 更新 `README.md` 添加使用说明
5. 提交 PR

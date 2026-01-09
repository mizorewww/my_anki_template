# Anki Modern Templates

为 Anki 设计的现代化卡片模板，改善官方 Anki 中不佳的视觉体验。

## 功能特点 / Features

- **现代视觉设计**: 圆角卡片、渐变阴影，支持自动切换深色/浅色主题。
- **全格式支持**: 内置 Markdown 渲染、LaTeX 公式 (KaTeX) 和代码高亮 (Highlight.js)。
- **离线使用**: 核心库已内嵌，无需网络连接。
- **健壮渲染引擎**: 采用"五阶段令牌化渲染"，完美解决 Anki 标签与 Markdown/LaTeX 的兼容性冲突。
- **自定义字体**: 内置 `霞鹜文楷` 与 `Maple Mono` 支持。

## 截图

![code_highlight](screenshots/highlight.png)
支持高亮

![latex](screenshots/latex.png)
支持LaTeX

## 项目结构 / Project Structure

```
my_anki_template/
├── anki_connect.py       # 一键同步脚本（模型更新、媒体同步、示例创建）
├── sync_libs.sh          # 同步最新的第三方 JS/CSS 库
├── sync_font.sh          # 同步字体文件
├── templates/
│   ├── cloze/            # 填空题模板
│   │   ├── front.html    # 正面模板
│   │   ├── back.html     # 背面模板
│   │   └── style.css     # 样式文件
│   └── vendor/           # 第三方库 (由脚本生成)
└── fonts/                # 字体文件 (由脚本生成)
```

## 快速开始 / Quick Start

### 1. 安装 AnkiConnect 插件

1. 打开 **Anki**
2. 进入 `工具` → `插件` → `获取插件`
3. 输入插件代码: **`2055492159`**
4. 重启 Anki

### 2. 初始化环境

确保已安装 Python 3，然后执行以下命令：

```bash
# 克隆项目
git clone https://github.com/your-username/my_anki_template.git
cd my_anki_template

# 下载第三方库 (Markdown/LaTeX/代码高亮)
./sync_libs.sh

# 下载字体文件
./sync_font.sh
```

### 3. 导入到 Anki

确保 Anki 已启动，然后运行：

```bash
python anki_connect.py
```

脚本将自动：
- ✅ 上传字体和 JS/CSS 库到 Anki 媒体文件夹
- ✅ 创建 `Cloze-Modern` 笔记类型
- ✅ 创建示例卡片（拉格朗日中值定理 + Python 装饰器）

### 4. 创建卡片

在 Anki 中：
1. 点击 `添加`
2. 选择笔记类型 `Cloze-Modern`
3. 在 `Text` 字段中使用 Markdown 格式编写内容
4. 使用 `{{c1::答案}}` 语法创建填空

## 卡片编写指南 / Writing Cards

### Markdown 语法

```markdown
## 标题

**粗体** 和 *斜体*

- 列表项 1
- 列表项 2

> 引用块

`行内代码`
```

### LaTeX 公式

行内公式使用单个 `$`：
```
勾股定理: $a^2 + b^2 = c^2$
```

块级公式使用双 `$$`：
```
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

### 代码块

使用三个反引号，并指定语言：

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### 填空语法

```markdown
拉格朗日中值定理要求函数在闭区间上{{c1::连续}}，在开区间内{{c2::可导}}。
```

## 主题切换 / Theming

模板会自动跟随系统深色/浅色模式。在 Anki 中也支持通过 `.nightMode` 类切换。

## 更新模板 / Updating

如需更新模板样式或渲染逻辑，修改 `templates/cloze/` 目录下的文件后，重新运行：

```bash
python anki_connect.py
```

## 故障排除 / Troubleshooting

### 连接失败

```
无法连接到 Anki Connect
```

**解决方案**：
1. 确保 Anki 已启动
2. 确保 AnkiConnect 插件已安装
3. 检查防火墙是否阻止了 `127.0.0.1:8765`

### 公式不显示

**解决方案**：
确保运行了 `./sync_libs.sh` 并重新执行 `python anki_connect.py`

## License / 许可证

**Public Domain (CC0 1.0)** - 详情请参阅项目内 LICENSE 文件。

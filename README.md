## 功能特点 / Features

- **现代视觉设计**: 圆角卡片、渐变阴影，支持自动切换深色/浅色主题。
- **全格式支持**: 内置 Markdown 渲染、LaTeX 公式 (KaTeX) 和代码高亮 (Highlight.js)。
- **离线使用**: 核心库已内嵌，无需网络连接。
- **健壮渲染引擎**: 采用“五阶段令牌化渲染”，完美解决 Anki 标签与 Markdown/LaTeX 的兼容性冲突。
- **自定义字体**: 内置 `霞鹜文楷` 与 `Maple Mono` 支持。

## 项目结构 / Project Structure

- `anki_connect.py`: 一键同步脚本（模型更新、媒体同步、示例创建）。
- `sync_libs.sh`: 同步最新的第三方 JS/CSS 库。
- `sync_font.sh`: 同步字体文件。
- `templates/`: 存放 HTML/CSS 模板源码。
- `test_template.py`: 渲染逻辑单元测试。

## 使用方法 / Usage

### 1. 准备工作

1. 打开 **Anki** 并安装插件 **AnkiConnect** (代码: `2055492159`)。
2. 确保已安装 Python 3。

### 2. 初始化环境

同步库文件（Markdown/LaTeX/代码高亮）：
```sh
./sync_libs.sh
```

同步字体文件：
```sh
./sync_font.sh
```


## License / 许可证

**Public Domain (CC0 1.0)** - 详情请参阅项目内说明。

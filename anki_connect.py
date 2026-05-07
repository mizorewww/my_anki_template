#!/usr/bin/env python3
"""
Anki Connect 同步脚本
功能：
1. 按需拉取最新代码 (python3 anki_connect.py --pull)
2. 创建/更新笔记类型
3. 同步媒体文件（字体、JS/CSS 库）
4. 创建示例卡片
"""

import argparse
import json
import urllib.request
import base64
import os
import re
import subprocess
from pathlib import Path

# ======================= 配置 =======================
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 目录配置
SCRIPT_DIR = Path(__file__).parent.resolve()
FONTS_DIR = SCRIPT_DIR / "fonts"
VENDOR_DIR = SCRIPT_DIR / "templates" / "vendor"
SHARED_DIR = SCRIPT_DIR / "templates" / "shared"
MEDIA_SETUP_HINT = (
    "请先运行资源脚本后再同步：\n"
    "  bash sync_font.sh\n"
    "  bash sync_libs.sh"
)


# ======================= Anki Connect API =======================
def invoke(action: str, timeout: int = 30, **params):
    """调用 Anki Connect API"""
    request_json = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode("utf-8")
    
    try:
        response = urllib.request.urlopen(
            urllib.request.Request(ANKI_CONNECT_URL, request_json),
            timeout=timeout
        )
        result = json.loads(response.read().decode("utf-8"))
        
        if result.get("error"):
            raise Exception(result["error"])
        return result.get("result")
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"无法连接到 Anki Connect。请确保：\n"
            f"1. Anki 已启动\n"
            f"2. AnkiConnect 插件已安装 (代码: 2055492159)\n"
            f"原始错误: {e}"
        )


def check_connection():
    """检查 Anki Connect 连接"""
    try:
        version = invoke("version")
        print(f"✓ Anki Connect 已连接 (版本: {version})")
        return True
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


# ======================= 媒体文件同步 =======================
def check_media_exists(filename: str) -> bool:
    """检查媒体文件是否已存在于 Anki"""
    try:
        result = invoke("getMediaFilesNames", pattern=filename)
        return filename in result if result else False
    except:
        return False


def sync_media_file(filename: str, filepath: Path, timeout: int = 60, force: bool = False):
    """同步单个媒体文件到 Anki"""
    if not filepath.exists():
        raise FileNotFoundError(f"缺少必需媒体文件: {filepath}\n{MEDIA_SETUP_HINT}")
    
    # 检查文件是否已存在 (除非强制上传)
    if not force and check_media_exists(filename):
        return "skipped"
    
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    
    invoke("storeMediaFile", timeout=timeout, filename=filename, data=data)
    return True


def sync_all_media(force: bool = False):
    """同步所有媒体文件
    
    Args:
        force: 如果为 True，则强制重新上传所有文件
    """
    print("\n📦 同步媒体文件...")
    
    synced = 0
    skipped = 0
    
    # 同步字体文件
    font_files = [
        ("_LXGWWenKai-Regular.ttf", "LXGWWenKai-Regular.ttf"),
        ("_LXGWWenKai-Medium.ttf", "LXGWWenKai-Medium.ttf"),
        ("_LXGWWenKai-Light.ttf", "LXGWWenKai-Light.ttf"),
        ("_MapleMono-NF-CN-Regular.ttf", "MapleMono-NF-CN-Regular.ttf"),
        ("_MapleMono-NF-CN-Bold.ttf", "MapleMono-NF-CN-Bold.ttf"),
        ("_MapleMono-NF-CN-Italic.ttf", "MapleMono-NF-CN-Italic.ttf"),
    ]
    
    print("  字体文件:")
    for anki_name, local_name in font_files:
        filepath = FONTS_DIR / local_name
        result = sync_media_file(anki_name, filepath, timeout=300, force=force)
        if result == "skipped":
            print(f"    ⏭ {anki_name} (已存在，跳过)")
            skipped += 1
        elif result:
            print(f"    ✓ {anki_name}")
            synced += 1
    
    # 同步 JS/CSS 库
    vendor_files = [
        "_renderer.js",
        "_marked.min.js",
        "_katex.min.js",
        "_katex.min.css",
        "_highlight.min.js",
        "_github.min.css",
        "_github-dark.min.css",

    ]

    katex_css_path = VENDOR_DIR / "katex.min.css"
    if katex_css_path.exists():
        katex_css = katex_css_path.read_text(encoding="utf-8", errors="ignore")
        if "fonts/KaTeX_" in katex_css:
            raise RuntimeError(
                "katex.min.css 仍引用 fonts/KaTeX_*，Anki 媒体库无法按这个相对路径加载字体。\n"
                f"{MEDIA_SETUP_HINT}"
            )

        referenced_katex_fonts = sorted(set(
            re.findall(r"url\(_(KaTeX_[^)'\"]+)\)", katex_css)
        ))
        for font_name in referenced_katex_fonts:
            vendor_files.append(f"_{font_name}")

    # Also sync any extra KaTeX font files already downloaded by sync_libs.sh.
    for font_path in sorted(VENDOR_DIR.glob("KaTeX_*")):
        if font_path.is_file():
            filename = f"_{font_path.name}"
            if filename not in vendor_files:
                vendor_files.append(filename)
    
    print("  JS/CSS 库:")
    for filename in vendor_files:
        # 特殊处理 renderer.js (位于 shared 目录)
        if filename == "_renderer.js":
            filepath = SHARED_DIR / "renderer.js"
            # renderer.js 经常变动，强制同步
            current_force = True
        else:
            # 移除前缀下划线匹配本地文件名
            local_name = filename[1:] if filename.startswith("_") else filename
            filepath = VENDOR_DIR / local_name
            current_force = force
            
        result = sync_media_file(filename, filepath, force=current_force)

        if result == "skipped":
            print(f"    ⏭ {filename} (已存在，跳过)")
            skipped += 1
        elif result:
            print(f"    ✓ {filename}")
            synced += 1
    
    print(f"\n  共同步 {synced} 个文件，跳过 {skipped} 个已存在文件")
    return synced


# ======================= 笔记类型管理 =======================
def read_template_file(path_str: str) -> str:
    """读取模板文件"""
    filepath = SCRIPT_DIR / "templates" / path_str
    if not filepath.exists():
        raise FileNotFoundError(f"模板文件不存在: {filepath}")
    return filepath.read_text(encoding="utf-8")


MODELS = [
    {
        "name": "Cloze-Modern",
        "type": "cloze",
        "fields": ["Text", "Extra"],
        "templates": [{"name": "Cloze", "front": "cloze/front.html", "back": "cloze/back.html"}],
        "css": "shared/style.css"
    },
    {
        "name": "Cloze-Modern-Typing",
        "type": "cloze",
        "fields": ["Text", "Extra"],
        "templates": [{"name": "Cloze Typing", "front": "cloze-type/front.html", "back": "cloze-type/back.html"}],
        "css": "shared/style.css"
    },
    {
        "name": "Basic-Modern",
        "type": "basic",  # basic (isCloze=False)
        "fields": ["Front", "Back"],
        "templates": [{"name": "Card 1", "front": "basic/front.html", "back": "basic/back.html"}],
        "css": "shared/style.css"
    },
    {
        "name": "Basic-Modern-Reversed",
        "type": "basic",
        "fields": ["Front", "Back"],
        "templates": [
            {"name": "Card 1", "front": "basic-reversed/card1-front.html", "back": "basic-reversed/card1-back.html"},
            {"name": "Card 2 (Reversed)", "front": "basic-reversed/card2-front.html", "back": "basic-reversed/card2-back.html"}
        ],
        "css": "shared/style.css"
    },
    {
        "name": "Basic-Modern-Typing",
        "type": "basic",
        "fields": ["Front", "Back"],
        "templates": [{"name": "Card 1", "front": "basic-type/front.html", "back": "basic-type/back.html"}],
        "css": "shared/style.css"
    }
]


def create_or_update_models():
    """创建或更新所有笔记类型"""
    existing_models = invoke("modelNames")
    
    for model in MODELS:
        print(f"\n📝 配置笔记类型: {model['name']}")
        
        css = read_template_file(model["css"])
        is_cloze = (model["type"] == "cloze")
        
        # 准备模板数据
        card_templates = []
        for tmpl in model["templates"]:
            card_templates.append({
                "Name": tmpl["name"],
                "Front": read_template_file(tmpl["front"]),
                "Back": read_template_file(tmpl["back"])
            })

        if model["name"] in existing_models:
            print(f"  更新现有笔记类型 ({model['name']})...")
            
            # 更新 CSS
            invoke("updateModelStyling", model={
                "name": model["name"],
                "css": css
            })
            print("    ✓ 样式已更新")
            
            # 更新模板 (遍历每个模板)
            tmpl_map = {}
            for ct in card_templates:
                tmpl_map[ct["Name"]] = {"Front": ct["Front"], "Back": ct["Back"]}
            
            invoke("updateModelTemplates", model={
                "name": model["name"],
                "templates": tmpl_map
            })
            print("    ✓ 模板已更新")
            
        else:
            print(f"  创建新笔记类型 ({model['name']})...")
            invoke("createModel", 
                   modelName=model["name"],
                   inOrderFields=model["fields"],
                   css=css,
                   isCloze=is_cloze,
                   cardTemplates=card_templates
            )
            print(f"    ✓ 笔记类型 '{model['name']}' 已创建")
    
    return True


# ======================= 示例卡片 =======================
EXAMPLE_CARDS = [
    {
        "deckName": "Default",
        "modelName": "Cloze-Modern",
        "fields": {
            "Text": """## 拉格朗日中值定理
**定理内容**：如果函数 $f(x)$ 满足：
1. 在闭区间 $[a, b]$ 上{{c1::连续}}
2. 在开区间 $(a, b)$ 内{{c2::可导}}

则至少存在一点 $\\xi \\in (a, b)$，使得：
$${{c3::f'(\\xi) = \\frac{f(b) - f(a)}{b - a}}}$$

> 💡 **几何意义**：曲线上至少存在一点，该点的{{c4::切线斜率}}等于两端点连线的斜率。
""",
            "Extra": "这是 **Cloze-Modern** 模板的示例。"
        },
        "tags": ["example", "cloze-modern"]
    },
    {
        "deckName": "Default",
        "modelName": "Cloze-Modern-Typing",
        "fields": {
            "Text": """## 单词拼写
Please type the meaning of "apple":
{{c1::apple}}
""",
            "Extra": "这是 **Cloze-Modern-Typing** 模板的示例。"
        },
        "tags": ["example", "cloze-typing"]
    },
    {
        "deckName": "Default",
        "modelName": "Basic-Modern",
        "fields": {
            "Front": """## 简答题
请简述 **Python** 中 `list` 和 `tuple` 的区别。
""",
            "Back": """1. **可变性**：`list` 是**可变的**，`tuple` 是**不可变的**。
2. **语法**：`list` 使用 `[]`，`tuple` 使用 `()`。
3. **性能**：`tuple` 通常比 `list` 略快，占用内存更少。

```python
x = [1, 2] # List
y = (1, 2) # Tuple
```
"""
        },
        "tags": ["example", "basic-modern"]
    },
    {
        "deckName": "Default",
        "modelName": "Basic-Modern-Reversed",
        "fields": {
            "Front": """## 词汇学习
**Apple** (noun)
""",
            "Back": """**苹果** 🍎

一种常见的水果，通常为红色、绿色或黄色。

> 例句: *An apple a day keeps the doctor away.*
"""
        },
        "tags": ["example", "basic-reversed"]
    },
    {
        "deckName": "Default",
        "modelName": "Basic-Modern-Typing",
        "fields": {
            "Front": "What comes after 'A'?",
            "Back": "B"
        },
        "tags": ["example", "basic-typing"]
    }
]


def create_example_cards():
    """创建示例卡片"""
    print("\n🃏 创建示例卡片...")
    created_count = 0
    
    for i, note in enumerate(EXAMPLE_CARDS):
        try:
            # 检查牌组是否存在
            decks = invoke("deckNames")
            if note["deckName"] not in decks:
                invoke("createDeck", deck=note["deckName"])

            # 创建笔记
            note_id = invoke("addNote", note={
                "deckName": note["deckName"],
                "modelName": note["modelName"],
                "fields": note["fields"],
                "tags": note.get("tags", []),
                "options": {
                    "allowDuplicate": False
                }
            })
            
            if note_id:
                print(f"  ✓ 示例卡片 {i+1} 已创建 ({note['modelName']})")
                created_count += 1
            else:
                print(f"  ⚠ 示例卡片 {i+1} 可能已存在")
                
        except Exception as e:
            if "duplicate" in str(e).lower():
                print(f"  ⚠ 示例卡片 {i+1} 已存在，跳过")
            else:
                print(f"  ✗ 创建失败: {e}")

    print(f"\n  共创建 {created_count} 张卡片")
    return created_count


# ======================= 主程序 =======================
def env_truthy(name: str) -> bool:
    """Return True when an environment variable asks for an opt-in behavior."""
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="同步 Anki 现代模板到 AnkiConnect。")
    parser.add_argument(
        "--pull",
        action="store_true",
        help="同步前执行 git pull。默认跳过，避免导入时隐式改动本地模板。",
    )
    parser.add_argument(
        "--force-media",
        action="store_true",
        help="强制重新上传已存在的媒体文件。",
    )
    return parser.parse_args(argv)


def try_git_pull(enabled: bool):
    """尝试拉取最新代码"""
    print("\n🔄 检查更新...")
    if not enabled:
        print("  ⏭ 已跳过 git pull（需要时使用 --pull 或设置 ANKI_TEMPLATE_GIT_PULL=1）")
        return

    try:
        result = subprocess.run(
            ["git", "pull"],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if "Already up to date" in output or "已是最新" in output:
                print("  ✓ 已是最新版本")
            else:
                print(f"  ✓ 已更新: {output.split(chr(10))[0]}")
        else:
            print(f"  ⚠ Git pull 失败，继续运行...")
    except FileNotFoundError:
        print("  ⚠ Git 未安装，跳过更新检查")
    except subprocess.TimeoutExpired:
        print("  ⚠ Git pull 超时，继续运行...")
    except Exception as e:
        print(f"  ⚠ 更新检查失败: {e}，继续运行...")


def main(argv=None):
    args = parse_args(argv)

    print("=" * 50)
    print("     Anki Connect 同步工具 v1.1")
    print("=" * 50)
    
    # 0. 按需拉取最新代码
    try_git_pull(args.pull or env_truthy("ANKI_TEMPLATE_GIT_PULL"))
    
    # 1. 检查连接
    if not check_connection():
        return 1

    try:
        # 2. 同步媒体文件
        sync_all_media(force=args.force_media)

        # 3. 配置笔记类型
        create_or_update_models()

        # 4. 创建示例卡片
        create_example_cards()
    except (FileNotFoundError, RuntimeError) as e:
        print(f"\n✗ 同步失败:\n{e}")
        return 1
    
    print("\n" + "=" * 50)
    print("     ✓ 同步完成！")
    print("=" * 50)
    print("\n请在 Anki 中查看笔记类型和示例卡片。")
    
    return 0


if __name__ == "__main__":
    exit(main())

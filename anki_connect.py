#!/usr/bin/env python3
"""
Anki Connect 同步脚本
功能：
1. 创建/更新 Cloze-Modern 笔记类型
2. 同步媒体文件（字体、JS/CSS 库）
3. 创建示例卡片
"""

import json
import urllib.request
import base64
import os
from pathlib import Path

# ======================= 配置 =======================
ANKI_CONNECT_URL = "http://127.0.0.1:8765"
MODEL_NAME = "Cloze-Modern"

# 目录配置
SCRIPT_DIR = Path(__file__).parent.resolve()
FONTS_DIR = SCRIPT_DIR / "fonts"
VENDOR_DIR = SCRIPT_DIR / "templates" / "vendor"
TEMPLATE_DIR = SCRIPT_DIR / "templates" / "cloze"


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
        print(f"  ⚠ 跳过不存在的文件: {filepath}")
        return False
    
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
    
    print("  JS/CSS 库:")
    for filename in vendor_files:
        # 特殊处理 renderer.js (位于 cloze 目录而非 vendor)
        if filename == "_renderer.js":
            filepath = SCRIPT_DIR / "templates" / "cloze" / "renderer.js"
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
def read_template_file(filename: str) -> str:
    """读取模板文件"""
    filepath = TEMPLATE_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"模板文件不存在: {filepath}")
    return filepath.read_text(encoding="utf-8")


def get_model_config():
    """获取笔记类型配置"""
    front_template = read_template_file("front.html")
    back_template = read_template_file("back.html")
    css = read_template_file("style.css")
    
    return {
        "modelName": MODEL_NAME,
        "inOrderFields": ["Text", "Extra"],
        "css": css,
        "isCloze": True,
        "cardTemplates": [
            {
                "Name": "Cloze",
                "Front": front_template,
                "Back": back_template,
            }
        ]
    }


def create_or_update_model():
    """创建或更新笔记类型"""
    print(f"\n📝 配置笔记类型: {MODEL_NAME}")
    
    existing_models = invoke("modelNames")
    model_config = get_model_config()
    
    if MODEL_NAME in existing_models:
        # 更新现有模型
        print("  更新现有笔记类型...")
        
        # 更新 CSS
        invoke("updateModelStyling", model={
            "name": MODEL_NAME,
            "css": model_config["css"]
        })
        print("    ✓ 样式已更新")
        
        # 更新模板
        invoke("updateModelTemplates", model={
            "name": MODEL_NAME,
            "templates": {
                "Cloze": {
                    "Front": model_config["cardTemplates"][0]["Front"],
                    "Back": model_config["cardTemplates"][0]["Back"],
                }
            }
        })
        print("    ✓ 模板已更新")
        
    else:
        # 创建新模型
        print("  创建新笔记类型...")
        invoke("createModel", **model_config)
        print(f"    ✓ 笔记类型 '{MODEL_NAME}' 已创建")
    
    return True


# ======================= 示例卡片 =======================
EXAMPLE_CARDS = [
    {
        "deckName": "Default",
        "modelName": MODEL_NAME,
        "fields": {
            "Text": """## 拉格朗日中值定理

**定理内容**：如果函数 $f(x)$ 满足：

1. 在闭区间 $[a, b]$ 上{{c1::连续}}
2. 在开区间 $(a, b)$ 内{{c2::可导}}

则至少存在一点 $\\xi \\in (a, b)$，使得：

$${{c3::f'(\\xi) = \\frac{f(b) - f(a)}{b - a}}}$$

> 💡 **几何意义**：曲线上至少存在一点，该点的{{c4::切线斜率}}等于两端点连线的斜率。
""",
            "Extra": "拉格朗日中值定理是微分学的基本定理之一，是罗尔定理的推广。"
        },
        "tags": ["数学", "微积分", "中值定理"]
    },
    {
        "deckName": "Default",
        "modelName": MODEL_NAME,
        "fields": {
            "Text": """## Python 装饰器

装饰器是一种{{c1::高阶函数}}，用于在不修改原函数代码的情况下扩展功能。

### 基本语法

```python
def {{c2::my_decorator}}(func):
    def wrapper(*args, **kwargs):
        print("函数调用前")
        result = {{c3::func(*args, **kwargs)}}
        print("函数调用后")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

# 调用
say_hello("World")
```

### 输出结果

```
函数调用前
Hello, World!
函数调用后
```

> 📌 `@decorator` 语法糖等价于 `func = decorator(func)`
""",
            "Extra": "装饰器是 Python 中实现 AOP (面向切面编程) 的常用方式。"
        },
        "tags": ["编程", "Python", "装饰器"]
    }
]


def create_example_cards():
    """创建示例卡片"""
    print("\n🃏 创建示例卡片...")
    
    created = 0
    for i, card in enumerate(EXAMPLE_CARDS, 1):
        try:
            # 检查牌组是否存在
            decks = invoke("deckNames")
            if card["deckName"] not in decks:
                invoke("createDeck", deck=card["deckName"])
            
            # 创建笔记
            note_id = invoke("addNote", note={
                "deckName": card["deckName"],
                "modelName": card["modelName"],
                "fields": card["fields"],
                "tags": card.get("tags", []),
                "options": {
                    "allowDuplicate": False
                }
            })
            
            if note_id:
                print(f"  ✓ 示例卡片 {i} 已创建 (ID: {note_id})")
                created += 1
            else:
                print(f"  ⚠ 示例卡片 {i} 可能已存在")
                
        except Exception as e:
            if "duplicate" in str(e).lower():
                print(f"  ⚠ 示例卡片 {i} 已存在，跳过")
            else:
                print(f"  ✗ 示例卡片 {i} 创建失败: {e}")
    
    print(f"\n  共创建 {created} 张卡片")
    return created


# ======================= 主程序 =======================
def main():
    print("=" * 50)
    print("     Anki Connect 同步工具 v1.0")
    print("=" * 50)
    
    # 1. 检查连接
    if not check_connection():
        return 1
    
    # 2. 同步媒体文件
    try:
        sync_all_media()
    except Exception as e:
        print(f"✗ 媒体同步失败: {e}")
        return 1
    
    # 3. 创建/更新笔记类型
    try:
        create_or_update_model()
    except Exception as e:
        print(f"✗ 笔记类型配置失败: {e}")
        return 1
    
    # 4. 创建示例卡片
    try:
        create_example_cards()
    except Exception as e:
        print(f"✗ 示例卡片创建失败: {e}")
        return 1
    
    print("\n" + "=" * 50)
    print("     ✓ 同步完成！")
    print("=" * 50)
    print(f"\n请在 Anki 中查看笔记类型 '{MODEL_NAME}' 和示例卡片。")
    
    return 0


if __name__ == "__main__":
    exit(main())

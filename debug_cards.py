#!/usr/bin/env python3
"""调试：尝试直接更新模板内容"""

import json
import urllib.request
from pathlib import Path

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATE_DIR = SCRIPT_DIR / "templates" / "cloze"

def invoke(action, **params):
    request_json = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode("utf-8")
    
    response = urllib.request.urlopen(
        urllib.request.Request(ANKI_CONNECT_URL, request_json),
        timeout=30
    )
    return json.loads(response.read().decode("utf-8"))

# 读取新模板
front = (TEMPLATE_DIR / "front.html").read_text()
back = (TEMPLATE_DIR / "back.html").read_text()

print(f"Front 模板长度: {len(front)} 字符")
print(f"Back 模板长度: {len(back)} 字符")

# 检查模板中是否包含 cloze 字段
print(f"\nFront 包含 {{{{cloze:Text}}}}: {'{{cloze:Text}}' in front}")
print(f"Back 包含 {{{{cloze:Text}}}}: {'{{cloze:Text}}' in back}")

# 尝试更新
print("\n尝试更新模板...")
try:
    result = invoke("updateModelTemplates", model={
        "name": "Cloze-Modern",
        "templates": {
            "Cloze": {
                "Front": front,
                "Back": back,
            }
        }
    })
    print(f"结果: {result}")
except Exception as e:
    print(f"错误: {e}")

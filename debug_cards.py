#!/usr/bin/env python3
"""调试脚本：获取卡片完整渲染HTML"""

import json
import urllib.request

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

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

# 获取第一张卡片的完整渲染
result = invoke("findCards", query="note:Cloze-Modern")
card_ids = result.get("result", [])

if card_ids:
    result = invoke("cardsInfo", cards=[card_ids[0]])
    card = result.get("result", [])[0]
    
    question = card.get('question', '')
    
    # 检查关键元素
    print("=" * 60)
    print("模板结构检查")
    print("=" * 60)
    
    checks = [
        ("隐藏内容 div", 'id="raw-content"' in question),
        ("渲染内容 div", 'id="rendered-content"' in question),
        ("marked.js 引用", '_marked.min.js' in question),
        ("katex.js 引用", '_katex.min.js' in question),
        ("highlight.js 引用", '_highlight.min.js' in question),
        ("katex.css 引用", '_katex.min.css' in question),
    ]
    
    for name, exists in checks:
        status = "✓" if exists else "✗"
        print(f"  {status} {name}")
    
    # 提取 raw-content 的内容
    import re
    match = re.search(r'id="raw-content"[^>]*>(.*?)</div>', question, re.DOTALL)
    if match:
        print("\n" + "=" * 60)
        print("raw-content 内容 (前500字符)")
        print("=" * 60)
        print(match.group(1)[:500])
    
    # 检查脚本部分
    print("\n" + "=" * 60)
    print("脚本引用检查")
    print("=" * 60)
    script_refs = re.findall(r'<script[^>]*src="([^"]+)"', question)
    for ref in script_refs:
        print(f"  引用: {ref}")
    
    link_refs = re.findall(r'<link[^>]*href="([^"]+)"', question)
    for ref in link_refs:
        print(f"  样式: {ref}")

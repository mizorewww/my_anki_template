#!/usr/bin/env bash

# ================= 配置区域 =================
# 设置颜色变量
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 目录配置
VENDOR_DIR="./templates/vendor"

# 版本配置
MARKED_VERSION="15.0.4"
KATEX_VERSION="0.16.21"
HLJS_VERSION="11.11.1"

# URL 配置
MARKED_URL="https://cdn.jsdelivr.net/npm/marked@${MARKED_VERSION}/marked.min.js"
KATEX_JS_URL="https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.js"
KATEX_CSS_URL="https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/katex.min.css"
HLJS_JS_URL="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@${HLJS_VERSION}/build/highlight.min.js"
HLJS_CSS_LIGHT_URL="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@${HLJS_VERSION}/build/styles/github.min.css"
HLJS_CSS_DARK_URL="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@${HLJS_VERSION}/build/styles/github-dark.min.css"

# 重试配置
MAX_RETRIES=3

# ================= 工具函数 =================

# 打印信息头
info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# 打印成功信息
success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# 打印警告/重试信息
warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 打印错误并退出
error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# 带有重试机制的下载函数
download_file() {
    local url=$1
    local output=$2
    local count=0
    local ret=1

    while [ $ret -ne 0 ] && [ $count -lt $MAX_RETRIES ]; do
        if [ $count -gt 0 ]; then
            warn "下载失败，正在尝试第 $count/$MAX_RETRIES 次重试..."
            sleep 2
        fi
        
        info "正在下载: $(basename "$output")"
        curl -sL "$url" -o "$output"
        ret=$?
        
        ((count++))
    done

    if [ $ret -ne 0 ]; then
        error "无法下载 $url，请检查网络连接。"
    else
        success "下载完成: $(basename "$output")"
    fi
}

# ================= 主逻辑 =================

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}       第三方库自动下载脚本 v1.0        ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. 初始化环境
info "初始化目录..."
mkdir -p "$VENDOR_DIR"

# 2. 下载 marked.js
echo ""
echo -e "${BLUE}>>> 处理任务 1/3: marked.js (Markdown 解析器)${NC}"
download_file "$MARKED_URL" "$VENDOR_DIR/marked.min.js"

# 3. 下载 KaTeX
echo ""
echo -e "${BLUE}>>> 处理任务 2/3: KaTeX (LaTeX 渲染)${NC}"
download_file "$KATEX_JS_URL" "$VENDOR_DIR/katex.min.js"
download_file "$KATEX_CSS_URL" "$VENDOR_DIR/katex.min.css"

# 4. 下载 Highlight.js
echo ""
echo -e "${BLUE}>>> 处理任务 3/3: Highlight.js (代码高亮)${NC}"
download_file "$HLJS_JS_URL" "$VENDOR_DIR/highlight.min.js"
download_file "$HLJS_CSS_LIGHT_URL" "$VENDOR_DIR/github.min.css"
download_file "$HLJS_CSS_DARK_URL" "$VENDOR_DIR/github-dark.min.css"

# 5. 完成
echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}   所有库文件已准备就绪！存放于: $VENDOR_DIR   ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 6. 显示下载的文件
echo ""
info "已下载的文件:"
ls -lh "$VENDOR_DIR"

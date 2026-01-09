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
TEMP_DIR="./temp"
FONT_DIR="./fonts"

# URL 配置
MAPLE_URL="https://github.com/subframe7536/maple-font/releases/download/v7.9/MapleMono-NF-CN.zip"
LXGW_URL="https://github.com/lxgw/LxgwWenKai/archive/refs/heads/main.zip"

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

# 旋转加载动画 (PID为参数)
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    echo -ne "  "
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
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
        
        # wget 参数说明:
        # -q: 安静模式 (不输出日志)
        # --show-progress: 强制显示进度条 (解决-q不仅显示进度条的问题)
        # --progress=bar:force:noscroll: 美观的进度条样式
        info "正在下载: $(basename "$output")"
        wget -q --show-progress --progress=bar:force:noscroll "$url" -O "$output"
        ret=$?
        
        ((count++))
    done

    if [ $ret -ne 0 ]; then
        error "无法下载 $url，请检查网络连接。"
    else
        success "下载完成。"
    fi
}

# ================= 主逻辑 =================

# 1. 初始化环境
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}       字体自动下载与安装脚本 v2.0       ${NC}"
echo -e "${BLUE}=========================================${NC}"

info "初始化目录..."
mkdir -p "$TEMP_DIR"
mkdir -p "$FONT_DIR"

# 2. 处理 Maple Mono 字体
echo ""
echo -e "${BLUE}>>> 处理任务 1/2: Maple Mono NF CN${NC}"
download_file "$MAPLE_URL" "$TEMP_DIR/maple-font.zip"

info "正在解压 Maple Font..."
# 后台解压，前台显示动画
unzip -q -o "$TEMP_DIR/maple-font.zip" -d "$FONT_DIR" &
spinner $!
success "Maple Font 解压完成"

# 3. 处理 LXGW WenKai 字体
echo ""
echo -e "${BLUE}>>> 处理任务 2/2: LXGW WenKai (霞鹜文楷)${NC}"
download_file "$LXGW_URL" "$TEMP_DIR/lxgw-wenkai.zip"

info "正在解压 LXGW WenKai (文件较大，请稍候)..."
unzip -q -o "$TEMP_DIR/lxgw-wenkai.zip" -d "$TEMP_DIR/lxgw-wenkai" &
spinner $!
success "解压完成，正在移动字体文件..."

# 移动文件 (增加判断，防止目录结构变化导致错误)
if [ -d "$TEMP_DIR/lxgw-wenkai/LxgwWenKai-main/fonts/TTF" ]; then
    cp -r "$TEMP_DIR/lxgw-wenkai/LxgwWenKai-main/fonts/TTF/"* "$FONT_DIR/"
    success "LXGW WenKai 文件移动完成"
else
    error "找不到解压后的 TTF 目录，请检查源文件结构。"
fi

# 4. 清理工作
echo ""
info "执行清理工作..."
rm -rf "$TEMP_DIR"

# 注意：这里修改了原本的 find 逻辑，限定在 $FONT_DIR 目录内删除
# 防止误删脚本所在目录的其他文件
info "移除 $FONT_DIR 下非 .ttf 文件..."
find "$FONT_DIR" -type f ! -name "*.ttf" -delete

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}   所有字体已准备就绪！存放于: $FONT_DIR   ${NC}"
echo -e "${BLUE}=========================================${NC}"
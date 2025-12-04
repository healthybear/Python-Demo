#!/bin/bash
# 修复 macOS SSL 证书问题的脚本

echo "正在修复 SSL 证书问题..."

# 方法 1: 尝试运行 Python 的证书安装脚本
if [ -f "/Applications/Python 3.12/Install Certificates.command" ]; then
    echo "找到证书安装脚本，正在运行..."
    "/Applications/Python 3.12/Install Certificates.command"
elif [ -f "/Applications/Python 3.11/Install Certificates.command" ]; then
    echo "找到 Python 3.11 证书安装脚本，正在运行..."
    "/Applications/Python 3.11/Install Certificates.command"
else
    echo "未找到证书安装脚本，尝试其他方法..."
    
    # 方法 2: 使用 pip 安装证书
    echo "使用 pip 安装/更新 certifi..."
    python3 -m pip install --upgrade certifi
    
    # 方法 3: 运行 Python 脚本来安装证书
    echo "运行 Python 证书安装脚本..."
    python3 << 'EOF'
import ssl
import certifi
import os

# 设置环境变量
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

print(f"SSL 证书路径已设置为: {certifi.where()}")
print("请将以下内容添加到您的 ~/.zshrc 或 ~/.bash_profile:")
print(f"export SSL_CERT_FILE={certifi.where()}")
print(f"export REQUESTS_CA_BUNDLE={certifi.where()}")
EOF
fi

echo ""
echo "修复完成！"
echo "如果问题仍然存在，请："
echo "1. 重启终端"
echo "2. 或运行: export HF_ENDPOINT=https://hf-mirror.com 使用镜像源"


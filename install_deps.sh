#!/bin/bash
# 使用国内镜像源安装依赖

source venv/bin/activate

echo "开始安装依赖，使用清华大学镜像源..."
echo "这可能需要几分钟时间，请耐心等待..."

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo ""
echo "安装完成！"


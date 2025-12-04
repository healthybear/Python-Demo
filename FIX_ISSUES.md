# 问题修复指南

## 已修复的问题

### 1. NumPy 版本兼容性问题 ✅

**问题**：NumPy 2.3.3 与使用 NumPy 1.x 编译的模块不兼容

**解决方案**：
- 已将 `requirements.txt` 中的 `numpy==2.3.3` 改为 `numpy<2.0`
- 已重新安装 NumPy 1.26.4

**验证**：
```bash
source .venv/bin/activate  # 或 source venv/bin/activate
pip list | grep numpy
```

### 2. SSL 证书验证失败 ⚠️

**问题**：无法从 HuggingFace 下载模型，SSL 证书验证失败

**已实施的解决方案**：
1. ✅ 配置了 HuggingFace 镜像源（`https://hf-mirror.com`）
2. ✅ 设置了 SSL 证书环境变量
3. ✅ 添加了错误处理和提示信息

**如果问题仍然存在，请尝试以下方法**：

#### 方法 1：运行 SSL 修复脚本（推荐）
```bash
./fix_ssl.sh
```

#### 方法 2：手动安装证书
```bash
# 如果使用 Homebrew 安装的 Python
/Applications/Python\ 3.12/Install\ Certificates.command

# 或者更新 certifi
pip install --upgrade certifi
```

#### 方法 3：使用环境变量（临时解决）
```bash
export HF_ENDPOINT=https://hf-mirror.com
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$(python3 -c "import certifi; print(certifi.where())")
```

#### 方法 4：将环境变量添加到 shell 配置
将以下内容添加到 `~/.zshrc` 或 `~/.bash_profile`：
```bash
export HF_ENDPOINT=https://hf-mirror.com
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$(python3 -c "import certifi; print(certifi.where())")
```

然后运行：
```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

## 重新安装依赖

如果修改了 `requirements.txt`，请重新安装依赖：

```bash
source .venv/bin/activate  # 或 source venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 测试运行

修复后，尝试运行：

```bash
python first-rag/first-rag.py
```

如果仍有问题，请检查：
1. 网络连接是否正常
2. 环境变量是否正确设置
3. 虚拟环境是否激活


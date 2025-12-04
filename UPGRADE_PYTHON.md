# Python 升级指南

## 当前状态
- 当前 Python 版本：3.9.6
- 需要版本：Python 3.10 或更高

## 方案 1：使用 Homebrew（推荐）

### 1. 安装 Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 安装 Python 3.12
```bash
brew install python@3.12
```

### 3. 验证安装
```bash
python3.12 --version
```

### 4. 安装项目依赖
```bash
python3.12 -m pip install -r requirements.txt
```

## 方案 2：从 python.org 下载

1. 访问：https://www.python.org/downloads/
2. 下载 Python 3.10+ 的 macOS 安装包
3. 运行安装程序
4. 安装完成后使用新版本安装依赖

## 方案 3：使用 pyenv（管理多个版本）

### 1. 安装 pyenv
```bash
brew install pyenv
```

### 2. 配置 shell（添加到 ~/.zshrc）
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 安装 Python 3.12
```bash
pyenv install 3.12.0
pyenv global 3.12.0
```

### 4. 验证
```bash
python --version
```

## 推荐方案
建议使用 **方案 1（Homebrew）**，因为：
- 安装简单
- 易于管理
- 更新方便


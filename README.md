# 热处理知识自动化收集整理系统


## 开始

本指南将帮助你在本地机器上为开发和测试目的设置项目。请按照下面的步骤操作。

### 前提条件

在开始之前，确保你的计算机上已经安装了 Python。本项目支持 Python 3.11 版本。

### 设置虚拟环境

为了保持你的开发环境整洁和一致，推荐使用 Python 的虚拟环境。以下步骤将指导你创建和激活一个虚拟环境：

#### 对于 macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

#### 对于 Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

激活虚拟环境后，你的命令行提示符将显示虚拟环境的名称，表明虚拟环境已被激活。

### 安装依赖

项目的依赖在 `apps/requirements.txt` 文件中定义。安装这些依赖非常简单，只需运行以下命令：

```bash
pip install -r requirements.txt
```

这将安装所有必要的库和包，以便项目能够运行。

## 运行项目

详细说明如何运行项目的各个部分，例如运行脚本、服务器或其他组件。

```bash
python your_script.py
```
# pyenv-doctor

`pyenv-doctor` 是一个最小可运行的 Python 命令行工具。

它会扫描当前目录，并根据几个常见文件判断这里看起来是不是一个 Python 项目。

这个版本只做最基础的识别，适合新手阅读和继续扩展。

## 项目简介

当前版本会检查下面这些文件是否存在：

- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`

如果检测到任意一个文件，就输出：

`这看起来是一个 Python 项目`

如果一个都没有检测到，就输出：

`未发现明显的 Python 项目特征`

## 项目结构

```text
pyenv-doctor/
├─ .gitignore
├─ README.md
├─ requirements.txt
└─ main.py
```

## 安装方法

### 1. 准备 Python 3.11

先确认本机已经安装 Python 3.11：

```powershell
py -3.11 --version
```

### 2. 进入项目目录

```powershell
cd pyenv-doctor
```

### 3. 安装依赖

这个最小版本只使用 Python 标准库，没有第三方依赖。

你仍然可以执行下面这条命令，保持项目使用方式统一：

```powershell
py -3.11 -m pip install -r requirements.txt
```

## 运行方法

当前最小版本直接运行 `main.py`：

```powershell
py -3.11 main.py
```

程序内部的命令名已经设置为 `pyenv-doctor`，后续如果需要，再把它做成真正可安装的命令即可。

## 示例输出

### 示例 1：当前目录像是 Python 项目

```text
扫描目录: C:\demo\my-project

检查结果:
- requirements.txt: 已发现
- pyproject.toml: 未发现
- setup.py: 未发现
- setup.cfg: 未发现

结论: 这看起来是一个 Python 项目
原因: 检测到 requirements.txt
```

### 示例 2：当前目录不像 Python 项目

```text
扫描目录: C:\demo\empty-folder

检查结果:
- requirements.txt: 未发现
- pyproject.toml: 未发现
- setup.py: 未发现
- setup.cfg: 未发现

结论: 未发现明显的 Python 项目特征
说明: 当前目录里没有找到常见的 Python 项目配置文件。
```

## 后续路线图

- 支持扫描指定目录，而不只是当前目录
- 增加退出状态码，方便脚本调用
- 增加单元测试
- 支持输出 JSON 结果
- 增加更多常见 Python 项目特征文件

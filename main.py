"""pyenv-doctor 的最小命令行入口。"""

import argparse
from pathlib import Path


# 这些文件是本次 MVP 用来判断 Python 项目的最基础特征。
PROJECT_MARKER_FILES = [
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
]


def build_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器。"""
    # 这里先不添加复杂参数，只保留最小可运行版本。
    return argparse.ArgumentParser(
        prog="pyenv-doctor",
        description="扫描当前目录，判断这里看起来是不是一个 Python 项目。",
    )


def find_marker_files(scan_path: Path) -> list[str]:
    """返回当前目录里检测到的特征文件。"""
    found_files: list[str] = []

    # 逐个检查文件是否存在，逻辑直观，方便新手阅读。
    for file_name in PROJECT_MARKER_FILES:
        if (scan_path / file_name).is_file():
            found_files.append(file_name)

    return found_files


def print_result(scan_path: Path, found_files: list[str]) -> None:
    """把检测结果打印成清晰、易读的文本。"""
    print(f"扫描目录: {scan_path}")
    print()
    print("检查结果:")

    # 按固定顺序输出每个文件的检查状态，方便逐项查看。
    for file_name in PROJECT_MARKER_FILES:
        status = "已发现" if file_name in found_files else "未发现"
        print(f"- {file_name}: {status}")

    print()

    # 只要找到任意一个特征文件，就给出正向判断。
    if found_files:
        print("结论: 这看起来是一个 Python 项目")
        print(f"原因: 检测到 {', '.join(found_files)}")
    else:
        print("结论: 未发现明显的 Python 项目特征")
        print("说明: 当前目录里没有找到常见的 Python 项目配置文件。")


def main() -> None:
    """执行主程序。"""
    # 先解析参数，保证后续扩展时入口结构保持稳定。
    parser = build_parser()
    parser.parse_args()

    # 本次需求只扫描当前工作目录。
    scan_path = Path.cwd()
    found_files = find_marker_files(scan_path)
    print_result(scan_path, found_files)


if __name__ == "__main__":
    # 允许直接通过 `python main.py` 运行这个工具。
    main()

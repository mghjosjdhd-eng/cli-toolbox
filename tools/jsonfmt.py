"""JSON 格式化工具"""

import json
import os
import tempfile
from pathlib import Path


def run(args):
    """主入口"""
    file_path = Path(args.file)

    if not file_path.is_file():
        print(f"错误：文件 '{args.file}' 不存在")
        return

    # 读取 JSON
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        return
    except Exception as e:
        print(f"读取文件出错：{e}")
        return

    # 格式化
    if args.compact:
        indent = None
        separators = (",", ":")
    else:
        indent = args.indent
        separators = None

    formatted = json.dumps(data, indent=indent, separators=separators, ensure_ascii=False)

    if args.in_place:
        # 原子写入：先写临时文件，再用 os.replace 原子替换，防止写一半断电丢数据
        tmp_fd, tmp_path = tempfile.mkstemp(
            suffix=".json", prefix="jsonfmt_", dir=file_path.parent
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(formatted)
                f.write("\n")
            os.replace(tmp_path, file_path)  # Windows 上也保证原子替换
        except Exception:
            os.unlink(tmp_path)
            raise

        print(f"已格式化并写回：{file_path}")
    else:
        print(formatted)

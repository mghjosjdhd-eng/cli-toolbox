"""CLI 工具箱 — 主入口"""

import argparse
import sys

from tools import renamer, jsonfmt, stats, toc


def main():
    parser = argparse.ArgumentParser(
        prog="toolbox",
        description="CLI 工具箱：文件重命名、JSON 格式化、文本统计、Markdown 目录生成",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # ---- rename ----
    p_rename = subparsers.add_parser("rename", help="批量重命名文件")
    p_rename.add_argument("directory", help="目标目录路径")
    p_rename.add_argument("--prefix", help="给文件名加前缀")
    p_rename.add_argument("--suffix", help="给文件名加后缀（在扩展名之前）")
    p_rename.add_argument("--replace", help="要替换的文字")
    p_rename.add_argument("--with", dest="replace_with", help="替换成什么文字")
    p_rename.add_argument("--number", nargs=2, metavar=("NAME", "START"),
                          help="按序号重命名，如: --number photo_ 1")
    p_rename.add_argument("--yes", "-y", action="store_true", help="跳过确认，直接执行")

    # ---- jsonfmt ----
    p_json = subparsers.add_parser("jsonfmt", help="JSON 格式化")
    p_json.add_argument("file", help="JSON 文件路径")
    p_json.add_argument("--indent", type=int, default=2, help="缩进空格数（默认 2）")
    p_json.add_argument("--compact", action="store_true", help="压缩成一行")
    p_json.add_argument("--in-place", "-i", action="store_true", help="写回原文件")

    # ---- stats ----
    p_stats = subparsers.add_parser("stats", help="文本统计")
    p_stats.add_argument("files", nargs="+", help="要统计的文件（支持通配符）")

    # ---- toc ----
    p_toc = subparsers.add_parser("toc", help="生成 Markdown 目录")
    p_toc.add_argument("file", help="Markdown 文件路径")

    # 解析参数
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # 分发到对应工具
    if args.command == "rename":
        renamer.run(args)
    elif args.command == "jsonfmt":
        jsonfmt.run(args)
    elif args.command == "stats":
        stats.run(args)
    elif args.command == "toc":
        toc.run(args)


if __name__ == "__main__":
    main()

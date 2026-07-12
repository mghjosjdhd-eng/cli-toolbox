"""文本统计工具 — 类似 wc 命令"""

import glob
from pathlib import Path


def count_file(file_path):
    """统计单个文件的行数、单词数、字符数、字节数"""
    try:
        # 用 read_bytes 获取真实字节数，避免 read_text 的换行符转换
        raw_bytes = file_path.read_bytes()
        # 用 read_text 获取文本内容来统计行和词
        content = raw_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return None, str(e)

    lines = content.count("\n")
    # 如果文件末尾没有换行符，最后一行也要算上
    if content and not content.endswith("\n"):
        lines += 1

    words = len(content.split())
    chars = len(content)
    byte_count = len(raw_bytes)  # 真实文件字节数

    return (lines, words, chars, byte_count), None


def run(args):
    """主入口"""
    # 处理通配符展开（Windows 下 argparse 不会自动展开）
    all_files = []
    for pattern in args.files:
        matched = glob.glob(pattern)
        if matched:
            all_files.extend(matched)
        else:
            all_files.append(pattern)

    total_lines = 0
    total_words = 0
    total_chars = 0
    total_bytes = 0
    file_count = 0

    for file_path_str in all_files:
        file_path = Path(file_path_str)

        if not file_path.is_file():
            print(f"⚠ 跳过（不是文件）：{file_path_str}")
            continue

        result, error = count_file(file_path)
        if error:
            print(f"⚠ 读取出错 {file_path_str}：{error}")
            continue

        lines, words, chars, byte_count = result
        print(f"{lines:>8} {words:>8} {chars:>8} {byte_count:>8}  {file_path_str}")

        total_lines += lines
        total_words += words
        total_chars += chars
        total_bytes += byte_count
        file_count += 1

    # 多个文件时显示合计
    if file_count > 1:
        print(f"{total_lines:>8} {total_words:>8} {total_chars:>8} {total_bytes:>8}  合计")

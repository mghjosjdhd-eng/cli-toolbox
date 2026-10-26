"""词频统计工具 — 统计文件里出现次数最多的词（Top N）"""

import re
from pathlib import Path

# 分词规则：英文单词/数字整体算一个词；每个汉字单独算一个单位（中文无空格，不依赖分词库）
TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[一-鿿]")


def count_words(file_path):
    """统计单个文件的词频，返回 ((词, 次数) 列表按次数降序, None) 或 (None, 错误信息)"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return None, str(e)

    counts = {}
    for token in TOKEN_RE.findall(content):
        # 英文统一小写，让 "Hello" 和 "hello" 合并计数；汉字不受影响
        key = token.lower()
        counts[key] = counts.get(key, 0) + 1

    # 按次数降序排列，次数相同按词排序，保证输出稳定
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered, None


def run(args):
    """主入口"""
    file_path = Path(args.file)

    if not file_path.is_file():
        print(f"⚠ 跳过（不是文件）：{file_path}")
        return

    result, error = count_words(file_path)
    if error:
        print(f"⚠ 读取出错 {file_path}：{error}")
        return

    top = args.top if args.top > 0 else 10
    for word, count in result[:top]:
        print(f"{count:>8}  {word}")

    if not result:
        print("（没有统计到任何词）")

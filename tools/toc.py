"""Markdown 目录生成工具"""

import re
import tempfile
import os
from pathlib import Path

# 匹配 Markdown 标题的正则（# 开头，支持 1-6 级）
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# 匹配围栏代码块（支持 ``` 和 ~~~ 两种围栏）
CODE_BLOCK_PATTERN = re.compile(r"(?:```|~~~)[\s\S]*?(?:```|~~~)", re.MULTILINE)

# 预编译的锚点处理正则
NON_WORD_PATTERN = re.compile(r"[^\w\s\-]")
SPACE_PATTERN = re.compile(r"\s+")
FIRST_HEADING_PATTERN = re.compile(r"^#\s+.*$", re.MULTILINE)

# 目录标记：插入到这个标记下面
TOC_MARKER = "<!-- toc -->"


def generate_toc(text):
    """从 Markdown 文本中提取标题，生成目录列表（跳过代码块内的 #）"""
    # 先把代码块去掉，避免把代码里的 # 当成标题
    clean_text = CODE_BLOCK_PATTERN.sub("", text)

    headings = HEADING_PATTERN.findall(clean_text)
    if not headings:
        return None

    # 记录已出现的锚点，处理重复标题（加 -1, -2 后缀）
    seen_anchors = {}

    lines = []
    for hashes, title in headings:
        level = len(hashes)  # 1-6
        indent = "  " * (level - 1)

        # 生成锚点链接（和 GitHub 风格一致）
        anchor = title.lower()
        anchor = NON_WORD_PATTERN.sub("", anchor)  # 去掉标点
        anchor = SPACE_PATTERN.sub("-", anchor)     # 空格换横线

        # 处理重复标题：给锚点加 -1, -2 后缀
        base_anchor = anchor
        if anchor in seen_anchors:
            seen_anchors[anchor] += 1
            anchor = f"{base_anchor}-{seen_anchors[anchor]}"
        else:
            seen_anchors[anchor] = 0

        lines.append(f"{indent}- [{title}](#{anchor})")

    return "\n".join(lines)


def insert_toc(text, toc):
    """把目录插入到 Markdown 文本中"""
    toc_block = f"{TOC_MARKER}\n\n{toc}"

    if TOC_MARKER in text:
        # 替换已有的 toc 标记区域
        return text.replace(TOC_MARKER, toc_block, 1)
    else:
        # 没有标记时：找到第一个 # 标题，插在它后面
        first_heading = FIRST_HEADING_PATTERN.search(text)
        if first_heading:
            pos = first_heading.end()
            return "".join([text[:pos], "\n\n", toc_block, "\n", text[pos:]])
        else:
            return toc_block + "\n" + text


def run(args):
    """主入口"""
    file_path = Path(args.file)

    if not file_path.is_file():
        print(f"错误：文件 '{args.file}' 不存在")
        return

    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"读取文件出错：{e}")
        return

    toc = generate_toc(text)
    if toc is None:
        print("文件中没有找到标题（# 开头的行）")
        return

    new_text = insert_toc(text, toc)

    # 原子写入：先写临时文件，再替换，避免写一半断电丢失数据
    tmp_fd, tmp_path = tempfile.mkstemp(
        suffix=".md", prefix="toc_", dir=file_path.parent
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.write(new_text)
        os.replace(tmp_path, file_path)  # Windows 上也保证原子替换
    except Exception:
        os.unlink(tmp_path)  # 出错了清理临时文件
        raise

    print(f"已生成目录并写入：{file_path}")
    print(f"\n生成的目录：\n{toc}")

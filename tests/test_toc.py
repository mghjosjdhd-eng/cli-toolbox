"""测试 toc 工具"""

from argparse import Namespace
import pytest
from tools.toc import generate_toc, insert_toc, TOC_MARKER, run




def test_generate_toc():
    """测试目录生成"""
    md = """# 第一章

一些内容

## 第一节

更多内容

### 小标题

## 第二节

# 第二章
"""
    toc = generate_toc(md)
    assert toc is not None
    assert "[第一章](#第一章)" in toc
    assert "  - [第一节](#第一节)" in toc  # 二级标题缩进
    assert "    - [小标题](#小标题)" in toc  # 三级标题更多缩进
    assert "  - [第二节](#第二节)" in toc
    assert "[第二章](#第二章)" in toc


def test_generate_toc_no_headings():
    """测试没有标题的文本"""
    md = """这是一段普通的文字。

没有任何 Markdown 标题。
"""
    toc = generate_toc(md)
    assert toc is None


def test_generate_toc_anchor():
    """测试锚点生成 — 特殊字符和空格"""
    md = "# Hello World! 你好"
    toc = generate_toc(md)
    assert toc == "- [Hello World! 你好](#hello-world-你好)"


def test_insert_toc_with_marker():
    """测试插入目录到已有标记处"""
    md = f"""# 标题

{TOC_MARKER}

正文内容
"""
    toc = "- [标题](#标题)"
    result = insert_toc(md, toc)
    assert TOC_MARKER in result
    assert toc in result
    # 标记应该还在
    assert result.count(TOC_MARKER) == 1


def test_insert_toc_without_marker():
    """测试在没有标记的文件中插入目录"""
    md = """# 标题

正文内容
"""
    toc = "- [标题](#标题)"
    result = insert_toc(md, toc)
    assert TOC_MARKER in result
    assert toc in result


def test_run(tmp_path):
    """测试完整 run 流程"""
    file = tmp_path / "doc.md"
    file.write_text("""# 简介

<!-- toc -->

## 安装

## 使用
""", encoding="utf-8")

    args = Namespace(file=str(file))
    run(args)

    result = file.read_text(encoding="utf-8")
    assert "[简介](#简介)" in result
    assert "[安装](#安装)" in result
    assert "[使用](#使用)" in result

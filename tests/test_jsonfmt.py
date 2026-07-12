"""测试 jsonfmt 工具"""

import json
from argparse import Namespace
import pytest
from tools.jsonfmt import run




def test_jsonfmt_indent(tmp_path, capsys):
    """测试美化输出"""
    file = tmp_path / "data.json"
    file.write_text('{"name":"张三","age":25}', encoding="utf-8")

    args = Namespace(
        file=str(file),
        indent=2,
        compact=False,
        in_place=False,
    )
    run(args)

    captured = capsys.readouterr()
    output = json.loads(captured.out)  # 应该能解析回来
    assert output == {"name": "张三", "age": 25}


def test_jsonfmt_compact(tmp_path, capsys):
    """测试压缩输出"""
    file = tmp_path / "data.json"
    file.write_text('{\n  "x": 1\n}', encoding="utf-8")

    args = Namespace(
        file=str(file),
        indent=2,
        compact=True,
        in_place=False,
    )
    run(args)

    captured = capsys.readouterr()
    # 压缩后应该没有换行
    assert "\n" not in captured.out.strip()


def test_jsonfmt_in_place(tmp_path):
    """测试写回原文件"""
    file = tmp_path / "data.json"
    file.write_text('{"a":1}', encoding="utf-8")

    args = Namespace(
        file=str(file),
        indent=4,
        compact=False,
        in_place=True,
    )
    run(args)

    result = file.read_text(encoding="utf-8")
    assert "    " in result  # 4 空格缩进
    assert json.loads(result) == {"a": 1}


def test_jsonfmt_invalid_json(tmp_path, capsys):
    """测试无效 JSON"""
    file = tmp_path / "bad.json"
    file.write_text("这不是 JSON", encoding="utf-8")

    args = Namespace(
        file=str(file),
        indent=2,
        compact=False,
        in_place=False,
    )
    run(args)

    captured = capsys.readouterr()
    assert "JSON 解析错误" in captured.out or "出错" in captured.out


def test_jsonfmt_file_not_found(capsys):
    """测试文件不存在"""
    args = Namespace(
        file="不存在的文件.json",
        indent=2,
        compact=False,
        in_place=False,
    )
    run(args)

    captured = capsys.readouterr()
    assert "不存在" in captured.out

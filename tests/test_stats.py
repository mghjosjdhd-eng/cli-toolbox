"""测试 stats 工具"""

from argparse import Namespace
import pytest
from tools.stats import count_file, run




def test_count_file(tmp_path):
    """测试单个文件统计"""
    file = tmp_path / "test.txt"
    file.write_text("hello world\n这是第二行\n第三行", encoding="utf-8")

    result, error = count_file(file)
    assert error is None
    lines, words, chars, byte_count = result

    assert lines == 3
    assert words == 4  # "hello" "world" "这是第二行" "第三行"
    # 中英文混合分词依赖 split()，这里只验证结果不为 0
    assert words > 0
    assert chars > 0
    assert byte_count > 0


def test_count_file_empty(tmp_path):
    """测试空文件"""
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")

    result, error = count_file(file)
    assert error is None
    lines, words, chars, byte_count = result
    assert lines == 0
    assert words == 0
    assert chars == 0


def test_count_file_not_found():
    """测试文件不存在"""
    from pathlib import Path
    result, error = count_file(Path("不存在的文件.txt"))
    assert result is None
    assert error is not None


def test_stats_run(tmp_path, capsys):
    """测试 run 函数输出"""
    file = tmp_path / "hello.txt"
    file.write_text("hello world", encoding="utf-8")

    args = Namespace(files=[str(file)])
    run(args)

    captured = capsys.readouterr()
    # 应该输出一行统计数据
    assert "hello.txt" in captured.out
    assert "1" in captured.out  # 至少有一行（没有换行符的情况是一行）


def test_stats_multiple_files(tmp_path, capsys):
    """测试多文件统计"""
    (tmp_path / "a.txt").write_text("aaa", encoding="utf-8")
    (tmp_path / "b.txt").write_text("bbb", encoding="utf-8")

    import glob as g
    args = Namespace(files=[str(tmp_path / "*.txt")])
    run(args)

    captured = capsys.readouterr()
    assert "合计" in captured.out

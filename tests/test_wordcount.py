"""测试 wordcount 工具"""

from argparse import Namespace
import pytest
from tools.wordcount import count_words, run


def test_count_words_english(tmp_path):
    """纯英文：大小写合并、按次数降序"""
    file = tmp_path / "eng.txt"
    file.write_text("Hello world hello Python world", encoding="utf-8")

    result, error = count_words(file)
    assert error is None
    # [("hello", 2), ("world", 2), ("python", 1)]
    assert result[0] == ("hello", 2)
    assert result[1] == ("world", 2)
    assert result[2] == ("python", 1)


def test_count_words_mixed_chinese(tmp_path):
    """中英混合：英文单词整体计，汉字逐个计"""
    file = tmp_path / "mix.txt"
    file.write_text("学习 AI AI", encoding="utf-8")

    result, error = count_words(file)
    assert error is None
    assert result[0] == ("ai", 2)
    # 「学」「习」各出现 1 次
    assert ("学", 1) in result
    assert ("习", 1) in result


def test_count_words_empty(tmp_path):
    """空文件：无词"""
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")

    result, error = count_words(file)
    assert error is None
    assert result == []


def test_count_words_not_found():
    """文件不存在"""
    from pathlib import Path
    result, error = count_words(Path("不存在的文件.txt"))
    assert result is None
    assert error is not None


def test_run_output(tmp_path, capsys):
    """run 输出：按次数降序且只显示前 N 个"""
    file = tmp_path / "a.txt"
    file.write_text("go go go go go", encoding="utf-8")

    args = Namespace(file=str(file), top=1)
    run(args)

    captured = capsys.readouterr()
    assert "5" in captured.out  # go 出现 5 次
    assert "go" in captured.out

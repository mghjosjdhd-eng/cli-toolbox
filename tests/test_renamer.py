"""测试 rename 工具"""

from argparse import Namespace
import pytest
from tools.renamer import run




def test_rename_prefix(tmp_path):
    """测试加前缀"""
    # 创建测试文件
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")

    args = Namespace(
        directory=str(tmp_path),
        prefix="pre_",
        suffix=None,
        replace=None,
        replace_with=None,
        number=None,
        yes=True,  # 跳过确认
    )
    run(args)

    renamed = sorted([f.name for f in tmp_path.iterdir()])
    assert renamed == ["pre_a.txt", "pre_b.txt"]


def test_rename_suffix(tmp_path):
    """测试加后缀"""
    (tmp_path / "doc.txt").write_text("content")

    args = Namespace(
        directory=str(tmp_path),
        prefix=None,
        suffix="_v2",
        replace=None,
        replace_with=None,
        number=None,
        yes=True,
    )
    run(args)

    renamed = [f.name for f in tmp_path.iterdir()]
    assert renamed == ["doc_v2.txt"]


def test_rename_replace(tmp_path):
    """测试替换文件名中的文字"""
    (tmp_path / "old_report.txt").write_text("data")
    (tmp_path / "old_summary.txt").write_text("data")

    args = Namespace(
        directory=str(tmp_path),
        prefix=None,
        suffix=None,
        replace="old",
        replace_with="new",
        number=None,
        yes=True,
    )
    run(args)

    renamed = sorted([f.name for f in tmp_path.iterdir()])
    assert renamed == ["new_report.txt", "new_summary.txt"]


def test_rename_number(tmp_path):
    """测试按序号重命名"""
    (tmp_path / "x.txt").write_text("1")
    (tmp_path / "y.txt").write_text("2")
    (tmp_path / "z.txt").write_text("3")

    args = Namespace(
        directory=str(tmp_path),
        prefix=None,
        suffix=None,
        replace=None,
        replace_with=None,
        number=["img_", 1],
        yes=True,
    )
    run(args)

    renamed = sorted([f.name for f in tmp_path.iterdir()])
    assert renamed == ["img_1.txt", "img_2.txt", "img_3.txt"]


def test_rename_empty_directory(tmp_path):
    """测试空目录"""
    args = Namespace(
        directory=str(tmp_path),
        prefix="pre_",
        suffix=None,
        replace=None,
        replace_with=None,
        number=None,
        yes=True,
    )
    run(args)  # 应该不会报错，只是没有操作

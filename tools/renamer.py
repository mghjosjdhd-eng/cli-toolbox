"""文件批量重命名工具"""

import re
from pathlib import Path


def natural_sort_key(name):
    """自然排序：把文件名中的数字按数值排序（file2 < file10）"""
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", name)]


def run(args):
    """主入口，接收 argparse 解析后的参数"""
    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"错误：'{args.directory}' 不是有效的目录")
        return

    # 用自然排序，file2 排在 file10 前面
    files = sorted(
        [f for f in directory.iterdir() if f.is_file()],
        key=lambda f: natural_sort_key(f.name),
    )
    if not files:
        print(f"目录 '{args.directory}' 中没有文件")
        return

    # 根据操作类型生成新旧文件名映射
    renames = []

    if args.number:
        base_name, start_num = args.number[0], int(args.number[1])
        for i, f in enumerate(files):
            new_name = f"{base_name}{start_num + i}{f.suffix}"
            renames.append((f, directory / new_name))

    elif args.replace and args.replace_with is not None:
        for f in files:
            new_stem = f.stem.replace(args.replace, args.replace_with)
            new_name = new_stem + f.suffix
            renames.append((f, directory / new_name))

    elif args.prefix:
        for f in files:
            new_name = f"{args.prefix}{f.name}"
            renames.append((f, directory / new_name))

    elif args.suffix:
        for f in files:
            new_name = f"{f.stem}{args.suffix}{f.suffix}"
            renames.append((f, directory / new_name))

    else:
        print("请指定一种操作：--prefix、--suffix、--replace 或 --number")
        print("用 --help 查看详细用法")
        return

    # 检测重名冲突
    existing_names = {f.name for f in directory.iterdir()}
    conflicts = []
    for old, new in renames:
        if new.name in existing_names and new != old:
            conflicts.append((old, new))

    if conflicts:
        print("\n⚠ 警告：以下目标文件名已存在，继续操作会覆盖：")
        print("-" * 50)
        for old, new in conflicts:
            print(f"  {old.name}  →  {new.name}  (目标已存在)")
        print("-" * 50)
        if not args.yes:
            answer = input("\n是否继续？(y/n): ").strip().lower()
            if answer != "y":
                print("已取消")
                return

    # 预览变更
    print("\n将要执行以下重命名：")
    print("-" * 50)
    for old, new in renames:
        marker = " ⚠覆盖" if (old, new) in conflicts else ""
        print(f"  {old.name}  →  {new.name}{marker}")
    print("-" * 50)

    # 确认
    if not args.yes:
        answer = input("\n确认执行？(y/n): ").strip().lower()
        if answer != "y":
            print("已取消")
            return

    # 逐文件执行，出错不中断后续
    success = 0
    failed = 0
    for old, new in renames:
        try:
            old.rename(new)
            success += 1
        except OSError as e:
            print(f"  出错：{old.name} → {new.name}（{e}）")
            failed += 1

    print(f"\n完成！成功 {success} 个" + (f"，失败 {failed} 个" if failed else ""))

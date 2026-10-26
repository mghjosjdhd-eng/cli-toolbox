# CLI 工具箱（给 Claude Code 看）

## 这是什么
Python 命令行工具箱，入口 `toolbox.py`，含 4 个子命令：
rename（批量重命名）、jsonfmt（JSON 格式化）、stats（文本统计）、toc（Markdown 目录生成）。

## 常用命令
- 运行: `python toolbox.py <子命令> [参数]`（如 `python toolbox.py stats README.md`）
- 测试: `python -m pytest tests/ -q`（当前 21 项，必须全绿）

## 约定
- 代码注释和 CLI 输出用中文
- 改动任何工具后必须跑对应测试（tests/test_<工具名>.py）
- 不要动 tests/ 目录——测试是验收标准
- 加新工具：tools/ 下建模块 → toolbox.py 里加 argparse 子命令 → README「工具列表」加一节
- 新依赖只加 requirements.txt

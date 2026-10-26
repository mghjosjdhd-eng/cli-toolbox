# CLI 工具箱

<!-- toc -->

- [CLI 工具箱](#cli-工具箱)
  - [安装](#安装)
  - [工具列表](#工具列表)
    - [1. 文件批量重命名 (`rename`)](#1-文件批量重命名-rename)
    - [2. JSON 格式化 (`jsonfmt`)](#2-json-格式化-jsonfmt)
    - [3. 文本统计 (`stats`)](#3-文本统计-stats)
    - [4. Markdown 目录生成 (`toc`)](#4-markdown-目录生成-toc)
    - [5. 词频统计 (`wordcount`)](#5-词频统计-wordcount)
  - [运行测试](#运行测试)



一个小巧实用的 Python 命令行工具箱，包含日常开发中常用的 5 个小工具。

## 安装

```bash
# 克隆到本地
git clone <仓库地址>
cd cli-toolbox

# 安装依赖（只有测试需要）
pip install -r requirements.txt
```

## 工具列表

### 1. 文件批量重命名 (`rename`)

```bash
# 加前缀
python toolbox.py rename ./my-files --prefix "backup_"

# 加后缀
python toolbox.py rename ./my-files --suffix "_v2"

# 替换文件名中的文字
python toolbox.py rename ./my-files --replace "旧文字" --with "新文字"

# 按数字序号重命名
python toolbox.py rename ./my-files --number "photo_" 1
```

### 2. JSON 格式化 (`jsonfmt`)

```bash
# 美化输出（2 空格缩进）
python toolbox.py jsonfmt data.json --indent 2

# 压缩成一行
python toolbox.py jsonfmt data.json --compact

# 写回文件（原地格式化）
python toolbox.py jsonfmt data.json --indent 4 --in-place
```

### 3. 文本统计 (`stats`)

```bash
# 统计单个文件
python toolbox.py stats README.md

# 统计多个文件
python toolbox.py stats *.py
```

### 4. Markdown 目录生成 (`toc`)

```bash
# 生成目录并插入到文件中
python toolbox.py toc README.md
```

### 5. 词频统计 (`wordcount`)

```bash
# 统计出现次数最多的前 10 个词（英文单词整体计，汉字逐个计）
python toolbox.py wordcount README.md

# 只看前 5 个
python toolbox.py wordcount README.md --top 5
```

## 运行测试

```bash
pytest tests/
```

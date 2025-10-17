# Repository Guidelines

## 项目结构与模块
本仓库以教学模块划分，根目录下的 `0_querying.py` 至 `6_subagents.py` 对应逐步进阶示例；辅助函数集中在 `cli_tools.py`；`docs/` 存放每个模块的延伸说明；`db/` 提供示例数据；`.claude/` 内的配置需根据本机路径调整。新增脚本时请按照模块编号放置，保持教学顺序。

## 构建、运行与开发
首次克隆后执行 `uv sync` 安装依赖；开发期推荐通过 `uv run python 0_querying.py` 这类命令运行模块，必要时附加 `--model claude-sonnet-4-20250514`。为调试工具，可利用 `uv run python 2_tools.py --help` 查看参数。若需快速 lint，请至少运行 `python -m compileall .` 确认语法。

## 编码风格与命名
全仓库使用 Python 3.13，遵循 PEP 8 与四空格缩进。模块文件沿用数字前缀，函数与变量使用 snake_case；面向终端的输出请通过 `rich` 保持一致风格。提交前清理未使用的导入与调试输出。

## 测试与验证
目前未引入自动化测试；新增特性时请在 `tests/` 目录创建 `test_<功能>.py` 并编写 `pytest` 用例，确保模块化函数可直接调用。增强交互脚本时务必手动运行相应模块，验证 MCP 工具与子代理配置信息。

## 提交与拉取请求
参考提交历史，使用英文小写祈使句（如 `add mcp tool example`），首行不超过 60 字符，关联议题可在正文注明 `Refs #id`。拉取请求需概述变更、列出测试命令与截图（若涉及终端界面），并说明对现有模块的影响。

## 配置与安全
将敏感令牌写入 `.env` 并加入 `.gitignore`，勿上传个人 Claude 凭据。更新 `.claude/settings.json` 时替换本地音频命令或移除声音钩子，避免硬编码系统路径。

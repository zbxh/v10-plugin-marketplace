# 智简魔方 V10 插件开发与商城上架

一个面向智简魔方业务系统 V10 的 Codex 技能。可以从插件想法、已有项目、报错截图或安装 ZIP 开始，根据当前任务进入开发、排查、测试或商城打包流程。[技能入口](SKILL.md)

## 安装

在插件开发项目的根目录执行。

```bash
git clone https://github.com/zbxh/v10-plugin-marketplace.git .agents/skills/v10-plugin-marketplace
```

需要跨项目使用时，将目标目录改为 `$HOME/.agents/skills/v10-plugin-marketplace`。[OpenAI Docs](https://developers.openai.com/codex/skills)

## 使用示例

在 Codex 里说一句话即可，也可以加上 `$v10-plugin-marketplace` 指定技能。

- 「我想做个续费提醒插件，先聊聊首版怎么做。」
- 「读一下这个插件，帮我找出后台保存失败的原因。」
- 「用这个 ZIP 测纯净安装，再测试官方主题和我指定的第三方主题。」
- 「按我指定的版本打一个商城测试包，顺便写版本说明。」

## 内置工具

- [官方文档索引](references/official-docs.md)按业务需求定位扩展类型、Hook 和主题目录。[从零开发指南](references/new-plugin.md)提供首个业务场景的开发步骤与[最小 addon 模板](assets/addon/ExamplePlugin.php)。
- [安装与升级验收](references/acceptance.md)涵盖纯净站、既有版本升级和主题测试。
- [商城打包指南](references/marketplace.md)包含授权代码注入兼容检查和[只读 ZIP 检查工具](scripts/check_zip.py)。脚本用 Python 3 和目标环境的 PHP CLI 校验包结构、完整性与 PHP 语法。

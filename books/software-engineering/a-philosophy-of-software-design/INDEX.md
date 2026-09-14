# 《软件设计的哲学》有声博客

| 字段 | 内容 |
| --- | --- |
| 英文书名 | A Philosophy of Software Design, 2nd Edition |
| 中文书名 | 软件设计的哲学，第二版 |
| 作者 | John Ousterhout |
| 主题 | 软件工程 |
| 语音 | Grok Voice `ara` / `zh` |

## 来源与许可

本系列对应的中文译本为 [yingang/aposd2e-zh](https://github.com/yingang/aposd2e-zh)（《软件设计的哲学，第二版》中文翻译），采用 [CC-BY 4.0](https://github.com/yingang/aposd2e-zh/blob/main/LICENSE) 许可。

在线阅读：

- [简体中文](https://yingang.github.io/aposd2e-zh/)
- [繁体中文](https://yingang.github.io/aposd2e-zh/zh-tw/)

已完成剧集的脚本文为口语化改编，非原文照搬。使用译本或改编内容时请保留上述署名。请勿编造未出现在来源中的书籍事实。

目录原文见译本 [README「目录」](https://github.com/yingang/aposd2e-zh#目录)。00–03 的标题取自各集 `meta.json`；其余标题与译本目录一致。

## 发布顺序

| 顺序 | 目录 | 标题 | 译本源文件 | 状态 |
| --- | --- | --- | --- | --- |
| 0 | `episodes/00-preface/` | 前言：为什么需要一本讲软件设计的书 | `docs/preface.md` | 已有脚本 |
| 1 | `episodes/01-intro/` | 第1章 介绍：软件最大的限制是理解力 | `docs/ch01.md` | 已有脚本 |
| 2 | `episodes/02-complexity/` | 第2章 复杂性的本质 | `docs/ch02.md` | 已有脚本 |
| 3 | `episodes/03-strategic/` | 第3章 能工作的代码是不够的 | `docs/ch03.md` | 已有脚本 |
| 4 | `episodes/04-deep-modules/` | 第 4 章 模块应该是深的 | `docs/ch04.md` | 占位 |
| 5 | `episodes/05-info-hiding/` | 第 5 章 信息隐藏和信息泄露 | `docs/ch05.md` | 占位 |
| 6 | `episodes/06-general-modules/` | 第 6 章 通用的模块是更深的 | `docs/ch06.md` | 占位 |
| 7 | `episodes/07-different-layers/` | 第 7 章 不同的层级，不同的抽象 | `docs/ch07.md` | 占位 |
| 8 | `episodes/08-pull-complexity-down/` | 第 8 章 下沉复杂性 | `docs/ch08.md` | 占位 |
| 9 | `episodes/09-together-or-apart/` | 第 9 章 在一起更好还是分开更好？ | `docs/ch09.md` | 占位 |
| 10 | `episodes/10-define-errors-out/` | 第 10 章 通过定义来规避错误 | `docs/ch10.md` | 占位 |
| 11 | `episodes/11-design-it-twice/` | 第 11 章 设计两次 | `docs/ch11.md` | 占位 |
| 12 | `episodes/12-comments-excuses/` | 第 12 章 不写注释的四个借口 | `docs/ch12.md` | 占位 |
| 13 | `episodes/13-comments-why/` | 第 13 章 注释应该描述代码中难以理解的内容 | `docs/ch13.md` | 占位 |
| 14 | `episodes/14-choosing-names/` | 第 14 章 选取名称 | `docs/ch14.md` | 占位 |
| 15 | `episodes/15-write-comments-first/` | 第 15 章 先写注释 | `docs/ch15.md` | 占位 |
| 16 | `episodes/16-modifying-existing/` | 第 16 章 修改现有的代码 | `docs/ch16.md` | 占位 |
| 17 | `episodes/17-consistency/` | 第 17 章 一致性 | `docs/ch17.md` | 占位 |
| 18 | `episodes/18-code-should-be-obvious/` | 第 18 章 代码应该是易理解的 | `docs/ch18.md` | 占位 |
| 19 | `episodes/19-software-trends/` | 第 19 章 软件发展趋势 | `docs/ch19.md` | 占位 |
| 20 | `episodes/20-performance/` | 第 20 章 性能设计 | `docs/ch20.md` | 占位 |
| 21 | `episodes/21-decide-what-matters/` | 第 21 章 决定什么是重要的 | `docs/ch21.md` | 占位 |
| 22 | `episodes/22-conclusion/` | 第 22 章 结论 | `docs/ch22.md` | 占位 |
| 23 | `episodes/23-summary/` | 总结 | `docs/summary.md` | 占位 |

剧集文件夹约定：

```text
episodes/<id>/
  script.md    # 朗读脚本
  meta.json    # 剧集元数据
  audio.mp3    # Grok Voice 产出（Git LFS）
  images/      # 优先原书插图
```

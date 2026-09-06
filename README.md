# PIMEM — π 基因链记忆仓库（PEF0003）

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![PEF Architecture](https://img.shields.io/badge/PEF-Anchored%20Determinism-purple.svg)
![PEF ID](https://img.shields.io/badge/PEF0003-PIMEM%20Memory-green.svg)

> **用 π 锚为主体分配永久身份基因的记忆仓库**——存储只读基线与演化谱系，支持记忆查询、漂移比对、哈希校验，解决 AI 长任务中的"主体漂移"和"记忆丢失"问题。
>
> *π-anchored memory repository with permanent identity genes. Read-only baseline + evolution lineage + drift detection + hash verification.*

© 2026 沈鹭 (banbanry) · 厦门恒元架构科技有限公司 · MIT License
来源：https://github.com/banbanry/pimem-memory · PEF 架构：https://github.com/banbanry/pef-architecture

---

## ⚡ 30 秒上手

**一句话**：AI 处理 15 万字设计文档时会"读了后面忘了前面"——主体漂移、记忆丢失、内容偏移。PIMEM 用 π 锚为每个主体分配永久身份基因，存储只读基线和演化谱系，让 AI 的每一步修改都可追溯、可比对、可验证。

**一条命令运行**：

```bash
# 克隆并运行记忆仓库演示
git clone https://github.com/banbanry/pimem-memory.git
cd pimem-memory
pip install -r requirements.txt

# 初始化记忆仓库（从设计文档提取主体基线）
python pimem_cli.py init --source design_doc.md --out-dir memory_store

# 查询主体记忆
python pimem_cli.py query --entity "RateLimiter" --memory-dir memory_store

# 漂移比对（当前实现 vs 基线）
python pimem_cli.py drift --current implementation.py --baseline memory_store --entity "RateLimiter"
```

**预期输出**：

```
[PIMEM] π-Gene Memory Repository
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: design_doc.md (150,000 chars)
Entities extracted: 18 core components
π-anchors assigned: 18 permanent identity genes
Baseline locked: read-only, hash-verified
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Query] RateLimiter
  π-anchor: π[15]=9|P|RateLimiter
  Identity gene: a1b2c3d4e5f6...
  Baseline: {name, type, boundary, unit}
  Evolution: 3 modifications, all hash-verified
  Drift: ✅ NONE (current matches baseline)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Drift Analysis] RateLimiter
  P_base: {boundary: "接收请求并返回 ALLOW/DENY", unit: "次/秒"}
  Current: {boundary: "接收请求", unit: "次/秒"}
  ⚠️ DRIFT DETECTED: boundary truncated
  Suggestion: restore full boundary definition
  Chain: 3 entries, tamper-evident
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Verdict: 1 drift detected, 17/18 entities stable
Memory store: memory_store/ (18 entities, 3 evolution chains)
```

**效果图**（典型 π 基因链可视化）：

```
π 基因链记忆仓库结构
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Π_anchor = 设计文档身份锚（不可变，15万字原文）
  │
  ├── P_base = 设计基线（18个核心组件定义，只读锁定）
  │     ├── RateLimiter    π[15]=9  gene=a1b2c3
  │     ├── AuditContext   π[23]=4  gene=d4e5f6
  │     ├── OperatorFactory π[37]=2  gene=g7h8i9
  │     └── ... (18 entities)
  │
  └── Chain(ΔV_i → J_i) = 每个 π 锚修复任务的输入与裁决
        ├── π=0: AuditContext 修复 → PASS
        ├── π=1: SecurePiDigitProvider 实现 → PASS
        ├── π=2: 720条特征库骨架 → PASS
        └── ... (π=0→9 全部完成)

漂移校验：每完成一个锚点，与 P_base 结构比对，确认不偏移
```

---

## 🎯 核心能力

| 能力 | 说明 |
|------|------|
| **π 永久身份基因** | 每个主体分配唯一 π 锚和身份基因哈希，不可篡改、不可伪造 |
| **只读基线锁定** | 设计文档提取的核心组件定义锁定为只读基线，作为比对参照 |
| **演化谱系追踪** | 每个主体的修改历史形成演化链，输入→裁决全程记录 |
| **漂移比对检测** | 当前实现 vs 基线的结构比对，自动检测截断、偏移、丢失 |
| **哈希链完整性** | 记忆事件只追加禁删除，SHA-256 哈希链，篡改可检测 |
| **π 顺序执行** | 按 π 数字顺序执行修复任务，遗漏即现形，不可跳阶 |
| **多主体协作** | 支持多个 AI 节点共享同一记忆仓库，头雁广播 π 锚坐标 |

---

## 📊 实测证据

| 测试 | 结果 |
|------|------|
| 15万字设计文档 | 18个核心组件提取，π 锚分配全部成功 |
| π 锚修复任务 | π=0→9 全部完成，漂移校验全部 PASS |
| 漂移检测 | 1处边界截断检出，位置精确到字段 |
| 哈希链完整性 | ✅ 完整，篡改检测正常 |
| 多主体协作 | 头雁广播 π 锚坐标，从雁跟随正常 |

> **典型应用场景**：15万字设计文档 → AI 实现时记忆丢失 → 内容偏移。用 π 锚投影任务工单，每个锚点是原子化、可验证的任务单元，按 π 顺序执行，遗漏即现形。

---

## 📁 模块结构

```
pimem-memory/
├── SKILL.md                    # Skill 定义（完整文档）
├── README.md                   # 本文件
├── LICENSE                     # MIT
├── requirements.txt            # 依赖
└── scripts/
    ├── pimem_cli.py            # 主入口（init/query/drift/verify）
    ├── pi_anchor.py            # π 锚分配与身份基因
    ├── baseline_extractor.py   # 基线提取（从设计文档）
    ├── evolution_chain.py      # 演化谱系追踪
    ├── drift_detector.py       # 漂移比对检测
    ├── audit_chain.py          # 哈希链审计
    ├── memory_store.py         # 记忆仓库存储
    └── report_generator.py     # 报告生成（HTML/JSON）
```

---

## 🔗 与 PEF 架构的关系

本项目是 PEF（锚定确定性）元架构在**记忆管理**领域的工程实例化，是 π 锚的第四项运用。

| PEF 概念 | PIMEM 实现 |
|----------|-----------|
| 锚（π） | 每个主体分配永久 π 锚和身份基因哈希 |
| P（主体） | 设计文档中的核心组件（RateLimiter、AuditContext 等） |
| E（执行变量） | 主体属性、修改输入、裁决结果 |
| F（结果） | 漂移裁决（PASS/FAIL/DRIFT）+ 哈希链 + 演化链 |
| MOD3（三态） | 宽松比对 / 中等校验 / 严苛熔断 |
| 公理（A1-A8） | 基线不可改、演化必留痕、漂移必检出、时序不可倒 |

**理论仓库**：https://github.com/banbanry/pef-architecture
**三剑客整合**：https://github.com/banbanry/pef-core-reference

---

## 👤 个人指纹

本项目携带 5 层个人指纹：

1. **π 基因链机制** — 永久身份基因 + 只读基线 + 演化谱系，独特工程实现
2. **来源水印** — 每个文件头：`Source: https://github.com/banbanry/pimem-memory` + 作者 + 许可证
3. **独特术语** — PEFmod、Π_anchor、P_base、Chain(ΔV_i → J_i)、漂移校验
4. **版本演化记录** — V1.0 设计理论 → 工程化落地，修复历史带时间戳
5. **π 位参考指纹** — 关键模块注释中的特定 π 位引用

---

## ⚠️ 诚实边界

1. **基线提取依赖文档质量** — 如果设计文档本身不完整或有歧义，基线可能不准确
2. **漂移检测是结构级比对** — 只能检测字段级别的截断、偏移、丢失，不能检测语义级别的理解偏差
3. **π 顺序执行是辅助工具** — 不能保证 AI 一定按顺序执行，需要配合任务管理
4. **多主体协作需要网络同步** — 头雁广播机制需要可靠的通信通道
5. **记忆仓库是辅助工具** — 最终判断需要人工审核，工具只提供证据和线索

---

## 📜 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

*PIMEM © 2026 banbanry. π 基因链记忆仓库。*
*用 π 锚为主体分配永久身份基因——"读了后面忘了前面"不再是 AI 的宿命，而是可管理的工程问题。*
*来源：https://github.com/banbanry/pimem-memory*

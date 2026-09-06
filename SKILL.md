---
name: pimem-memory
description: PIMEM π-基因链记忆仓库（PEF-π 第四项运用）。用 π 锚为"主体"分配永久身份基因，存储只读基线 P_base 与演化谱系 Chain(ΔV_i → J_i)，支持记忆查询、漂移比对、哈希链验真。当用户需要建立可查询、可比对、可防漂移的记忆库时使用：如"把 XX 的知识/状态/决策按 π 锚存成记忆"、"查一下之前对 XX 的结论"、"比对当前状态和当初基线有没有漂移"、"验证记忆有没有被改过"。触发词：PIMEM、π记忆、记忆锚、基因链记忆、主体漂移检测。
---

# PIMEM π-基因链记忆仓库

设计依据: PEF-EXT-MEM-004 PIMEM 设计理论 V1.0（PEF-π 第四项运用）。
核心三元组 `(Π_anchor, P_base, Chain)`：**Π_anchor**=π 数位一次性分配的身份基因（永久固定）；**P_base**=只读基线快照（定义类 DEF_FIELDS 参与漂移比对 / 状态类 STATE_FIELDS 允许演化）；**Chain**=哈希链锁定的演化谱系（只追加）。

## 快速开始

```bash
# 1. 基因初始化（分配 Π_anchor + 写 P_base + 创世上链）
python scripts/pimem_cli.py --root <记忆库目录> init \
  --name RateLimiter --type LOGICAL --boundary "接收请求返回ALLOW/DENY" --unit "次/秒" \
  --def-fields "limit=100" --state-fields "current=0"

# 2. 追加演化记录（每轮推演/决策/状态变化都记）
python scripts/pimem_cli.py --root <记忆库目录> remember \
  --anchor "π[0]=3" --delta-v "rate=120" --judgment FAIL --rho 0.7 --mod3 2

# 3. 查询演化谱系（记忆回溯）
python scripts/pimem_cli.py --root <记忆库目录> query --anchor "π[0]=3"

# 4. 漂移比对（核心：当前状态 vs 基线定义类字段）
python scripts/pimem_cli.py --root <记忆库目录> diff \
  --anchor "π-0-3" --current-file current_state.json   # 推荐: JSON 文件方式

# 5. 验真（哈希链完整性 + 注册表摘要; 篡改时退出码=1）
python scripts/pimem_cli.py --root <记忆库目录> verify --anchor "π-0-3"
echo $LASTEXITCODE   # 0=链完整, 1=检出篡改
```

## 命令速查

| 命令 | 用途 | 关键参数 |
|---|---|---|
| `init` | 基因初始化（每个主体一次） | `--name --type --boundary --unit --def-fields k=v --state-fields k=v` |
| `remember` | 追加演化记录 | `--anchor --delta-v --judgment PASS/FAIL --rho --mod3` |
| `query` | 查演化谱系 | `--anchor` |
| `diff` | **漂移比对**（当前 vs 基线） | `--anchor --current-file <json>`（推荐）或 `--current '<json>'` |
| `verify` | 哈希链 + 注册表验真 | `--anchor` |
| `list` | 列全部主体 | — |
| `tree` | 演化谱系树（分叉示意） | `--anchor` |

所有命令可加 `--root <目录>` 指定记忆库位置（默认当前目录，数据存 `<root>/pimem_memory/`）。

## 使用规则

0. **PowerShell/命令行注意**：内层双引号会被 shell 吞掉，`--current '{"a":1}'` 会解析失败——一律用 `--current-file` 传 JSON 文件；`--anchor` 格式为 `π-<位置>-<数位>`（如 `π-0-3`），不含方括号。

1. **一个主体只 init 一次**：Π_anchor 永久固定不可重入；后续全部用 `remember` 追加。
2. **DEF vs STATE 字段**：身份/规格承诺（名称、边界、单位、不可变参数）放 `--def-fields`，会参与漂移告警；运行时状态（当前值、模式）放 `--state-fields`，变化只记演化不告警。
3. **漂移处置**（对齐 PIMEM 文档阶段四）：diff 检出漂移 → 默认先阻断（不再 remember）→ 告警 → 人工决定是否回退基线。勿直接覆盖 P_base。
4. **信任链**：`verify` 验哈希链 + D_base 摘要。任何篡改会断裂——这是"记忆没被改过"的可审计证据。
5. **诚实边界**：本实现为记忆层工具，不替代 PEF 本体公理；π 锚位单调消耗（前 200 位），与设计文档"不可回退"一致。

## 典型场景

- **知识记忆**：把每条结论/决策存为 `remember`，随时 `query` 回溯"之前是怎么定的"。
- **状态比对**：定期 `diff` 当前状态 vs 当初基线，秒级发现"主体漂移"（如参数被静默改掉）。
- **长会话记忆**：AI 工作记忆的外置锚定——跨会话取回基线 + 演化链，防止"AI 忘了当初约定"。
- **审计留痕**：`verify` 证明记忆链未被篡改（哈希链 + 创世摘要）。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIMEM π-基因链记忆仓库 CLI
设计依据: PEF-EXT-MEM-004 PIMEM 设计理论 V1.0 (PEF-π 第四项运用)
核心: (Π_anchor, P_base, Chain(ΔV_i → J_i)) 三元组
  - Π_anchor : π 数位一次性分配, 永久固定, 不可回退
  - P_base   : 只读基线快照 (DEF_FIELDS 定义类/ STATE_FIELDS 状态类)
  - Chain    : 演化链, 哈希链锁定, 只追加
命令: init / remember / query / diff / verify / list / tree
零第三方依赖 (stdlib only)
"""
import argparse, hashlib, json, os, sys, time

# ---- π 预置表 (前 200 位, 不可由程序计算, 查表即锚定) ----
PI_DIGITS = ("314159265358979323846264338327950288419716939937510582097494"
             "459230781640628620899862803482534211706798214808651328230664"
             "709384460955058223172535940812848111745028410270193852110555"
             "964462294895493038196")

# ---- 记忆库结构 ----
REGISTRY_FILE = "registry.json"   # Πanchor ↦ {P_base, D_base}
CHAIN_PREFIX = "chain_"           # chain_<anchor>.json  演化链

def _path(root):
    return os.path.join(root, "pimem_memory")

def _canon(d):
    """canonical JSON 序列化 (排序键, 紧凑, 无空格)"""
    return json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def _load(fp):
    if not os.path.exists(fp):
        return {}
    with open(fp, encoding="utf-8-sig") as f:
        return json.load(f)

def _save(fp, d):
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)

def _alloc_anchor(registry):
    """按注册表条目数分配下一个 π 锚位, 单调递增不可回退
    锚格式: π-<位置>-<数位>  (如 π-0-3); 避免方括号数字, 兼容跨平台文件名"""
    used = len(registry)
    if used >= len(PI_DIGITS):
        sys.exit("✗ π 锚位耗尽 (前 200 位已全部分配)")
    pos = used
    return f"π-{pos}-{PI_DIGITS[pos]}"

# ================= 命令实现 =================

def cmd_init(a):
    root = a.root
    reg = _load(os.path.join(_path(root), REGISTRY_FILE))
    name = a.name
    if any(r.get("name") == name for r in reg.values()):
        sys.exit(f"✗ 主体 '{name}' 已存在 (Π_anchor 不可重复初始化, 请用 remember 追加演化)")
    anchor = _alloc_anchor(reg)
    pbase = {
        "name": name,
        "type": a.type or "LOGICAL",
        "boundary": a.boundary or "",
        "unit": a.unit or "",
        "def_fields": dict(kv.split("=", 1) for kv in (a.def_fields or [])),
        "state_fields": dict(kv.split("=", 1) for kv in (a.state_fields or [])),
    }
    dbase = _sha(_canon({"anchor": anchor, "p_base": pbase}))
    reg[anchor] = {"name": name, "p_base": pbase, "d_base": dbase,
                   "created": time.strftime("%Y-%m-%dT%H:%M:%S")}
    _save(os.path.join(_path(root), REGISTRY_FILE), reg)
    # 创世上链: GENESIS 记录 (注册表可审计)
    chain = _load(os.path.join(_path(root), CHAIN_PREFIX + anchor.replace("=", "_").replace("[", "_").replace("]", "_") + ".json"))
    genesis = {"seq": 0, "event": "GENESIS", "anchor": anchor,
               "d_base": dbase, "prev_hash": "GENESIS",
               "t": time.strftime("%Y-%m-%dT%H:%M:%S")}
    genesis["hash"] = _sha(_canon(genesis))
    chain["entries"] = [genesis]
    _save(os.path.join(_path(root), CHAIN_PREFIX + anchor.replace("=", "_").replace("[", "_").replace("]", "_") + ".json"), chain)
    print(f"✅ 基因初始化完成")
    print(f"   Π_anchor : {anchor}  (永久固定, 不可回退)")
    print(f"   P_base   : {name} ({pbase['type']}) | boundary={pbase['boundary']} | unit={pbase['unit']}")
    print(f"   D_base   : {dbase[:16]}...")
    print(f"   演化链    : [GENESIS] 已上链")
    print(f"\n   后续命令: remember --anchor '{anchor}' --delta-v '...' --judgment PASS")

def _chain_file(root, anchor):
    safe = anchor.replace("=", "_").replace("[", "_").replace("]", "_")
    return os.path.join(_path(root), CHAIN_PREFIX + safe + ".json")

def cmd_remember(a):
    root = a.root
    reg = _load(os.path.join(_path(root), REGISTRY_FILE))
    if a.anchor not in reg:
        sys.exit(f"✗ 锚 {a.anchor} 不存在, 先 init")
    cf = _chain_file(root, a.anchor)
    chain = _load(cf)
    entries = chain.get("entries", [])
    prev = entries[-1]["hash"] if entries else "GENESIS"
    rec = {
        "seq": len(entries),
        "delta_v": a.delta_v,
        "judgment": a.judgment.upper(),
        "rho": a.rho,
        "mod3": a.mod3,
        "anchor": a.anchor,
        "prev_hash": prev,
        "t": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    rec["hash"] = _sha(_canon(rec))
    entries.append(rec)
    chain["entries"] = entries
    _save(cf, chain)
    print(f"✅ 演化已记录 seq={rec['seq']}  {a.delta_v} → {rec['judgment']} (ρ={a.rho}, MOD3={a.mod3})")
    print(f"   hash={rec['hash'][:16]}...  prev={prev[:16]}...")

def cmd_query(a):
    root = a.root
    reg = _load(os.path.join(_path(root), REGISTRY_FILE))
    if a.anchor not in reg:
        sys.exit(f"✗ 锚 {a.anchor} 不存在")
    r = reg[a.anchor]
    print(f"Π_anchor : {a.anchor}  (创建于 {r['created']})")
    print(f"P_base   : {json.dumps(r['p_base'], ensure_ascii=False)}")
    print(f"D_base   : {r['d_base'][:16]}...")
    cf = _chain_file(root, a.anchor)
    chain = _load(cf)
    entries = chain.get("entries", [])
    print(f"\n演化谱系 ({len(entries)} 条):")
    for e in entries:
        if e.get("event") == "GENESIS":
            print(f"  [{e['seq']:2d}] GENESIS 锚定基线")
        else:
            flag = "✓" if e["judgment"] == "PASS" else "✗"
            print(f"  [{e['seq']:2d}] {flag} {e['delta_v'][:40]:40s} → {e['judgment']} ρ={e['rho']} MOD3={e['mod3']}")

def cmd_diff(a):
    """漂移比对: 当前主体 vs P_base 的 DEF_FIELDS 结构比对 (核心能力)"""
    root = a.root
    reg = _load(os.path.join(_path(root), REGISTRY_FILE))
    if a.anchor not in reg:
        sys.exit(f"✗ 锚 {a.anchor} 不存在")
    r = reg[a.anchor]
    pbase = r["p_base"]
    if a.current_file:
        try:
            with open(a.current_file, encoding="utf-8-sig") as f:
                cur = json.load(f)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            sys.exit(f"✗ 读取 --current-file 失败: {e}")
    else:
        try:
            cur = json.loads(a.current)
        except (ValueError, json.JSONDecodeError):
            sys.exit("✗ --current 必须是 JSON 字符串; 若引号被命令行吞掉, 请改用 --current-file <path.json>")
    # 1) 注册表摘要校验 (防篡改)
    d_check = _sha(_canon({"anchor": a.anchor, "p_base": pbase}))
    base_ok = (d_check == r["d_base"])
    print(f"注册表摘要校验 : {'✅ 一致' if base_ok else '✗ 被篡改! (D_base 不匹配)'}")
    # 2) DEF_FIELDS 漂移比对
    drift = []
    for k, v in (pbase.get("def_fields") or {}).items():
        cv = cur.get(k)
        if str(cv) != str(v):
            drift.append((k, v, cv))
    # name/boundary/unit 也属于定义类
    for k in ("name", "boundary", "unit"):
        if k in cur and str(cur[k]) != str(pbase.get(k)):
            drift.append((k, pbase.get(k), cur[k]))
    if drift:
        print(f"\n⚠ 主体漂移检测: {len(drift)} 个定义类字段偏移")
        for k, old, new in drift:
            print(f"   - {k}: '{old}' → '{new}'")
    else:
        print(f"\n✅ 无漂移: 定义类字段与 P_base 完全一致")
    # 3) 状态类字段演化提示
    st_cur = {k: v for k, v in cur.items() if k not in ("name", "type", "boundary", "unit") and k not in (pbase.get("def_fields") or {})}
    if st_cur:
        print(f"   状态类字段(演化非漂移): {json.dumps(st_cur, ensure_ascii=False)}")

def cmd_verify(a):
    """哈希链完整性 + 注册表摘要全验"""
    root = a.root
    reg = _load(os.path.join(_path(root), REGISTRY_FILE))
    if a.anchor not in reg:
        sys.exit(f"✗ 锚 {a.anchor} 不存在")
    r = reg[a.anchor]
    d_check = _sha(_canon({"anchor": a.anchor, "p_base": r["p_base"]}))
    ok = (d_check == r["d_base"])
    print(f"注册表 D_base : {'✅' if ok else '✗ 篡改'}")
    cf = _chain_file(root, a.anchor)
    chain = _load(cf)
    entries = chain.get("entries", [])
    bad = 0
    prev = "GENESIS"
    for e in entries:
        recomputed = _sha(_canon({k: v for k, v in e.items() if k != "hash"}))
        if recomputed != e["hash"] or e["prev_hash"] != prev:
            bad += 1
            print(f"  ✗ seq={e['seq']} 哈希链断裂!")
        prev = e["hash"]
    print(f"哈希链 : {len(entries)} 条记录, {'✅ 完整' if bad == 0 else f'✗ {bad} 处断裂'}")
    return 0 if (ok and bad == 0) else 1

def cmd_list(a):
    reg = _load(os.path.join(_path(root := a.root), REGISTRY_FILE))
    if not reg:
        print("(空) 尚无主体, 用 init 建立第一个")
        return
    for anchor, r in reg.items():
        print(f"  {anchor}  {r['name']}  ({r['p_base'].get('type')})  创建于 {r['created']}")

def cmd_tree(a):
    """PIMEM-Tree 简化: 沿演化链展示 PASS/FAIL 走向 (分叉记忆示意)"""
    root = a.root
    cf = _chain_file(root, a.anchor)
    chain = _load(cf)
    entries = chain.get("entries", [])
    print(f"Π_anchor {a.anchor} 演化谱系树:")
    for e in entries:
        if e.get("event") == "GENESIS":
            print("  ├─ GENESIS (P_base 基线)")
            continue
        branch = "└─" if e["seq"] == len(entries) - 1 else "├─"
        flag = "PASS" if e["judgment"] == "PASS" else "FAIL⚠"
        print(f"  {branch} [{e['seq']}] {flag} {e['delta_v'][:50]}")

def main():
    ap = argparse.ArgumentParser(description="PIMEM π-基因链记忆仓库")
    ap.add_argument("--root", default=".", help="记忆库根目录 (默认当前目录)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init", help="基因初始化: 分配Π_anchor, 写P_base, 创世上链")
    p.add_argument("--name", required=True); p.add_argument("--type", default="LOGICAL")
    p.add_argument("--boundary", default=""); p.add_argument("--unit", default="")
    p.add_argument("--def-fields", action="append", help="定义类字段 k=v (可多次)")
    p.add_argument("--state-fields", action="append", help="状态类字段 k=v (可多次)")
    p = sub.add_parser("remember", help="追加演化记录 (哈希链锁定)")
    p.add_argument("--anchor", required=True); p.add_argument("--delta-v", required=True)
    p.add_argument("--judgment", choices=["PASS", "FAIL", "MISMATCH"], default="PASS")
    p.add_argument("--rho", type=float, default=0.0); p.add_argument("--mod3", type=int, default=0)
    p = sub.add_parser("query", help="查询主体演化谱系")
    p.add_argument("--anchor", required=True)
    p = sub.add_parser("diff", help="漂移比对: 当前状态 vs P_base 定义类字段")
    p.add_argument("--anchor", required=True)
    p.add_argument("--current", help="当前状态 JSON 字符串")
    p.add_argument("--current-file", help="当前状态 JSON 文件路径 (推荐, 避免引号问题)")
    p = sub.add_parser("verify", help="哈希链完整性 + 注册表校验")
    p.add_argument("--anchor", required=True)
    p = sub.add_parser("list", help="列出所有主体")
    p = sub.add_parser("tree", help="演化谱系树 (分叉记忆示意)")
    p.add_argument("--anchor", required=True)
    a = ap.parse_args()
    rc = {"init": cmd_init, "remember": cmd_remember, "query": cmd_query,
          "diff": cmd_diff, "verify": cmd_verify, "list": cmd_list,
          "tree": cmd_tree}[a.cmd](a)
    sys.exit(rc or 0)

if __name__ == "__main__":
    main()

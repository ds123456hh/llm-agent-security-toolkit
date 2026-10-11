"""加载并统计漏洞分类库与攻击载荷库。

用法：
    python -m llmsec.loader
    python src/llmsec/loader.py
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("缺少依赖 PyYAML。请先运行：pip install -r requirements.txt")

# src/llmsec/loader.py -> parents[2] == 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_yaml(filename: str) -> dict[str, Any]:
    """读取 data/ 下的 YAML 文件。"""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"数据文件不存在：{path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{filename} 的顶层结构应为映射（dict）")
    return data


def load_vulnerabilities() -> list[dict[str, Any]]:
    return load_yaml("vulnerabilities.yaml").get("vulnerabilities", [])


def load_payload_groups() -> list[dict[str, Any]]:
    return load_yaml("payloads.yaml").get("groups", [])


def summarize() -> str:
    """生成一份简短的统计摘要。"""
    vulns = load_vulnerabilities()
    groups = load_payload_groups()

    payload_count = sum(len(g.get("payloads", [])) for g in groups)

    by_severity = Counter(v.get("severity", "unknown") for v in vulns)
    by_status = Counter(v.get("status", "unknown") for v in vulns)
    by_category = Counter(v.get("category", "unknown") for v in vulns)
    by_group = Counter({g["id"]: len(g.get("payloads", [])) for g in groups})

    # 覆盖率：有多少漏洞条目至少被一个载荷组指向
    targeted = {v for g in groups for v in g.get("targets", [])}
    covered = [v["id"] for v in vulns if v["id"] in targeted]

    lines = [
        "=" * 62,
        "  llmsec · 数据库统计",
        "=" * 62,
        "",
        f"漏洞条目   : {len(vulns)}",
        f"载荷分组   : {len(groups)}",
        f"载荷总数   : {payload_count}",
        "",
        "-- 漏洞 · 按严重程度 " + "-" * 40,
    ]
    for key, cnt in by_severity.most_common():
        lines.append(f"  {key:<10} {cnt}")

    lines += ["", "-- 漏洞 · 按状态 " + "-" * 44]
    for key, cnt in by_status.most_common():
        lines.append(f"  {key:<10} {cnt}")

    lines += ["", "-- 漏洞 · 按类别 " + "-" * 44]
    for key, cnt in by_category.most_common():
        lines.append(f"  {key:<14} {cnt}")

    lines += ["", "-- 载荷 · 按分组 " + "-" * 44]
    for key, cnt in by_group.most_common():
        lines.append(f"  {key:<28} {cnt}")

    lines += [
        "",
        "-- 载荷覆盖率 " + "-" * 47,
        f"  已被载荷覆盖的漏洞条目：{len(covered)} / {len(vulns)}",
    ]

    uncovered = [v["id"] for v in vulns if v["id"] not in targeted]
    if uncovered:
        lines.append(f"  尚未覆盖：{', '.join(uncovered)}")

    lines += ["", "=" * 62]
    return "\n".join(lines)


def main() -> int:
    try:
        print(summarize())
    except (FileNotFoundError, ValueError) as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

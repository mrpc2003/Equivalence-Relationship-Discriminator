from typing import List, Tuple, Iterable, Optional, Set
import sys
import os

Matrix = List[List[int]]


def format_matrix(matrix: Matrix, elements: List[int]) -> str:
    n = len(matrix)
    col_width = 2
    header = "    " + " ".join(f"{e:>{col_width}}" for e in elements)
    sep = "    " + "-" * (n * (col_width + 1) - 1)

    lines = [header, sep]
    for i, row in enumerate(matrix):
        row_str = " ".join(f"{val:>{col_width}d}" for val in row)
        lines.append(f"{elements[i]:>2} | {row_str}")
    return "\n".join(lines)


def format_pairs(
    pairs: Iterable[Tuple[int, int]],
    highlight: Optional[Set[Tuple[int, int]]] = None,
    per_line: int = 8,
) -> str:
    items: List[str] = []
    highlight = highlight or set()
    for p in pairs:
        mark = "*" if p in highlight else " "
        items.append(f"{mark}({p[0]},{p[1]})")

    lines: List[str] = []
    for i in range(0, len(items), per_line):
        lines.append(" ".join(items[i : i + per_line]))
    return "\n".join(lines) if lines else "(빈 집합)"


def draw_graph(matrix: Matrix, elements: List[int], out_path: str) -> None:
    try:
        import networkx as nx  # type: ignore
        import matplotlib  # type: ignore
        # 비대화형 저장을 위해 Agg 백엔드 사용 (macOS GUI 경고 방지)
        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        print(
            "[경고] networkx/matplotlib을 불러올 수 없어 그래프 생성을 건너뜁니다.",
            file=sys.stderr,
        )
        return

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    g = nx.DiGraph()
    g.add_nodes_from(elements)
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                g.add_edge(elements[i], elements[j])

    plt.figure(figsize=(5.5, 5.0))
    pos = nx.spring_layout(g, seed=42)
    nx.draw_networkx_nodes(g, pos, node_color="#4C78A8", node_size=900)
    nx.draw_networkx_labels(g, pos, font_color="white", font_size=12)
    nx.draw_networkx_edges(
        g, pos, edge_color="#9ecae9", arrows=True, arrowsize=15, width=1.8
    )
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()

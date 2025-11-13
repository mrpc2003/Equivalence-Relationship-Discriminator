from typing import List, Tuple, Dict, Set

Matrix = List[List[int]]

def is_reflexive(matrix: Matrix) -> bool:
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] != 1:
            return False
    return True


def is_symmetric(matrix: Matrix) -> bool:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def is_transitive(matrix: Matrix) -> bool:
    n = len(matrix)
    for i in range(n):
        for k in range(n):
            if matrix[i][k] == 1:
                for j in range(n):
                    if matrix[k][j] == 1 and matrix[i][j] == 0:
                        return False
    return True


def is_equivalence(matrix: Matrix) -> Tuple[bool, Dict[str, bool]]:
    ref = is_reflexive(matrix)
    sym = is_symmetric(matrix)
    tra = is_transitive(matrix)
    return (ref and sym and tra), {"reflexive": ref, "symmetric": sym, "transitive": tra}


def reflexive_closure(matrix: Matrix) -> Matrix:
    n = len(matrix)
    result = [row[:] for row in matrix]
    for i in range(n):
        result[i][i] = 1
    return result


def symmetric_closure(matrix: Matrix) -> Matrix:
    n = len(matrix)
    result = [row[:] for row in matrix]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1 or matrix[j][i] == 1:
                result[i][j] = 1
                result[j][i] = 1
    return result


def transitive_closure(matrix: Matrix) -> Matrix:
    n = len(matrix)
    result = [row[:] for row in matrix]
    for k in range(n):
        for i in range(n):
            if result[i][k] == 1:
                for j in range(n):
                    if result[k][j] == 1:
                        result[i][j] = 1
    return result


def equivalence_closure(matrix: Matrix) -> Matrix:
    """
    입력 관계 R에 대해, R을 포함하는 최소의 동치 관계(반사·대칭·추이)를 생성한다.
    구현: 대칭 폐포 → 추이 폐포 → 반사 폐포 순으로 적용.
    (대칭인 관계의 추이 폐포는 대칭성을 유지하므로, 마지막에 반사만 보장하면 충분)
    """
    # 대칭 폐포
    sym = symmetric_closure(matrix)
    # 추이 폐포
    tra = transitive_closure(sym)
    # 반사 폐포
    return reflexive_closure(tra)


def to_pairs(matrix: Matrix, elements: List[int]) -> List[Tuple[int, int]]:
    n = len(matrix)
    pairs: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                pairs.append((elements[i], elements[j]))
    return pairs


def equivalence_classes(matrix: Matrix, elements: List[int]) -> List[Set[int]]:
    """
    동치 관계(반사·대칭·추이)를 가정하고 동치류를 반환한다.
    구현은 DSU(Union-Find)를 사용해 (i,j)와 (j,i)가 모두 1인 경우 같은 집합으로 합친다.
    """
    n = len(matrix)

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1 and matrix[j][i] == 1:
                union(i, j)

    groups: Dict[int, Set[int]] = {}
    for idx in range(n):
        root = find(idx)
        groups.setdefault(root, set()).add(elements[idx])

    return list(groups.values())


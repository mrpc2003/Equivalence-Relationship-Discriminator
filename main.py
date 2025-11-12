import os
from typing import List, Tuple, Set

from relations import (
    Matrix,
    is_reflexive,
    is_symmetric,
    is_transitive,
    is_equivalence,
    reflexive_closure,
    symmetric_closure,
    transitive_closure,
    to_pairs as rel_to_pairs,
    equivalence_classes,
)
from pretty import format_matrix, format_pairs, draw_graph


ELEMENTS: List[int] = [1, 2, 3, 4, 5]
N = len(ELEMENTS)


def print_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"{title}")
    print("=" * 70)


def print_sub(title: str) -> None:
    print("\n" + "-" * 50)
    print(f"{title}")
    print("-" * 50)


def parse_row(line: str) -> List[int]:
    parts = line.strip().split()
    if len(parts) != N:
        raise ValueError(f"{N}개의 0/1 값을 공백으로 입력해야 합니다.")
    row = []
    for p in parts:
        if p not in ("0", "1"):
            raise ValueError("0 또는 1만 입력 가능합니다.")
        row.append(int(p))
    return row


def input_matrix() -> Matrix:
    print_section("관계 행렬 입력 (A = {1,2,3,4,5})")
    print("각 행을 공백으로 구분된 0/1 다섯 개로 입력하세요. (총 5행)")
    matrix: Matrix = []
    r = 1
    while r <= N:
        try:
            line = input(f"행 {r} 입력: ")
            row = parse_row(line)
            matrix.append(row)
            r += 1
        except Exception as e:
            print(f"[오류] {e} 다시 입력해주세요.")
    return matrix


def print_properties(matrix: Matrix) -> Tuple[bool, bool, bool, bool]:
    is_eq, props = is_equivalence(matrix)
    ref = props["reflexive"]
    sym = props["symmetric"]
    tra = props["transitive"]
    print_sub("성질 판별 결과")
    print(f"반사(reflexive): {'예' if ref else '아니오'}")
    print(f"대칭(symmetric): {'예' if sym else '아니오'}")
    print(f"추이(transitive): {'예' if tra else '아니오'}")
    print(f"동치관계 여부: {'동치 관계입니다.' if is_eq else '동치 관계가 아닙니다.'}")
    return is_eq, ref, sym, tra


def show_matrix_and_pairs(title: str, matrix: Matrix, highlight: Set[Tuple[int, int]] | None = None) -> None:
    print_sub(title)
    print("[행렬]")
    print(format_matrix(matrix, ELEMENTS))
    print("\n[관계쌍]")
    pairs = rel_to_pairs(matrix, ELEMENTS)
    print(format_pairs(pairs, highlight=highlight))


def prompt_yes_no(question: str, default: bool = False) -> bool:
    while True:
        suffix = "y/n"
        default_mark = "y" if default else "n"
        ans = input(f"{question} ({suffix}) [{default_mark}]: ").strip().lower()
        if ans == "" or ans is None:
            return default
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("y 또는 n으로 입력해주세요.")


def prompt_menu(title: str, options: List[Tuple[str, str]], default_index: int = 1) -> int:
    print_section(title)
    for idx, (_, label) in enumerate(options, start=1):
        print(f"{idx}. {label}")
    while True:
        raw = input(f"번호를 선택하세요 [{default_index}]: ").strip()
        if raw == "":
            return default_index
        if raw.isdigit():
            val = int(raw)
            if 1 <= val <= len(options):
                return val
        print("유효한 번호를 입력해주세요.")


def prompt_text(question: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{question}{suffix}: ").strip()
    if raw == "" and default is not None:
        return default
    return raw


def process_closure(
    name: str,
    matrix: Matrix,
    outdir: str | None,
    save_graph: bool,
) -> None:
    if name == "reflexive":
        after = reflexive_closure(matrix)
        label = "반사 폐포 (Reflexive Closure)"
        file_stub = "reflexive"
    elif name == "symmetric":
        after = symmetric_closure(matrix)
        label = "대칭 폐포 (Symmetric Closure)"
        file_stub = "symmetric"
    elif name == "transitive":
        after = transitive_closure(matrix)
        label = "추이 폐포 (Transitive Closure)"
        file_stub = "transitive"
    else:
        return

    print_section(label)
    before_pairs = set(rel_to_pairs(matrix, ELEMENTS))
    after_pairs = set(rel_to_pairs(after, ELEMENTS))
    added = after_pairs - before_pairs

    show_matrix_and_pairs("변환 전", matrix)
    show_matrix_and_pairs("변환 후 (추가된 쌍에 * 표시)", after, highlight=added)

    if save_graph and outdir:
        os.makedirs(outdir, exist_ok=True)
        from_path = os.path.join(outdir, f"graph_before_{file_stub}.png")
        to_path = os.path.join(outdir, f"graph_{file_stub}.png")
        draw_graph(matrix, ELEMENTS, from_path)
        draw_graph(after, ELEMENTS, to_path)
        print(f"\n[그래프 저장] {from_path}, {to_path}")

    is_eq, ref, sym, tra = print_properties(after)
    if is_eq:
        print_sub("동치류")
        classes = equivalence_classes(after, ELEMENTS)
        for cls in classes:
            print(f"{{{', '.join(map(str, sorted(cls)))}}}")


def process_equivalence_closure(
    matrix: Matrix,
    outdir: str | None,
    save_graph: bool,
) -> None:
    from relations import equivalence_closure

    print_section("동치 폐포 (Equivalence Closure)")
    before_pairs = set(rel_to_pairs(matrix, ELEMENTS))
    after = equivalence_closure(matrix)
    after_pairs = set(rel_to_pairs(after, ELEMENTS))
    added = after_pairs - before_pairs

    show_matrix_and_pairs("변환 전", matrix)
    show_matrix_and_pairs("변환 후 (추가된 쌍에 * 표시)", after, highlight=added)

    if save_graph and outdir:
        os.makedirs(outdir, exist_ok=True)
        before_path = os.path.join(outdir, "graph_before_equiv.png")
        after_path = os.path.join(outdir, "graph_equiv.png")
        draw_graph(matrix, ELEMENTS, before_path)
        draw_graph(after, ELEMENTS, after_path)
        print(f"\n[그래프 저장] {before_path}, {after_path}")

    is_eq, ref, sym, tra = print_properties(after)
    if is_eq:
        print_sub("동치류")
        classes = equivalence_classes(after, ELEMENTS)
        for cls in classes:
            print(f"{{{', '.join(map(str, sorted(cls)))}}}")


def load_example(name: str) -> Matrix:
    # 추가 기능: 예제 행렬 로드
    if name == "even":  # 홀짝으로 나뉘는 동치 관계
        return [
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
        ]
    if name == "non_equiv":  # 비동치 예시
        return [
            [0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ]
    raise ValueError("알 수 없는 예제 이름입니다. (even | non_equiv)")


def main() -> None:
    # 실행 모드 선택
    choice = prompt_menu(
        "실행 모드 선택",
        options=[
            ("manual", "수동 입력(행렬 직접 입력)"),
            ("even", "예제: 홀짝 동치 (even)"),
            ("non_equiv", "예제: 비동치 (non_equiv)"),
        ],
        default_index=1,
    )
    if choice == 1:
        matrix = input_matrix()
        example_name = None
    elif choice == 2:
        matrix = load_example("even")
        example_name = "even"
        print_section("예제 불러오기: even")
    else:
        matrix = load_example("non_equiv")
        example_name = "non_equiv"
        print_section("예제 불러오기: non_equiv")

    # 그래프 저장 옵션
    save_graph = prompt_yes_no("그래프 이미지를 저장하시겠습니까?", default=False)
    outdir = None
    if save_graph:
        outdir = prompt_text("그래프 출력 디렉터리를 입력하세요", default="outputs")

    print_section("원본 관계 R")
    show_matrix_and_pairs("원본 R", matrix)
    if save_graph and outdir:
        os.makedirs(outdir, exist_ok=True)
        out_path = os.path.join(outdir, "graph_original.png")
        draw_graph(matrix, ELEMENTS, out_path)
        print(f"\n[그래프 저장] {out_path}")

    is_eq, ref, sym, tra = print_properties(matrix)
    if is_eq:
        print_sub("동치류")
        classes = equivalence_classes(matrix, ELEMENTS)
        for cls in classes:
            print(f"{{{', '.join(map(str, sorted(cls)))}}}")

    # 검토사항 반영: 없는 성질에 대해서만 해당 폐포 생성/출력
    if not ref:
        process_closure("reflexive", matrix, outdir, save_graph)
    if not sym:
        process_closure("symmetric", matrix, outdir, save_graph)
    if not tra:
        process_closure("transitive", matrix, outdir, save_graph)

    # 추가 기능: 동치 폐포(한 번에)도 생성할지 여부
    if not is_eq:
        if prompt_yes_no("동치 폐포(한 번에)도 생성/확인할까요?", default=True):
            process_equivalence_closure(matrix, outdir, save_graph)


if __name__ == "__main__":
    main()


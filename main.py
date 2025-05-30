# 制約プログラミングを使用したSumpleteソルバー
# Gemini 2.5 Flashの支援を受けて開発

from constraint import Problem

def solve_sumplete(grid, row_sums, col_sums):
    """
    Sumpleteパズルを制約充足問題 (CSP) として解く関数。

    Args:
        grid (list of list of int): パズル盤面の数字のグリッド。
        row_sums (list of int): 各行の目標合計値。
        col_sums (list of int): 各列の目標合計値。

    Returns:
        dict or None: 解が見つかった場合は、各セル(i, j)に対する0(除外)または1(選択)の辞書。
                      解が見つからない場合はNone。
    """
    R = len(grid)
    C = len(grid[0])
    problem = Problem()

    # 変数定義: x_i_j は grid[i][j] が合計に含まれるか (1) 除外されるか (0) を表す
    variables = [(i, j) for i in range(R) for j in range(C)]
    problem.addVariables(variables, [0, 1])

    # 行の合計制約を追加
    for i in range(R):
        row_vars = [(i, j) for j in range(C)]
        row_values = [grid[i][j] for j in range(C)]
        target_sum = row_sums[i] # ここで行の目標値をキャプチャ

        # 制約関数 (キーワード引数で値をキャプチャ)
        def row_sum_constraint(*vals, row_values=row_values, target_sum=target_sum):
            current_sum = sum(v * val for v, val in zip(row_values, vals))
            return current_sum == target_sum
        
        problem.addConstraint(row_sum_constraint, row_vars)

    # 列の合計制約を追加
    for j in range(C):
        col_vars = [(i, j) for i in range(R)]
        col_values = [grid[i][j] for i in range(R)]
        target_sum = col_sums[j] # ここで列の目標値をキャプチャ

        # 制約関数 (キーワード引数で値をキャプチャ)
        def col_sum_constraint(*vals, col_values=col_values, target_sum=target_sum):
            current_sum = sum(v * val for v, val in zip(col_values, vals))
            return current_sum == target_sum
        
        problem.addConstraint(col_sum_constraint, col_vars)

    # 最初の解を見つける
    solution = problem.getSolution()
    return solution

def print_sumplete_solution_ox(solution, R, C):
    """
    Sumpleteの解を'O' (選択) と 'X' (除外) で表示する関数。

    Args:
        solution (dict): problem.getSolution() から得られる解の辞書。
                         キーは (行, 列) のタプル、値は0(除外)または1(選択)。
        R (int): グリッドの行数。
        C (int): グリッドの列数。
    """
    if solution is None:
        print("No solution to display.")
        return

    print("\nSumplete Solution (O: Selected, X: Excluded):")
    for r in range(R):
        for c in range(C):
            # solution辞書から(r, c)の値を参照
            # .get((r,c), 0) はキーが存在しない場合にデフォルト値0を返す（念のため）
            if solution.get((r, c), 0) == 1:
                print("O", end="\t") # 選択された場合
            else:
                print("X", end="\t") # 除外された場合
        print() # 次の行へ

if __name__ == "__main__":
    grid = [
        [5, 8, 2, 7, 2, 9, 1],
        [5, 6, 3, 8, 9, 4, 4],
        [9, 7, 1, 8, 8, 6, 6],
        [5, 7, 6, 6, 6, 1, 8],
        [6, 3, 8, 5, 9, 5, 1],
        [4, 4, 8, 6, 4, 4, 7],
        [2, 2, 2, 4, 3, 8, 2]
    ]
    row_sums = [8, 26, 28, 14, 20, 22, 16]
    col_sums = [18, 21, 10, 29, 18, 23, 15]
    solution = solve_sumplete(grid, row_sums, col_sums)
    print_sumplete_solution_ox(solution, len(grid), len(grid[0]))

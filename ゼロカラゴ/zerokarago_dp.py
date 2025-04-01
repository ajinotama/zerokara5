import matplotlib.pyplot as plt
import japanize_matplotlib
from math import factorial, prod
from collections import Counter, defaultdict
from scipy.special import comb
from itertools import combinations_with_replacement, combinations
import datetime


dp_cache = {}

def find_partitions(k):
    """ 和が k になる 1以上の整数の組み合わせを DP で求める（キャッシュ対応） """
    def backtrack(target, start, path, result):
        if target == 0:
            result.append(path[:])
            return
        for i in range(start, k + 1):
            if i > target:
                break
            backtrack(target - i, i, path + [i], result)


    if k in dp_cache:
        return dp_cache[k]
    # DPテーブルの初期化
    dp = defaultdict(list)
    dp[0] = [[]]  # 和が0のときの組み合わせは空リスト（1通り）

    result = []
    backtrack(k, 1, [], result)
    dp[k] = result
    return result


def find_valid_partitions(k):
    """ 和が k になる組を求め、和が k/2 になる2分割を列挙 """
    target_sum = k // 2
    valid_partitions = set()

    for partition in find_partitions(k):
      for i in range(1, len(partition)):
        for group1 in combinations(partition, i):
            if sum(group1) == target_sum:
                group2 = list(partition)
                for x in group1:
                    group2.remove(x)
                
                # 2つのグループを1つのリストに統合し、ソート
                merged_partition = tuple(sorted(list(group1) + group2))
                valid_partitions.add(merged_partition)

    # 出力形式を aabbbccc のように変換
    return [''.join(chr(97+i)*x for i,x in enumerate(partition)) for partition in sorted(valid_partitions)]



def multi_comb(n, *denominators):
    """ n! を複数の分母階乗で割る計算を最適化 """
    return factorial(n) // prod(factorial(d) for d in denominators)


def chohuku_comb(array):
    """ 重複組み合わせの計算 """
    array_counter = Counter(array)
    return multi_comb(sum(array_counter.values()), *array_counter.values())


valid_partitions_cache = {}

def calc_zerokaraN_probability(n, k):
    print(f'n={n}\tk={k}\t{datetime.datetime.now()}')
    """ ゼロカラNを試行し、1回で組み分けが成功する確率 """
    if k in valid_partitions_cache:
        valid_partitions = valid_partitions_cache[k]
    else:
        valid_partitions = find_valid_partitions(k)
        valid_partitions_cache[k] = valid_partitions
    bunbo = (n + 1) ** k
    bunshi = sum(
        comb(n + 1, len(Counter(pattern))) * chohuku_comb(Counter(pattern).values()) * chohuku_comb(pattern)
        for pattern in valid_partitions
    )
    return bunshi / bunbo * 100


K_MAX = 5
X_MAX = 30
x_member = [i for i in range(1, X_MAX + 1) if i % 2 == 0]
fig, ax = plt.subplots(figsize=(12.0,6.0))

for k in range(1, K_MAX + 1):
    y = [calc_zerokaraN_probability(k, x) for x in x_member]
    ax.plot(x_member, y, label=f'ゼロカラ{k}')

ax.set_title('1回の試行で2組に分かれる確率')
ax.set_xlabel('人数')
ax.set_ylabel('確率')
ax.set_xticks(x_member)
ax.grid()
ax.legend(loc=3)
plt.show()

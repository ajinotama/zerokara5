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
    if k in dp_cache:
        return dp_cache[k]
    
    dp = defaultdict(list)
    dp[0] = [[]]  # 0を作る方法は空リスト1つ

    for num in range(1, k + 1):
        for i in range(k, num - 1, -1):
            dp[i] += [combination + [num] for combination in dp[i - num]]

    dp_cache[k] = dp[k]
    return dp[k]


def find_valid_partitions(k):
    """ 和が k になる組を求め、和が k/2 になる2分割を列挙 """
    target_sum = k // 2
    valid_partitions = set()

    # 和が k になる 1以上の整数の組み合わせを列挙
    for n in range(1, k + 1):  # 要素数を1〜kまで変えて試す
        for partition in combinations_with_replacement(range(1, k + 1), n):
            if sum(partition) != k:
                continue  # 和が k ちょうどでないものはスキップ

            # 部分集合の分割を試す
            for i in range(1, len(partition)):  # 1個以上選ぶ
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
X_MAX = 20
x_member = [i * 2 for i in range(1, X_MAX)]
fig, ax = plt.subplots()

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

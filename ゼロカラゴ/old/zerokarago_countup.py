
import matplotlib.pyplot as plt
import japanize_matplotlib

from math import factorial, prod
from collections import Counter
from scipy.special import comb
from itertools import combinations_with_replacement, combinations


def find_valid_partitions(k):
    """ 
    和が k になる 1以上の整数の組み合わせを列挙し、条件を満たす分割を探す

    ex. k=6 -> aaabbc,aaabcd,aabbcd,abcdee...
    """
    if k % 2 != 0:
        return []  # k が奇数なら分割不可能

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
    #print(valid_partitions)
    return [''.join(chr(97+i)*x for i,x in enumerate(partition)) for partition in sorted(valid_partitions)]


def multi_comb(n, *denominators):
    """ n! を複数の分母階乗で割る計算を最適化 """
    res = 1
    denom_factors = []  # 分母の因子をリストで保持
    
    # 分母の階乗を個別の因子に分解
    for d in denominators:
        denom_factors.extend(range(1, d + 1))
    
    # 分子の計算をしながら分母で割る
    for i in range(1, n + 1):
        res *= i  # 分子の n! を計算
        while denom_factors and res % denom_factors[0] == 0:
            res //= denom_factors.pop(0)  # すぐに割る

    return res


def chohuku_comb(array: list) -> int: 
    """
    重複組み合わせを計算する

    ex. input: abbccc -> output: 6!/1!/2!/3!
    """
    array_counter = Counter(array)
    #bunbo = prod([factorial(x) for x in array_counter.values()])
    #bunshi = factorial(sum(array_counter.values()))
    return multi_comb(sum(array_counter.values()), *array_counter.values())
    #return bunshi // bunbo


def calc_zerokaraN_probability(n,k):
    """
    ゼロカラNを試行し、1回で組み分けが成功する確率

    ex. n=5,k=6 -> 0~5までの数字を6人で出し合うとき、1回で組み分けが成功する確率
    """
    valid_partitions = find_valid_partitions(k)
    bunbo = (n+1)**k
    bunshi = 0
    for pattern in valid_partitions:
        pattern_counter = Counter(pattern)
        c = comb(n+1, len(pattern_counter)) * chohuku_comb(pattern_counter.values()) * chohuku_comb(pattern)
        #print(f'{comb(n+1, len(pattern_counter))}*{chohuku_comb(pattern_counter.values())}*{chohuku_comb(pattern)}={c}')
        bunshi += c
    return bunshi / bunbo * 100



x_member = [i*2 for i in range(1,8)]
y_gupa    = [calc_zerokaraN_probability(1,x) for x in x_member]
y_zeroka2 = [calc_zerokaraN_probability(2,x) for x in x_member]
y_zeroka3 = [calc_zerokaraN_probability(3,x) for x in x_member]
y_zeroka4 = [calc_zerokaraN_probability(4,x) for x in x_member]
y_zeroka5 = [calc_zerokaraN_probability(5,x) for x in x_member]

fig, ax = plt.subplots()
ax.set_title('1回の試行で2組に分かれる確率')
ax.set_xlabel('人数')
ax.set_ylabel('確率')
ax.set_xticks(x_member)
ax.grid()
ax.plot(x_member, y_gupa, label='グーパー')
ax.plot(x_member, y_zeroka2, label='ゼロカラニ')
ax.plot(x_member, y_zeroka3, label='ゼロカラサン')
ax.plot(x_member, y_zeroka4, label='ゼロカラヨン')
ax.plot(x_member, y_zeroka5, label='ゼロカラゴ')
ax.legend(loc=3)

plt.show()

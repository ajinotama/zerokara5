import matplotlib.pyplot as plt
import japanize_matplotlib
from math import factorial, prod
from collections import Counter, defaultdict
from scipy.special import comb
from itertools import combinations_with_replacement, combinations
import datetime


dp_cache = {}

def find_partitions(p: int) -> list:
    """
    x_1 + x_2 + ... = p となる x の組み合わせを列挙します。
    ただし、組み合わせの要素数は FINGER_MAX 以下 とします。

    例えば、p=4 の場合、出力される x の組み合わせは以下の通りです：
        [[4], [3,1], [2,1,1], [2,2], [1,1,1,1]]
    これらは、次のような等式を表しています：
        4=4, 3+1=4, 2+1+1=4, 2+2=4, 1+1+1+1=4
    また、2+1+1=4 という組み合わせは、
    「2人が同じ本数の指を出し、もう2人が別の本数の指を出し、さらに1人が別の本数の指を出している」パターンを表しています。
    例えば [2,1,1] の場合、
    A君とB君 が3本の指、C君 が4本の指、D君 が5本の指を出しているようなパターンが含まれています。
    
    Parameters
    ----------
    p : int
        組み分けする人数

    Result
    ------
    result : list
        x_1 + x_2 + ... = p となるxの組    
    """
    def backtrack(target, start, path, result):
        if target == 0:
            result.append(path[:])
            return
        if len(path) > FINGER_MAX:
            return
        for i in range(start, p + 1):
            if i > target:
                break
            backtrack(target - i, i, path + [i], result)


    if p in dp_cache:
        return dp_cache[p]
    dp = defaultdict(list)
    dp[0] = [[]] 
    result = []
    backtrack(p, 1, [], result)
    dp[p] = result
    return result


def find_valid_partitions(p: int) -> list:
    """
    x_1 + x_2 + ... = p となる x の組み合わせの中で、2つのグループに分けたとき、それぞれの合計が p/2 になるもの を探し、文字列の形で列挙します。
    例えば、p=4 の場合、x の組み合わせは以下の通りです：
        [[4], [3,1], [2,1,1], [2,2], [1,1,1,1]]
    この中で、2つの部分集合に分割して合計がそれぞれ p/2 = 2 になるものは、以下の3つです：
        [[2,1,1], [2,2], [1,1,1,1]]
    これらを文字列に変換すると、
        ['aabc', 'aabb' , 'abcd']
    となります。

    例えば [2,1,1] の場合、A君とB君が3本の指、C君が4本の指、D君が5本の指を出しているパターンを含んでいます。
    このとき (A,B)(C,D) とすることで、ゼロカラゴによる組み分けが出来ることを表しています。

    Parameters
    ----------
    p : int
        組み分けする人数
    
    Return
    ------
    result : list
        文字列のリスト
    """
    target_sum = p // 2
    valid_partitions = set()

    for partition in find_partitions(p):
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
    result = [''.join(chr(97+i)*x for i,x in enumerate(partition)) for partition in sorted(valid_partitions)]
    return result


def multi_comb(n: int, *denominators: tuple) -> float:
    """
    重複組み合わせの階乗計算を最適化します。
    
    Parameters
    ----------
    n : int
        分子の値 (ex. 6)
    *denominators : tuple
        分母の値のtuple (ex. [3,2,1])
        
    Return
    ------
    return : float
        計算結果 (ex. 6!/(3!2!1!) = 60)
    """
    result = factorial(n) // prod(factorial(d) for d in denominators)
    return result


def chohuku_comb(lst: list) -> float:
    """
    重複組み合わせの計算をします。

    Parameters
    ----------
    lst : list
        (ex. [1,1,1,2,2,3])
    
    Returns
    -------
    result : float
        計算結果 (ex. 6!/(3!2!1!) = 60)
    """
    array_counter = Counter(lst)
    result = multi_comb(sum(array_counter.values()), *array_counter.values())
    return result


valid_partitions_cache = {}

def calc_zerokaraN_probability(finger: int, player: int) -> float:
    """
    ゼロカラ{finger}を試行し、1回で組み分けが成功する確率を求めます。
    
    Parameters
    ----------
    finger : int
        組み分け字に使用する指の本数
    player : int
        組み分けする人数

    Returns
    -------
    p : float
        1回で組み分けが成功する確率
    """
    print(f'f={finger}\tp={player}\t{datetime.datetime.now()}')
    if player in valid_partitions_cache:
        valid_partitions = valid_partitions_cache[player]
    else:
        valid_partitions = find_valid_partitions(player)
        valid_partitions_cache[player] = valid_partitions
    bunbo = (finger + 1) ** player
    bunshi = sum(
        comb(finger + 1, len(Counter(pattern))) * chohuku_comb(Counter(pattern).values()) * chohuku_comb(pattern)
        for pattern in valid_partitions
    )
    p = bunshi / bunbo * 100
    return p


FINGER_MAX = 5
PLAYER_MAX = 30
players = [i for i in range(1, PLAYER_MAX + 1) if i % 2 == 0]
fig, ax = plt.subplots(figsize=(12.0,6.0))

for finger in range(1, FINGER_MAX + 1):
    y = [calc_zerokaraN_probability(finger, player) for player in players]
    ax.plot(players, y, label=f'ゼロカラ{finger}')

ax.set_title('1回の試行で2組に分かれる確率')
ax.set_xlabel('人数')
ax.set_ylabel('確率')
ax.set_xticks(players)
ax.set_yticks([i * 10 for i in range(1,11)])
ax.grid()
ax.legend(loc=3)
plt.show()

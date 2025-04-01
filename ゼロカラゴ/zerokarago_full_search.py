import itertools
from collections import Counter
from scipy.special import comb
import matplotlib.pyplot as plt
import japanize_matplotlib

def calc_zerokaraN_probability(n, member):
    pattern_total = (n + 1) ** member
    pattern_ok_count = 0
    for pattern in itertools.product(range(n + 1),repeat=member):
        counter = Counter(pattern)
        counts = list(counter.values())
        
        # すべての要素が同じ値である場合（例: [3,3,3,3,3,3])
        if len(counter) == 1:
            continue

        # 異なる値がすべて同じ回数で出現する場合（例: [0,0,0,2,2,2] [1,1,3,3,5,5] [0,1,2,3,4,5]）
        if len(set(counts)) == 1:
            pattern_ok_count += 1
            continue

        # リストの半数が同じ値の場合（例: [1,1,1,2,3,4] [0,0,0,1,2,2])
        if member // 2 in counts:
            pattern_ok_count += 1

    return pattern_ok_count / pattern_total * 100

def calc_gutopa_probability(member):
    pattern_total = 2 ** member
    pattern_ok_count = comb(member, member // 2, exact=True)
    return pattern_ok_count / pattern_total * 100


x_member = [2,4,6]
y_gutopa = [calc_gutopa_probability(x) for x in x_member]
y_zeroka2 = [calc_zerokaraN_probability(2,x) for x in x_member]
y_zeroka3 = [calc_zerokaraN_probability(3,x) for x in x_member]
y_zeroka4 = [calc_zerokaraN_probability(4,x) for x in x_member]
y_zeroka5 = [calc_zerokaraN_probability(5,x) for x in x_member]

fig, ax = plt.subplots()
ax.set_xlabel('人数')
ax.set_ylabel('確率')
ax.set_xticks(x_member)
ax.plot(x_member, y_gutopa, label='グーパー')
ax.plot(x_member, y_zeroka2, label='ゼロカラニ')
ax.plot(x_member, y_zeroka3, label='ゼロカラサン')
ax.plot(x_member, y_zeroka4, label='ゼロカラヨン')
ax.plot(x_member, y_zeroka5, label='ゼロカラゴ')

ax.legend(loc=3)
plt.show()

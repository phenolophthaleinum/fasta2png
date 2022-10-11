from operator import itemgetter
import time


# def cmp(a, b):
#     return (a > b) - (a < b)
#
#
# def bwt3(s):
#     n = len(s)
#     ids = sorted(range(n), key=lambda x, y: rcmp(s, x, y))
#     last_colum = [s[(i-1) % n] for i in ids]
#     return "".join(last_colum), ids.index(0)
#
#
# def rcmp(s, i, j):
#     x = s[i:]+s[:i]
#     y = s[j:]+s[:j]
#     return cmp(x, y)
#
#
# def test():
#     s = "this is the demo program of bwt transform in the real programming code"
#     p = bwt3(s)
#     print("bwt3(s) ==>", p)
#
#
# if __name__ == "__main__":
#     test()
def bw_transform(s):
    n = len(s)
    m = sorted((s[i:]+s[:i] for i in range(n)))
    # print(m)
    I = m.index(s)
    L = ''.join((q[-1] for q in m))
    return I, L


def bw_restore(I, L):
    n = len(L)
    X = sorted([(i, x) for i, x in enumerate(L)], key=itemgetter(1))
    # print(X)

    T = [None for i in range(n)]
    # print(T)
    for i, y in enumerate(X):
        j, _ = y
        print(j)
        T[j] = i
    # print(T)

    Tx = [I]
    # print(Tx)
    for i in range(1, n):
        Tx.append(T[Tx[i-1]])
    # print(Tx)

    # test = [I]
    # test = [test.append(T[test[i-1]]) for i in range(1, n)]
    # print(test)

    S = [L[i] for i in Tx]
    S = ''.join(S)
    return S[::-1]


def rotations(t):
    """ Return list of rotations of input string t """
    tt = t * 2
    return [tt[i:i+len(t)] for i in range(0, len(t))]


def bwm(t):
    """ Return lexicographically sorted list of t’s rotations """
    return sorted(rotations(t))


def bwtViaBwm(t):
    """ Given T, returns BWT(T) by way of the BWM """
    return ''.join(map(lambda x: x[-1], bwm(t)))


def rankBwt(bw):
    """ Given BWT string bw, return parallel list of B-ranks.  Also
        returns tots: map from character to # times it appears. """
    tots = dict()
    ranks = []
    for c in bw:
        if c not in tots: tots[c] = 0
        ranks.append(tots[c])
        tots[c] += 1
    return ranks, tots


def firstCol(tots):
    """ Return map from character to the range of rows prefixed by
        the character. """
    first = {}
    totc = 0
    for c, count in sorted(tots.items()):
        first[c] = (totc, totc + count)
        totc += count
    return first


def reverseBwt(bw):
    """ Make T from BWT(T) """
    ranks, tots = rankBwt(bw)
    first = firstCol(tots)
    rowi = 0  # start in first row
    t = '$'  # start with rightmost character
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t  # prepend to answer
        # jump to row that starts with c of same rank
        rowi = first[c][0] + ranks[rowi]
    return t


if __name__ == "__main__":
    tic = time.perf_counter()
    trans1 = bw_transform("politechnika jest jebana")
    reverted1 = bw_restore(20, trans1[-1])
    toc = time.perf_counter()
    elapsed_time = toc - tic
    print("first way:")
    print(trans1)
    print(reverted1)
    print(f"elapsed time: {elapsed_time:0.8f} seconds")
    tic = time.perf_counter()
    trans2 = bwtViaBwm("politechnika jest jebana")
    reverted2 = reverseBwt(trans2)
    toc = time.perf_counter()
    elapsed_time = toc - tic
    print("second way:")
    print(trans2)
    print(reverted2)
    print(f"elapsed time: {elapsed_time:0.8f} seconds")

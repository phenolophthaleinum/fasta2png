import sys
import zlib
import random
import math
import itertools
import ruamel.yaml
from memory_profiler import profile
from pathlib import Path
import pyfastx
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed
import numpy as np


subs = {
    "A": "CTG",
    "C": "ATG",
    "T": "ACG",
    "G": "ACT"
}


def generate_sequence(l):
    return ''.join(random.choice('ACTG') for _ in range(l))


def read_seqs(dir):
    files = list(Path(dir).glob("*"))
    return {file.stem: [r for r in pyfastx.Fasta(str(file), build_index=False)][0][1] for file in files}


def similarity(seq, identity):
    l = len(seq)

    # print((1 - identity) * l)
    samples = random.sample(range(0, l - 1), math.ceil((1 - identity) * l))
    print(len(samples) == len(set(samples)))
    # print(f"Before: {''.join(seq)}")
    for i in samples:
        seq[i] = random.choice(subs[seq[i]])
    # print(f"After: {''.join(seq)}")
    return ''.join(seq)


def shuffle_seq(seq, seed):
    temp = seq
    random.seed(seed)
    random.shuffle(temp)
    return ''.join(temp)


def complexity(s):
    s = s.encode("utf-8")
    compr = zlib.compress(s)
    c = float(len(compr))
    return c


def ncd(s1, s2):
    c1 = complexity(s1)
    c2 = complexity(s2)
    c12 = complexity(s1 + s2)
    return c12 / max(c1, c2)


def ncd_parallel_wrapper(s, seqs):
    return [s[0], s[1], ncd(seqs[s[0]], seqs[s[1]])]


def partition_queries(pairs, partitions: int = 16 - 1):
    partitions = np.array_split(np.array(pairs), partitions)
    # debug for partitions
    # print(partitions)
    # print([ar.shape for ar in partitions])
    return partitions


def batch_exec(pair_batch, seqs):
    return [ncd_parallel_wrapper(s, seqs) for s in pair_batch]


def ncd_pairwise(pairs, seqs, name, parallel):
    if parallel:
        data = Parallel(n_jobs=-1, verbose=False, prefer="threads")(delayed(ncd_parallel_wrapper)(s, seqs) for s in tqdm(pairs))
        # data = Parallel(n_jobs=-1, verbose=False, prefer="threads")(delayed(batch_exec)(batch, seqs) for batch in tqdm(partition_queries(pairs)))
    else:
        data = [[s[0], s[1], ncd(seqs[s[0]], seqs[s[1]])] for s in tqdm(pairs)]
    df = pd.DataFrame.from_dict(data)
    df.to_csv(f'ncd_testing/tsv/{name}.tsv', sep='\t', header=False, index=False)


# @profile
def main():
    # old - random seqs; result to yamls
    # # probable automation-------------------------------
    # seq = generate_sequence(10000)
    # seq_100 = seq
    # seq_90 = similarity(list(seq), 0.9)
    # seq_50 = similarity(list(seq), 0.5)
    #
    # seq_100_shuffled = shuffle_seq(list(seq), seed=0)
    # seq_50_shuffled = shuffle_seq(list(seq_50), seed=0)
    #
    # seqs = {
    #     'seq_100': seq,
    #     'seq_90': seq_90,
    #     'seq_50': seq_50,
    #     'seq_100_shuffled': seq_100_shuffled,
    #     'seq_50_shuffled': seq_50_shuffled
    # }
    # # ---------------------------------------------------

    # ncd pairwise
    # pairs = list(itertools.product(seqs, repeat=2))
    # d_temp = {k: ncd(k[0], k[1]) for k in pairs}
    # res = {k[0]: {k: {'ncd': v, 'relative_diff': 0}} for k, v in d_temp.items() if k[0] == k[1]}
    # for elem in d_temp:
    #     if elem[0] != elem[1]:
    #         res[elem[0]].update({elem: {'ncd': d_temp[elem], 'relative_diff': abs(res[elem[0]][(elem[0], elem[0])]['ncd'] - d_temp[elem])}})

    # # print comparison
    # yaml = ruamel.yaml.YAML()
    # yaml.default_flow_style = None
    # print(yaml.dump(res, sys.stdout))

    # ncd to tsv
    seqs = read_seqs("ncd_testing/datasets/genome/sim_hgt/fasta")
    pairs = list(itertools.combinations(seqs, 2))
    ncd_pairwise(pairs, seqs, "sim_hgt", parallel=True)


if __name__ == '__main__':
    main()
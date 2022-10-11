from Bio import SeqIO
from PIL import Image
import dill
import zstandard
import math
import time


def get_group(seq):
    current = seq[0]
    counter = 0
    groups = []
    for bit in seq:
        if current == bit:
            counter += 1
        else:
            c = counter - 1
            code = f'{current}{c * "1"}{current}' if current == '0' else f'{current}{c * "0"}{current}'
            groups.append(code)
            current = bit
            counter = 1
    return groups


def get_group2(seq):
    current = seq[0]
    counter = 0
    groups = []
    for bit in seq:
        if current == bit:
            counter += 1
        else:
            groups.append(f'{current}{counter},')
            current = bit
            counter = 1
    return groups


code_table_R = {
    "A": 0,
    "T": 0,
    "C": 1,
    "G": 1
}
code_table_G = {
    "A": 1,
    "T": 0,
    "C": 0,
    "G": 1
}

seq_obj, = SeqIO.parse("NC_017186.fna", 'fasta')
seq = seq_obj.seq
seqR = *map(lambda base: str(code_table_R[base]), seq),
seqR = ''.join(seqR)
seqR_group = ''.join(get_group(seqR))
seqG = *map(lambda base: str(code_table_G[base]), seq),
seqG = ''.join(seqG)
seqG_group = ''.join(get_group(seqG))

# print(len(seq_obj.seq))
# p_seq = dill.dumps(seq_obj)
# print(len(p_seq))

p_seqR = dill.dumps(seqR_group)
p_seqG = dill.dumps(seqG_group)

cctx = zstandard.ZstdCompressor(level=11, threads=-1)
p_seqR_c = cctx.compress(p_seqR)
p_seqG_c = cctx.compress(p_seqG)

size = 0
if len(p_seqR_c) > len(p_seqG_c):
    size = len(p_seqR_c)
else:
    size = len(p_seqG_c)

dim = math.floor(math.sqrt(size)) + 1
target = dim * dim
diff_R = target - len(p_seqR_c)
diff_G = target - len(p_seqG_c)
n_seqR = p_seqR_c + bytes(int(diff_R))
n_seqG = p_seqG_c + bytes(int(diff_G))
# print(len(n_seq))
R_ch = Image.frombytes("L", (dim, dim), n_seqR)
G_ch = Image.frombytes("L", (dim, dim), n_seqG)
# B_ch = Image.new("L", (dim, dim))
maskmap = Image.merge("LA", (R_ch, G_ch))
maskmap.save("NC_017186_maskmap_bindlike_LA.webp", lossless=True)

from timeit import default_timer as timer
from Bio import SeqIO
import dill
import bz2
from PIL import Image
import math
import joblib
from io import BytesIO

def chunker(chunk_size, src):
    for i in range(0, len(src), chunk_size):
        yield src[i:i + chunk_size]


total_start = timer()
# seq_obj, = SeqIO.parse("X:/edwards2016/host/fasta/NC_017186.fna", 'fasta')
seq_obj, = SeqIO.parse("X:/edwards2016/caenorhabditis_elegans.fna", 'fasta')
# p_seq = dill.dumps(seq_obj)
# data_comp = bz2.compress(p_seq)
data_comp = BytesIO()
joblib.dump(seq_obj, data_comp, compress=('lzma', 3))
data_comp = data_comp.getvalue()
dim = math.floor(math.sqrt(len(data_comp))) + 1
target = dim * dim
diff = target - len(data_comp)
n_seq = data_comp + bytes(int(diff))
# chunks = list(chunker(2048, n_seq))

img = Image.frombytes('P', (int(dim), int(dim)), n_seq)
img.save(f"lzma_elegans_test_parallel.png")
total_end = timer()
total_runtime = total_end - total_start
print(f"Total elapsed time {total_runtime:.6f} seconds")

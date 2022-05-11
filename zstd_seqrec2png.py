from timeit import default_timer as timer
from Bio import SeqIO
import dill
import bz2
from PIL import Image
import math
import joblib
from io import BytesIO
import zstandard


cctx = zstandard.ZstdCompressor(level=11, threads=-1)
total_start = timer()
# seq_obj, = SeqIO.parse("X:/edwards2016/host/fasta/NC_017186.fna", 'fasta')
seq_obj, = SeqIO.parse("/home/hyperscroll/edwards2016/host/fasta/NC_017186.fna", 'fasta')
# seq_obj, = SeqIO.parse("/home/hyperscroll/edwards2016/caenorhabditis_elegans.fna", 'fasta')
# seq_obj, = SeqIO.parse("X:/edwards2016/caenorhabditis_elegans.fna", 'fasta')
# seq_obj, = SeqIO.parse("X:/edwards2016/Cmin.fna", 'fasta')
p_seq = dill.dumps(seq_obj)
data_comp = cctx.compress(p_seq)
dim = math.floor(math.sqrt(len(data_comp))) + 1
target = dim * dim
diff = target - len(data_comp)
n_seq = data_comp + bytes(int(diff))
img = Image.frombytes('P', (int(dim), int(dim)), n_seq)
img.save(f"zstd_elegans.png")
total_end = timer()
total_runtime = total_end - total_start
print(f"Total elapsed time {total_runtime:.6f} seconds")
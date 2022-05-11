import math
import dill
from Bio import SeqIO
from PIL import Image
from timeit import default_timer as timer
import c_mk_diff

total_start = timer()

# assuming single record for now
seq_obj, = SeqIO.parse("X:/edwards2016/caenorhabditis_elegans.fna", 'fasta')
# object dump
p_seq = dill.dumps(seq_obj)
# closest square root
# dim = math.floor(math.sqrt(len(p_seq))) + 1
# # final size
# target = dim * dim
# # how much needed to fill up the target
# diff = target - len(p_seq)
### cython
dim = c_mk_diff.calc_dim(len(p_seq))
diff = c_mk_diff.calc_diff(dim, len(p_seq))
###
# final data
n_seq = p_seq + bytes(int(diff))
# save image from bytes with P image mode - 8-bit pixels, mapped to any other mode using a color palette - most space saved without disrupting the data
img = Image.frombytes('P', (int(dim), int(dim)), n_seq)
img.save(f"caenohabditis_elegans_seqrec2png.png")

# timing
total_end = timer()
total_runtime = total_end - total_start
print(f"Total elapsed time (SeqRecord save to png file): {total_runtime:.6f} seconds")
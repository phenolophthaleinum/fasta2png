from Bio import SeqIO
from PIL import Image
import dill
import zstandard
import math
import time


tic = time.perf_counter()
# COMPRESSION
# parse fastq file merging all records into one strings of sequence and score
all_seq = []
all_phred = []
with open("fastqs/ERR6099228.fastq") as fq:
    for record in SeqIO.parse(fq, "fastq"):
        all_seq.append(str(record.seq))
        all_phred.extend([chr(phred + 33) for phred in record.letter_annotations['phred_quality']])
        # score as int in str is worse
        # all_phred.extend([str(phred) for phred in record.letter_annotations['phred_quality']])
    all_seq = ''.join(all_seq)
    all_phred = ''.join(all_phred)

score1 = all_phred[:len(all_phred)//2]
score2 = all_phred[len(all_phred)//2:]

# dump, compress
p_seq = dill.dumps(all_seq)
p_score1 = dill.dumps(score1)
p_score2 = dill.dumps(score2)
cctx = zstandard.ZstdCompressor(level=11, threads=-1)
p_seq_c = cctx.compress(p_seq)
p_score1_c = cctx.compress(p_score1)
p_score2_c = cctx.compress(p_score2)

# compute dimensions of image for seq and score
# TODO: check which one is bigger
dim = math.floor(math.sqrt(len(p_score2_c))) + 1
target = dim * dim
diff_score1 = target - len(p_score1_c)
diff_score2 = target - len(p_score2_c)
diff_seq = target - len(p_seq_c)
n_score1 = p_score1_c + bytes(int(diff_score1))
n_score2 = p_score2_c + bytes(int(diff_score2))
n_seq = p_seq_c + bytes(int(diff_seq))

# save data to separate images
img_score1 = Image.frombytes('P', (int(dim), int(dim)), n_score1)
img_score2 = Image.frombytes('P', (int(dim), int(dim)), n_score2)
# img_score.save("ERR6099228_score.webp", lossless=True, bits=8)
img_seq = Image.frombytes('P', (int(dim), int(dim)), n_seq)
# img_seq.save("ERR6099228_seq.webp", lossless=True, bits=8)

# create masked image in LA space
r_ch = img_seq.convert("L")
g_ch = img_score1.convert("L")
b_ch = img_score2.convert("L")
# maskmap = Image.merge("LA", (r_ch, g_ch))
# maskmap.save("ERR6099228_maskmap_LA.webp", lossless=True, bits=8)

# create masked image in RGB space
# b_ch = Image.new("L", (dim, dim))
maskmap = Image.merge("RGB", (r_ch, g_ch, b_ch))
maskmap.save("ERR6099228_maskmap_RGB_distscore.webp", lossless=True, bits=8)
toc = time.perf_counter()
elapsed_time = toc - tic
print(f"elapsed time: {elapsed_time:0.8f} seconds")

# # -----------------------------------------------------------
# # DECOMPRESSION of masked image in LA space
# tic = time.perf_counter()
# # load image
# loaded_mask = Image.open("ERR6099228_maskmap_RGB.webp")
# # decompose channels
# loaded_seq_ch, loaded_score_ch, blank = loaded_mask.split()
# # revert to bytes
# n_seq_reverted = loaded_seq_ch.tobytes()
# n_score_reverted = loaded_score_ch.tobytes()
# # decompress
# dctx = zstandard.ZstdDecompressor()
# decompressed_seq = dctx.decompress(n_seq_reverted)
# decompressed_score = dctx.decompress(n_score_reverted)
# # decode
# decoded_seq = dill.loads(decompressed_seq)
# decoded_score = dill.loads(decompressed_score)
# toc = time.perf_counter()
# elapsed_time = toc - tic
# print(len(decoded_seq))
# print(len(decoded_score))
# print(f"elapsed time: {elapsed_time:0.8f} seconds")

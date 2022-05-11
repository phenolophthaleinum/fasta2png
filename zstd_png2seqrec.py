from timeit import default_timer as timer
from Bio import SeqIO
import dill
import bz2
from PIL import Image
import math
import joblib
from io import BytesIO
import zstandard


Image.MAX_IMAGE_PIXELS = None
total_start = timer()
r_img = Image.open("zstd_cmin.png")
dctx = zstandard.ZstdDecompressor()
obj = dill.loads(dctx.decompress(r_img.tobytes()))
total_end = timer()
total_runtime = total_end - total_start
print(f"Total elapsed time (SeqRecord read from png file): {total_runtime:.6f} seconds")
print(len(obj.seq))
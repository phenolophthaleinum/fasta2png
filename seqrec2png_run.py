import time
import functools
import argparse
import dill
import math
import zstandard
import pyppmd
import bz2
import lz4.frame as lz4
from Bio import SeqIO
from PIL import Image


def timeit(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.8f} seconds")
        return value

    return wrapper_timer


def zstandard_compress(data):
    cctx = zstandard.ZstdCompressor(level=11, threads=-1)
    return cctx.compress(data)


def ppm_compress(data):
    return pyppmd.compress(data)


def lz4_compress(data):
    return lz4.compress(data, compression_level=lz4.COMPRESSIONLEVEL_MINHC)


def bz2_compress(data):
    return bz2.compress(data)


@timeit
def standard_workflow(input, output, comp_func):
    seq_obj, = SeqIO.parse(input, 'fasta')
    # print(len(seq_obj.seq))
    p_seq = dill.dumps(seq_obj)
    # print(len(p_seq))
    if comp_func:
        # print("in")
        p_seq = comp_func(p_seq)
    dim = math.floor(math.sqrt(len(p_seq))) + 1
    target = dim * dim
    diff = target - len(p_seq)
    n_seq = p_seq + bytes(int(diff))
    # print(len(n_seq))
    img = Image.frombytes('P', (int(dim), int(dim)), n_seq)
    img.save(output, bits=8)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fastDNA model creation")
    parser.add_argument("-i", "--input", required=True,
                        help="Input filename")
    parser.add_argument("-o", "--output", required=True,
                        help="Output filename")
    parser.add_argument("-f", "--func", required=False,
                        default='standard',
                        const='standard',
                        nargs='?',
                        choices=["standard", "zstandard", "ppm", "lz4", "bz2"],
                        help="Conversion type")
    args = parser.parse_args()
    funcs = {
        "standard": None,
        "zstandard": zstandard_compress,
        "ppm": ppm_compress,
        "lz4": lz4_compress,
        "bz2": bz2_compress
    }
    standard_workflow(args.input, args.output, funcs[args.func])


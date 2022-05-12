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
        passed_args = kwargs
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        f_name = "standard"
        if passed_args["comp_func"] is not None:
            f_name = passed_args["comp_func"].__name__
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"{f_name} elapsed time: {elapsed_time:0.8f} seconds")
        return value, elapsed_time

    return wrapper_timer


def zstandard_compress(data):
    cctx = zstandard.ZstdCompressor(level=11, threads=-1)
    return cctx.compress(data)


def zstandard_decompress(data):
    dctx = zstandard.ZstdDecompressor()
    return dctx.decompress(data)


def ppm_compress(data):
    return pyppmd.compress(data)


def ppm_decompress(data):
    return pyppmd.decompress(data)


def lz4_compress(data):
    return lz4.compress(data, compression_level=lz4.COMPRESSIONLEVEL_MINHC)


def lz4_decommpress(data):
    return lz4.decompress(data)


def bz2_compress(data):
    return bz2.compress(data)


def bz2_decompress(data):
    return bz2.decompress(data)


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


@timeit
def standard_encode(input, comp_func):
    r_img = Image.open(input)
    if comp_func:
        return dill.loads(comp_func(r_img.tobytes()))
    return dill.loads(r_img.tobytes())

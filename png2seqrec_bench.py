import seqrec2png_lib as s2p
import pandas as pd
import os
import glob

# i = "X:/edwards2016/caenorhabditis_elegans.fna"
# o = "elegans_t.png"
# tmp = s2p.standard_workflow(i, o, s2p.zstandard_compress)
# print(tmp)


# files = [
#     "X:/edwards2016/host/fasta/NC_017186.fna",
#     "X:/edwards2016/caenorhabditis_elegans.fna"
# ]
funcs = {
    "standard": None,
    "ppm": s2p.ppm_decompress,
    "lz4": s2p.lz4_decommpress,
    "bz2": s2p.bz2_decompress,
    "zstd": s2p.zstandard_decompress
}

# print(s2p.standard_encode('bench/NC_017186_zstd.png', s2p.zstandard_decompress))
df = pd.DataFrame(columns=['type', 'file name', 'file size (MB)', 'exec time (s)'])
for file in glob.glob('bench/*.png'):
    file_size = os.stat(file).st_size / (1024 * 1024)
    sh_name = file.split("/")[-1]
    f = sh_name.split(".")[0].split('_')[-1]
    time = s2p.standard_encode(input=file, comp_func=funcs[f])[1]
    data = [f, sh_name, file_size, time]
    df.loc[len(df)] = data
    # df['file name'] = [sh_name]
    # df['original file size (MB)'] = [file_size]
    # for f in funcs:
    #     time = s2p.standard_encode(file, funcs[f])[1]
    #     data = [f, sh_name, file_size, time]
    #     df.loc[len(df)] = data
with open("bench/p2s_results.md", 'w') as fh:
    fh.write(df.to_markdown())


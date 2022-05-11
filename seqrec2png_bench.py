import seqrec2png_lib as s2p
import pandas as pd
import os

# i = "X:/edwards2016/caenorhabditis_elegans.fna"
# o = "elegans_t.png"
# tmp = s2p.standard_workflow(i, o, s2p.zstandard_compress)
# print(tmp)

files = [
    "X:/edwards2016/host/fasta/NC_017186.fna",
    "X:/edwards2016/caenorhabditis_elegans.fna"
]
funcs = {
    "standard": None,
    "ppm": s2p.ppm_compress,
    "lz4": s2p.lz4_compress,
    "bz2": s2p.bz2_compress,
    "zstd": s2p.zstandard_compress
}
df = pd.DataFrame(columns=['type', 'file name', 'original file size (MB)', 'new file size (MB)', 'exec time (s)'])
for file in files:
    file_size = os.stat(file).st_size / (1024 * 1024)
    sh_name = file.split("/")[-1]
    outname = sh_name.split(".")[0]
    # df['file name'] = [sh_name]
    # df['original file size (MB)'] = [file_size]
    for f in funcs:
        time = s2p.standard_workflow(file, f"bench/{outname}_{f}.png", funcs[f])[1]
        # df['type'] = f
        # df['exec time (s)'] = time
        new_size = os.stat(f"bench/{outname}_{f}.png").st_size / (1024 * 1024)
        data = [f, sh_name, file_size, new_size, time]
        df.loc[len(df)] = data
with open("bench/s2p_results.md", 'w') as fh:
    fh.write(df.to_markdown())


import math
import os

import numpy
import time
import pyfastx
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib import cm
import pylab
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from skimage.metrics import structural_similarity as ssim


def count_kmers(seq, k):
    d = defaultdict(int)
    for i in range(len(seq) - (k - 1)):
        key = seq[i:i + k]
        if "N" in key:
            continue
        d[seq[i:i + k]] += 1
    return d


def get_kmer_probs(kmers, k, slen):
    return {key: float(v) / (slen - k + 1) for key, v in kmers.items()}


def make_chaos(probs, k):
    """
    - A: (-1, 1) upper left
    - T: (1, -1) lower right
    - G: (1, 1) upper right
    - C: (-1, -1) lower left
    """
    matrix_size = int(math.sqrt(4**k))
    chaos_matrix = np.zeros((matrix_size, matrix_size))
    kmer_matrix = np.empty((matrix_size, matrix_size), dtype=f"<U{k}")

    maxx = matrix_size
    maxy = matrix_size
    posx = 0
    posy = 0
    for key, value in probs.items():
        for char in key:
            if char == "T":
                posx += maxx // 2
            elif char == "C":
                posy += maxy // 2
            elif char == "G":
                posx += maxx // 2
                posy += maxy // 2
            maxx = maxx // 2
            maxy //= 2
        chaos_matrix[posy][posx] = value
        # print(key)
        kmer_matrix[posy][posx] = key
        # print(kmer_matrix[posy][posx])
        maxx = matrix_size
        maxy = matrix_size
        posx = 0
        posy = 0

    return chaos_matrix, kmer_matrix

# xanthomonadales
#   NC_007705 Xanthomonas oryzae pv. oryzae MAFF 311018
#   NC_010513 Xylella fastidiosa M12
records_host = [r for r in pyfastx.Fasta("X:/edwards2016/host/fasta/NC_007705.fna", build_index=False)]
records_vir = [r for r in pyfastx.Fasta("X:/edwards2016/host/fasta/NC_003902.fna", build_index=False)]
records_vir2 = [r for r in pyfastx.Fasta("X:/edwards2016/host/fasta/NC_010515.fna", build_index=False)]
k_mers = count_kmers(records_host[0][1], 7)
k_mers_v = count_kmers(records_vir[0][1], 7)
k_mers_v2 = count_kmers(records_vir2[0][1], 7)
k_mers_prob = get_kmer_probs(k_mers, 7, len(records_host[0][1]))
k_mers_prob_v = get_kmer_probs(k_mers_v, 7, len(records_vir[0][1]))
k_mers_prob_v2 = get_kmer_probs(k_mers_v2, 7, len(records_vir2[0][1]))
# print(k_mers_prob.items())
chaos, kmer_labels = make_chaos(k_mers_prob, 7)
chaos_v, kmer_labels_v = make_chaos(k_mers_prob_v, 7)
chaos_v2, kmer_labels_v2 = make_chaos(k_mers_prob_v2, 7)
host_v1 = chaos - chaos_v
host_v2 = chaos - chaos_v2

#ssim
ssim_host = ssim(chaos, chaos, data_range=np.max(chaos) - np.min(chaos))
print(f"host-host ssim: {ssim_host}")
ssim_v1 = ssim(chaos, host_v1, data_range=np.max(host_v1) - np.min(host_v1))
print(f"host-v1 ssim: {ssim_v1}")
ssim_v2 = ssim(chaos, host_v2, data_range=np.max(host_v2) - np.min(host_v2))
print(f"host-v2 ssim: {ssim_v2}")

# print(chaos)
# pylab.title(f'host: {records_host[0][0]}')
# pylab.imshow(chaos, interpolation='nearest', cmap=cm.gray_r)
# pylab.title(f'virus: {records_vir[0][0]}')
# pylab.imshow(chaos_v, interpolation='nearest', cmap=cm.gray_r)
# pylab.show()
# fig = px.imshow(chaos)
# fig.show()
# print(kmer_labels)


# fig = make_subplots(rows=3, cols=2)
# fig.add_trace(
#     go.Heatmap(z=chaos, text=kmer_labels, hovertemplate="%{text}"),
#     row=1, col=1
# )
# fig.add_trace(
#     go.Heatmap(z=chaos_v, text=kmer_labels_v, hovertemplate="%{text}"),
#     row=1, col=2
# )
# fig.add_trace(
#     go.Heatmap(z=chaos_v2, text=kmer_labels_v2, hovertemplate="%{text}"),
#     row=2, col=1
# )
# fig.add_trace(
#     go.Heatmap(z=host_v1),
#     row=2, col=2
# )
# fig.add_trace(
#     go.Heatmap(z=host_v2),
#     row=3, col=2
# )
# # fig = go.Figure(data=go.Heatmap(z=chaos,
# #                     text=kmer_labels,
# #                     hovertemplate="%{text}"))
# fig.update_layout(height=1400, width=2500, title_text="host - virus")
# subplot_titles = [f"host: {records_host[0][0]}", f"related virus: {records_vir[0][0]}", f"unrelated virus: {records_vir2[0][0]}"]
# fig.for_each_annotation(lambda a: a.update(text=subplot_titles[0]))
# fig.show()
dirname = f"fcgr_{records_host[0][0]}_{records_vir[0][0]}"
Path(dirname).mkdir(exist_ok=True)
# zeropoint = abs(np.min(host_v1)) / (np.max(host_v1) + abs(np.min(host_v1)))
fig = px.imshow(chaos)
fig.write_image(f"{dirname}/{records_host[0][0]}.webp", width=2000, height=2000)
# fig.show()
fig = px.imshow(chaos_v)
fig.write_image(f"{dirname}/{records_vir[0][0]}.webp", width=2000, height=2000)
# fig.show()
fig = px.imshow(host_v1, color_continuous_scale=px.colors.diverging.BrBG, color_continuous_midpoint=0)
fig.write_image(f"{dirname}/comparison.webp", width=2000, height=2000)
# fig.show()

dirname = f"fcgr_{records_host[0][0]}_{records_vir2[0][0]}"
Path(dirname).mkdir(exist_ok=True)
# zeropoint = abs(np.min(host_v1)) / (np.max(host_v1) + abs(np.min(host_v1)))
# print(zeropoint)
fig = px.imshow(chaos)
fig.write_image(f"{dirname}/{records_host[0][0]}.webp", width=2000, height=2000)
# fig.show()
fig = px.imshow(chaos_v2)
fig.write_image(f"{dirname}/{records_vir2[0][0]}.webp", width=2000, height=2000)
# fig.show()
fig = px.imshow(host_v2, color_continuous_scale=px.colors.diverging.BrBG, color_continuous_midpoint=0)
fig.write_image(f"{dirname}/comparison.webp", width=2000, height=2000)
# fig.show()



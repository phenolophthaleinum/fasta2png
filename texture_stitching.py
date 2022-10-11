import stitching
from pathlib import Path
import time
import cv2 as cv


tic = time.perf_counter()
imgs = list(Path("C:/Users/Maciej/samsung-raw/scan_new1_grass3_jpg").rglob("grass3_scan*"))
imgs = [str(x) for x in imgs]
stitcher = stitching.Stitcher(blend_strength=20, try_use_gpu=True, warper_type='plane')
panorama = stitcher.stitch(imgs)
cv.imwrite("scan3_grass3_merged_blend20_nocorrect.png", panorama)
toc = time.perf_counter()
elapsed_time = toc - tic
print(f"elapsed time: {elapsed_time:0.8f} seconds")

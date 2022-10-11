import cv2
import pathlib
import time
import numpy as np


tic = time.perf_counter()
imgs = list(pathlib.Path("slides").rglob("*"))
imgs = [str(x) for x in imgs]
missed_imgs = []
processed_imgs = []
output_dir = "slides_processed"
print(imgs)
print(f"{len(imgs)} images will be processed")

for image in imgs:
    im_name = image.split("\\")[-1]
    im = cv2.imread(image, -1)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thres = cv2.threshold(im_gray, 175, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    opening = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel, iterations=3)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    image_number = 0

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        # cv2.rectangle(im, (x, y), (x + w, y + h), (36, 255, 12), 3)
        ROI = im[y:y + h, x:x + w]
        print(ROI.shape)
        print(f"x: {x}, y: {y}, w: {w}, h: {h}")
        if ROI.shape[0] * ROI.shape[1] >= 1_500_000:
            # input_points = np.float32([[x, y], [x + w, y], [x, y + h], [x + w, y + h]])
            # output_points = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, y - 1]])
            # matrix = cv2.getPerspectiveTransform(input_points, output_points)
            # imgOutput = cv2.warpPerspective(ROI, matrix, (w, h),
            #                                 borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
            # cv2.imwrite(f"{output_dir}/{im_name}_ROI_{image_number}.png", cv2.rotate(imgOutput, cv2.ROTATE_90_CLOCKWISE))
            cv2.imwrite(f"{output_dir}/{im_name}_ROI_{image_number}.png", cv2.rotate(ROI, cv2.ROTATE_90_CLOCKWISE))
            image_number += 1
            processed_imgs.append(im_name)
        else:
            missed_imgs.append(im_name)
            continue

print(f"Missed images: \n{set(missed_imgs) - set(processed_imgs)}")
toc = time.perf_counter()
elapsed_time = toc - tic
print(f"elapsed time: {elapsed_time:0.8f} seconds")

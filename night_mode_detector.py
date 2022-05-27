"""
This file content main NightModeDetector class
if run as main will check a random file form "Images\**\**" and print whether it is a day or nigh image
if --img_path pass with a file img path will check and print whether that is a day or nigh image


"""


from glob import glob
import os
import random
import cv2 as cv
import numpy as np


histSize = 256
histRange = (0, 256)  # the upper boundary is exclusive
accumulate = False

hist_w = 512
hist_h = 400
bin_w = int(round(hist_w / histSize))


class NightModeDetector:
    max_ratio_of_dark_hist_value = 0.6
    ratio_for_dark_hist_range = 0.25
    ShowSrcFlag = False
    ShowHistFlag = False

    def __init__(self, max_ratio_of_dark_hist_value=None, ratio_for_dark_hist_range=None, ShowSrcFlag=False, ShowHistFlag=False) -> None:
        self.ShowSrcFlag = ShowSrcFlag
        self.ShowHistFlag = ShowHistFlag

        if max_ratio_of_dark_hist_value is not None:
            self.max_ratio_of_dark_hist_value = max_ratio_of_dark_hist_value

        if ratio_for_dark_hist_range is not None:
            self.ratio_for_dark_hist_range = ratio_for_dark_hist_range
        pass

    def detect_is_night(self, img: np.ndarray):
        if self.ShowSrcFlag:
            self.show_img(img, "Src Image", False)

        bgr_planes = cv.split(img)

        b_hist = cv.calcHist(bgr_planes, [0], None, [
            histSize], histRange, accumulate=accumulate)
        g_hist = cv.calcHist(bgr_planes, [1], None, [
            histSize], histRange, accumulate=accumulate)
        r_hist = cv.calcHist(bgr_planes, [2], None, [
            histSize], histRange, accumulate=accumulate)

        b_ratio_of_dark_hist_value = self.calculate_ratio_of_dark_hist(b_hist)
        g_ratio_of_dark_hist_value = self.calculate_ratio_of_dark_hist(g_hist)
        r_ratio_of_dark_hist_value = self.calculate_ratio_of_dark_hist(r_hist)

        if self.ShowHistFlag:
            self.show_hist(b_hist, g_hist, r_hist, False)

        if self.ShowSrcFlag or self.ShowHistFlag:
            self.wait_for_key()

        mv = self.max_ratio_of_dark_hist_value

        print(b_ratio_of_dark_hist_value >= mv, g_ratio_of_dark_hist_value >=
              mv, r_ratio_of_dark_hist_value >= mv)
        return b_ratio_of_dark_hist_value >= mv and g_ratio_of_dark_hist_value >= mv and r_ratio_of_dark_hist_value >= mv

    def calculate_ratio_of_dark_hist(self, hist):
        dark_hist = hist[:int(len(hist) * self.ratio_for_dark_hist_range)]

        print(sum(dark_hist), sum(hist), sum(dark_hist) / sum(hist))

        return float(sum(dark_hist)) / sum(hist)

    def wait_for_key(self, wait: int = 0):
        return cv.waitKey(wait)

    def show_img(self, img: np.ndarray, title: str, wait=True):
        cv.imshow(title, img)
        if wait == True:
            self.wait_for_key()

        elif isinstance(wait, int) and wait != False:
            self.wait_for_key(wait=wait)

    def show_hist(self, b_hist: np.ndarray, g_hist: np.ndarray, r_hist: np.ndarray, wait=True):
        cv.normalize(b_hist, b_hist, alpha=0, beta=hist_h,
                     norm_type=cv.NORM_MINMAX)
        cv.normalize(g_hist, g_hist, alpha=0, beta=hist_h,
                     norm_type=cv.NORM_MINMAX)
        cv.normalize(r_hist, r_hist, alpha=0, beta=hist_h,
                     norm_type=cv.NORM_MINMAX)
        histImage = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)
        for i in range(1, histSize):
            cv.line(histImage, (bin_w * (i - 1), hist_h - int(b_hist[i - 1])),
                    (bin_w * (i), hist_h - int(b_hist[i])),
                    (255, 0, 0), thickness=2)
            cv.line(histImage, (bin_w * (i - 1), hist_h - int(g_hist[i - 1])),
                    (bin_w * (i), hist_h - int(g_hist[i])),
                    (0, 255, 0), thickness=2)
            cv.line(histImage, (bin_w * (i - 1), hist_h - int(r_hist[i - 1])),
                    (bin_w * (i), hist_h - int(r_hist[i])),
                    (0, 0, 255), thickness=2)
        self.show_img(histImage, 'Histogram', wait)

    def load_img(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError("Please Provide A Valid Image Path!")

        return cv.imread(path)

    def detect_is_night_from_path(self, path: str):
        return self.detect_is_night(self.load_img(path))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Code For Night Mode Detection')
    parser.add_argument(
        '--img_path', help='Path to input image.', default=None)
    args = parser.parse_args()

    path = args.img_path

    if not path:
        path = random.choice(glob(r"Images\**\**"))

    print("img path -> ", path)

    is_night = NightModeDetector(
        ShowSrcFlag=True, ShowHistFlag=True).detect_is_night_from_path(path)

    print(f"It Is A -> {'Night' if is_night else 'Day'} Image")

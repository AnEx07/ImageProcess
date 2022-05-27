"""
This Script will loop through all "Images\**\**" files
checks if result is matching with image labels(Day/Night)
calculate success rate

"""


from glob import glob
import os
import random

from night_mode_detector import NightModeDetector


if __name__ == "__main__":
    path = random.choice(glob(r"Images\**\**"))

    print("img path -> ", path)

    is_night = NightModeDetector().detect_is_night_from_path(path)

    print("Night" if is_night else "Day")

    image_paths = glob(r"Images\**\**")
    failed_paths = []

    for path in image_paths:
        print("img path -> ", path)

        is_night = NightModeDetector().detect_is_night_from_path(path)

        if path.startswith(os.path.join("Images", "Night" if is_night else "Day")):
            pass

        else:
            print("Test Fail For Img -> ", path)
            failed_paths.append(path)

        print("------------------------------------\n")

    print("Success Ratio -> ", 1 - (len(failed_paths) / len(image_paths)))

    if failed_paths:
        print("Failed Paths -> ", failed_paths)

    else:
        print("No Failed Paths")

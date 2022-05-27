# ImageProcess
the night_mode_detector.py content main NightModeDetector class.<br />
if run as main will check a random file form "Images" Folder and print whether it is a day or nigh image.<br />
if --img_path pass with a file img path will check and print whether that is a day or nigh image.<br />
```
python night_mode_detector.py
or
python night_mode_detector.py --img_path Images\Night\15.jpg
```
the run_test.py will loop through all files of sub directoris of "Images" Folder,<br />
checks if result is matching with image labels(Day/Night) and calculate success rate<br />
```
python run_test.py
```

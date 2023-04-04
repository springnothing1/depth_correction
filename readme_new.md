# Fix Fake Depth Map With SuperPoint

## Dependencies
* [OpenCV](https://opencv.org/) python >= 3.4
* [PyTorch](https://pytorch.org/) >= 0.4

This repo depends on a few standard pythonic modules, plus OpenCV and PyTorch. These commands usually work (tested on Mac and Ubuntu) for installing the two libraries:

```sh
pip install opencv-python
pip install torch
```



## How to fix fake depth map with it

### Obtain the depth.txt 
You should obtain the file containing the path of all the fake depth maps,and put it in the root directory of this project,naming depth.txt 

Under the depth map general directory，for example:
```
/home/spring/mnt/sda3/database/20230329/i18R/DEPTH/AdelaiDepth/TRAIN/EVT
```
Enter the command in the terminal：
```angular2html
find ./ -type f > depth.txt
```

Or maybe just:
```angular2html
find /home/spring/mnt/sda3/database/20230329/i18R/DEPTH/AdelaiDepth/TRAIN/EVT -type f > depth.txt
```

### Obtaining the remapl.txt
You should obtain the file containing the path of all the map of left camera.
you can replace the path in depth.txt with remap 

Enter the command in the terminal：
```angular2html
sed "s|DEPTH/AdelaiDepth|REMAP|g" depth.txt > remapl.txt
```

### Obtaining the remapr.txt
You should obtain the file containing the path of all the map of left camera.
you can replace the path in remapl.txt with remap from right camera.

Enter the command in the terminal：
```angular2html
sed "s|left|right|g" ramapl.txt > remapr.txt
```

### Put all the file.txt in the root directory of this project

### End
In the end, you can input:
```
python3 demo_superpoint_orb.py --input1="/media/zhangs/T7/parker/shujuji0310/小广场/高光/recordgcgaoguang500/imsee_data.bag.imgs.L/" --input2="/media/zhangs/T7/parker/shujuji0310/小广场/高光/recordgcgaoguang500/imsee_data.bag.imgs.R/" --W=640 --H=400 --cuda --display_scale=1
```

- 参数说明
  - `-input1`left-camera record的路径，保证文件夹下非空即可，没有使用
  - `-input2`right-camera record的路径，保证文件夹下非空即可，没有使用
  - `--W`图像的with
  - `--H`图像的height
  - `--cuda` lag to enable the GPU
  - `--display_scale` 尺度化显示的图像大小，实际提取点还是在原图上进行 
  - `Esc`　键盘退出程序
  - 键盘空格键表示暂停，再次点击空格键盘开始

### Output
In the terminal, you'll see this for every thousand images processed
```angular2html
**images are done!!!
```
and you'll obtain the result in the directory(you can change in the module---computation)
```angular2html
/home/spring/mnt/sda3/database/20230329/i18R/new_DEPTH/AdelaiDepth/TRAIN/EVT
```

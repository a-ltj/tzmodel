#import crnninterface
import os
import cv2
import time
import math
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont
from eastdemo import east_detect
from test_shadownet import recognize
from models.Target import Target


def get_images(test_data_dir):
    files = []
    exts = ['jpg', 'png', 'jpeg', 'JPG']
    for parent, dirnames, filenames in os.walk(test_data_dir):
        for filename in filenames:
            for ext in exts:
                if filename.endswith(ext):
                    files.append(os.path.join(parent, filename))
                    break
    print('Find {} images'.format(len(files)))
    return files

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    
def sort_poly(p):
    min_axis = np.argmin(np.sum(p, axis=1))
    p = p[[min_axis, (min_axis+1)%4, (min_axis+2)%4, (min_axis+3)%4]]
    if abs(p[0, 0] - p[1, 0]) > abs(p[0, 1] - p[1, 1]):
        return p
    else:
        return p[[0, 3, 2, 1]]
        
def cut_roi(image, boxes):
    img_crop = []
    for i, box in enumerate(boxes):
        box = sort_poly(box.astype(np.int32))
        im_cut = image[box[0, 1]:box[3, 1], box[0, 0]:box[1, 0], ::-1]
        img_crop.append(im_cut)

    return img_crop

def main(im_fn):
    #east args
    checkpoint_dir = 'model/checkpoint/east/'

    # #crnn args
    weights_path = 'model/checkpoint/crnnsyn/'
    char_dict_path = 'crnn/data/char_dict/char_dict.json'
    ord_map_dict_path = 'crnn/data/char_dict/ord_map.json'

    targets = []
    im = cv2.imread(im_fn)[:, :, ::-1]
    boxes = east_detect(checkpoint_dir,im_fn)
    if boxes is not None:
        img_crop = cut_roi(im[:, :, ::-1], boxes)
        for i, box in enumerate(boxes):
            box = sort_poly(box.astype(np.int32))
            if np.linalg.norm(box[0] - box[1]) < 5 or np.linalg.norm(box[3] - box[0]) < 5:
                continue
            target = Target('label', int(box[0,0]), int(box[0,1]), int(box[2,0] - box[0,0]), int(box[2,1] - box[0,1]))
            targets.append(target)

    textresults = recognize(img_crop,weights_path,char_dict_path,ord_map_dict_path)

    return targets,textresults

if __name__ == '__main__':
    main()
import json
import glob
import cv2
import os
import random
from pathlib import Path

data_path = '/home/etriobj/jupyter/etri/data'
work_path = '/home/etriobj/mgyukim/workspaces/challenge_dataset'
save_path = str(Path.home()) + os.sep + work_path 

def getResolution(vid):
    vidcap = cv2.VideoCapture(vid)
    width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vidcap.release()

    return width, height

def pos2yololabel(position, img_width, img_height):
    print(position, img_width, img_height)
    x_min, y_min, x_max, y_max = position
    x_center = ((x_max + x_min) / 2) / img_width
    y_center = ((y_max + y_min) / 2) / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height

    return x_center, y_center, width, height

def renameDir(img_change=True, label_change=True):
    vid_list = glob.glob(data_path + '/*')
    for v in vid_list:
        if not os.path.isdir(v):
            vid_list.remove(v)
    
    for v in vid_list:
        if img_change and os.path.exists(v+'/image'):
            os.rename(v+'/image', v+'/images')
        if label_change and os.path.exists(v+'/label'):
            os.rename(v+'/label', v+'/labels')

def parser():
    vid_list = glob.glob(data_path + '/*')
    for v in vid_list:
        if not os.path.isdir(v):
            vid_list.remove(v)
    
    for v in vid_list:
        label_path = os.path.join(v, 'label')
        if not os.path.exists(label_path):
            os.makedirs(label_path)

        dir_name = v.split('/')[-1]
        # vid_path = v + '/' + dir_name + '.mp4'
        # width, height = getResolution(vid_path) # get frame width and height for normalize

        json_name = os.path.join(v, dir_name + '.json')
        #json_name = v + '/' + dir_name + '.json'
        with open(json_name, 'r') as jf:
            config = json.load(jf)

        imgs = config[dir_name]['videos']['images']

        for img in imgs:
            label_file = label_path + '/' + dir_name + '_' + img['id'][2:] + '.txt'
            objects = img['objects']

            if objects is None:
                pass
            
            labels = []
            for obj in objects:
                pos = obj['position']
                x_center, y_center, width, height = pos2yololabel(pos, 1920, 1080)

                if obj['class_ID'] == 'c_1':
                    labels.append([0, x_center, y_center, width, height])
                else:
                    labels.append([1, x_center, y_center, width, height])
            
            with open(label_file, 'w') as file:
                for l in labels:
                    class_id, x_center, y_center, width, height = l
                    file.write('{} {} {} {} {}\n'.format(class_id, x_center, y_center, width, height))

def gentext(shuffle=True, p=0.8):
    vid_list = glob.glob(data_path + '/*')
    for v in vid_list:
        if not os.path.isdir(v):
            vid_list.remove(v)
    
    img_path = []
    for v in vid_list:
        img_names = v + '/images/*.jpg'
        img_path += glob.glob(img_names)

    if shuffle:
        random.shuffle(img_path)

    split = int(len(img_path) * p)

    with open(save_path + os.sep + 'train.txt', 'w') as train_file:
        for i in range(split):
            train_file.write('{}\n'.format(img_path[i]))

    with open(save_path + os.sep + 'val.txt', 'w') as val_file:
        for i in range(split, len(img_path)):
            val_file.write('{}\n'.format(img_path[i]))
    

if __name__ == '__main__':
    # renameDir(True, False)
    parser()
    gentext()
import os
import cv2
import json
import glob

import matplotlib.pyplot as plt

def coco_extract_bbox(coco_json_dict, img_file_name):
    # Initialize
    bbox_list = []
    img_idx = None

    # Get json infomation
    imgs_file_info = coco_json_dict['images']
    imgs_label_info = coco_json_dict['annotations']

    # Check existence of files
    for img_info in imgs_file_info:
        if img_file_name == img_info['file_name']:
            img_idx = img_info['id']

    # Get bbox information
    if not img_idx == None:
        for img_anno in imgs_label_info:
            if img_anno['image_id'] == img_idx:
                bbox_info = img_anno['bbox']
                bbox_list.append(bbox_info)
        return bbox_list

    # Exceptional treatement
    else:
        assert NotImplementedError
        return 0

def challenge_extract_bbox(challenge_json_dict, img_file_name):
    # Number
    dir_name = img_file_name.rsplit("_", 1)[0]
    
    # bbox_list
    bbox_list = []
    
    # img_number
    img_number = '00' + str.split(img_file_name, '_')[-1]
    
    # Slicing image info (not video)
    imgs_info = challenge_json_dict[dir_name]['videos']['images']

    # look for img_id
    for img_info in imgs_info:
        if img_info['id'] == img_number:
            objects = img_info['objects'] # list
            for object_info in objects:
                bbox_info = object_info['position'] #bbox_info list
                bbox_list.append(bbox_info)

    return bbox_list

def yolo_extract_bbox(label_file_path, img_width, img_height):
    # Initialize bbox_list
    bbox_list = []

    # Get files
    f = open(label_file_path)

    while True:
            line = f.readline()
            if not line:
                break

            class_number, center_x,center_y,box_width,box_height = line.split()
            
            # should put bbox x,y,width,height
            # bbox x,y is top left
            
            center_x =  int(float(center_x) * int(img.shape[1]))
            center_y = int(float(center_y) * int(img.shape[0]))
            box_width = int(float(box_width) * int(img.shape[1]))
            box_height = int(float(box_height) * int(img.shape[0]))
            top_left_x = center_x - int(box_width/2)
            top_left_y = center_y - int(box_height/2)

            bbox = [top_left_x, top_left_y, box_width, box_height]
            bbox_list.append(bbox)

    return bbox_list

def get_label_name_and_path(img_path):
    img_dir_path = os.path.split(img_path)[:-1]
    label_dir_path = os.path.split(os.path.split(img_path)[0])[0]

    img_file_path = os.path.split(img_path)[-1]
    img_file_name = os.path.splitext(img_file_path)[0]

    label_dir_path = os.path.join(label_dir_path, 'label')
    label_file_path = os.path.join(label_dir_path, img_file_name + '.txt')

    return img_file_name, img_file_path, label_dir_path, label_file_path

def visualize(img_path, bbox_list, datatype="coco"):
    # File name
    img_file_name, _, _, _ = \
            get_label_name_and_path(img_path)
    
    # Import an image
    img = cv2.imread(img_path)

    # Draw bounding boxes
    for bbox in bbox_list:
        if datatype=="coco":
            upper_left_pos = (bbox[0], bbox[1])
            lower_right_pos = (bbox[0]+bbox[2], bbox[1]+bbox[3])
            img = cv2.rectangle(img, upper_left_pos, lower_right_pos, (0, 255, 0), 2)

        if datatype=="challenge":
            upper_left_pos = (bbox[0], bbox[1])
            lower_right_pos = (bbox[2], bbox[3])
            img = cv2.rectangle(img, upper_left_pos, lower_right_pos, (0, 255, 0), 2)

    # Save images
    cv2.imwrite("bounding_box"+img_file_name+".png", img)

    # Save figure
    #plt.savefig(img, "bounding_box"+img_file_name+".png")

    return 0

def json_load_file(filename):
    with open(filename, 'r') as jf:
            json_dict = json.load(jf)

    return json_dict



if __name__ == "__main__":
    img_width = 1920
    img_height = 1080
    
    img_file_path = '/home/etriobj/jupyter/etri/data/0506_V0001/image/0506_V0001_009.jpg'
    coco_anno_path = '/home/etriobj/jupyter/etri/data/coco_style_anno.json'
    challenge_anno_path = '/home/etriobj/jupyter/etri/data/0506_V0001/0506_V0001.json'

    # Load json
    anno_coco = json_load_file(coco_anno_path)
    anno_challenge = json_load_file(challenge_anno_path)

    # Split filename
    img_file_name, img_file_path_ext, _, _ = \
        get_label_name_and_path(img_file_path)

    bbox_list_coco = coco_extract_bbox(anno_coco, img_file_path_ext)
    bbox_list_challenge = challenge_extract_bbox(anno_challenge, img_file_name)

    #visualize(img_file_path, bbox_list_coco)
    visualize(img_file_path, bbox_list_coco, datatype='coco')
    



    

    

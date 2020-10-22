'''
   Make a json file for "coco annotation"
'''

import json
import os
import cv2
import math
import random
import datetime
from tqdm import tqdm

# coco utils
from utils_coco import *

def get_label_list(coco_path):
    ''' 
        Get all label file paths in coco_path

        Args:
            coco_path : root_path
        Returns:
            label_file_list : [0508_V0001.json, ..., ]
            file_name_list : [0508_V0001, ..., ]
    '''
    # Get label directory
    label_dir_path = os.path.join(coco_path, 'labels')

    # Get file list (.json)
    label_file_list = sorted(os.listdir(label_dir_path))

    # Get file name (.json)
    file_name_list = []
    for file_path in label_file_list:
        file_name = file_path.rsplit(".", 1)[0]
        file_name_list.append(file_name)

    return label_file_list, file_name_list

def get_file_name_dict(coco_path, file_name_list):
    ''' 
        Get a dict of hierachical directory_name and img_files

        Args:
            coco_path : root_path
            file_name_list : e.g) [0508_V0001, ..., ]
        Returns:
            img_file_dict : 
                key : file_name e.g)0508_V001
                value : file_path_list e.g) [0508_V001_001.jpg, ..., ]
    '''
    
    # Set image directory
    img_dir_path = os.path.join(coco_path, 'images')

    # File list
    img_file_list = os.listdir(img_dir_path)

    # Initialize : img_file_list
    img_file_dict = {}

    # Insert img_file_path according to directory name
    for file_name in file_name_list:
        temp = []

        for file_path in img_file_list:
            file_name_by_images = file_path.rsplit("_", 1)[0]

            if file_name == file_name_by_images:
                temp.append(file_path)

        img_file_dict[file_name] = sorted(temp)

    return img_file_dict

def exe_convert_custom_to_coco(is_train=True):
    '''
        Main function for convert

        Args:
            is_train : set train directory or valid directory
    '''
    
    # Set root path
    if is_train:
        coco_path = "/home/etriobj/jupyter/etri/coco/train"
    else:
        coco_path = "/home/etriobj/jupyter/etri/coco/train"
    
    # Annotation file name
    coco_annotation_path = os.path.join(coco_path, "annotations")
    annotation_file_path = os.path.join(coco_annotation_path, "challenge_train"+".json")

    # Get label_file_list, file_name_list
    label_file_list, file_name_list = get_label_list(coco_path)

    # Get dict of directory and file_path
    file_path_dict = get_file_name_dict(coco_path, file_name_list)

    # Initialize
    image_dict_list = []
    annotaion_dict_list = []

    # tqdm for visualization of loop
    pbar = enumerate(file_path_dict.items())
    pbar = tqdm(pbar, total=len(file_path_dict))

    # Loop file path (about 30 min)
    for i, (key, file_path_list) in pbar:
        for image_file_path in file_path_list:
            # Set image and annotation
            annotaion_dict_list = coco_annotation_dict_list(coco_path, \
                annotaion_dict_list, image_dict_list, image_file_path, label_file_list)

    # Make a coco basic
    info_dict = coco_info()
    licenses_list = coco_licenses()
    categories_list = coco_categories()

    # Make a final dictionary right before coco format json
    total = coco_total(info_dict, licenses_list, categories_list,\
        image_dict_list, annotaion_dict_list)

    # Save json file
    with open(annotation_file_path, 'w', encoding='utf-8') as make_file :
        json.dump(total, make_file, ensure_ascii=False, indent='\t')

if __name__ == "__main__":
    exe_convert_custom_to_coco(is_train=True)
    exe_convert_custom_to_coco(is_train=False)

    


            




    

    
    
    
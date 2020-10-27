'''
    Arrange and copy files for matching "coco format"
'''

import json
import os
import cv2
import math
import random
import shutil


def get_directory_name_list(root_path):
    '''
        Get directory name list

        Args
            root_path 

        Returns
            train_name_list : all directory name list e.g)[0506_V0001, ...]
    '''
    
    directory_path_list = []

    dir_name_list = os.listdir(root_path)

    for dir_name in dir_name_list:
        dir_path = os.path.join(root_path, dir_name)
        
        if os.path.isdir(dir_path) and dir_path.rsplit("_", 1)[-1] != "checkpoints":
            directory_path_list.append(dir_path)
            #print(dir_path)

    result = sorted(directory_path_list)
    return result

def split_train_and_val_dir_list(directory_path_list, p=0.7, shuffle=False):
    '''
        Split train and val directory list

        Args
            directory_name_list 

        Returns
            train_directory_name_list :  e.g)[ 0506_V0001, ..., 0608_V001]
            val_directory_name_list : e.g) [ 0609_V001, ..., 0628_V001]
    '''

    total_count = len(directory_path_list)
    threshold_idx = int(round(total_count*p))

    if shuffle:
        random.shuffle(directory_path_list)

    train_name_list = directory_path_list[:threshold_idx]
    val_name_list = directory_path_list[threshold_idx:]

    return train_name_list, val_name_list

def get_label_json_path_list(dir_path_list):
    '''
        Split train and val directory list

        Args
            directory_name_list 

        Returns
            train_directory_name_list :  e.g)[ 0506_V0001, ..., 0608_V001]
            val_directory_name_list : e.g) [ 0609_V001, ..., 0628_V001]
    '''
        
    path_list = []
    
    for dir_path in dir_path_list:
        file_name = os.path.split(dir_path)[-1]
        #img_file_name = os.path.splitext(img_file_path)[0]
        
        label_file_path = os.path.join(dir_path, file_name + ".json")
        if os.path.isfile(label_file_path):
            path_list.append(label_file_path)
    
    return path_list

def get_img_files_path_list(dir_path_list):
    '''
        Get img_file_name_list 

        Args
            dir_path_list : directory_list comes from "split_train_and_val_dir_list" func.

        Return
            file_path_list : e.g [0508_V001_000001.jpg, ...]
    '''
    
    
    path_list = []

    for dir_path in dir_path_list:
        img_dir_path = os.path.join(dir_path, 'image')
        img_file_list = os.listdir(img_dir_path)

        for img_file in img_file_list:
            if os.path.splitext(img_file)[-1] == ".jpg" and \
                os.path.split(img_file)[-1].rsplit('_', 1)[-1] != "checkpoints":
                continue
            else:
                assert NotImplementedError
        img_file_list = sorted(img_file_list)
        path_list.append(img_file_list)

    return path_list

def json_load_file(filename):
    '''
        Convert a json file to python dict instance.
    '''
    
    with open(filename, 'r') as jf:
            json_dict = json.load(jf)

    return json_dict


def mk_dir_coco_root(save_root_path):
    '''
        Just Make a directory coco root directory
            if exists, remove all files in save_root_path

        e.g)
            coco (save_root_path)
                |- train
                    |- images
                    |- lables
                    |- annotations
                |- val
                    |- images
                    |- lables
                    |- annotations
    '''

    def mk_sub_dirs(dir_path):
        os.mkdir(dir_path)
        os.mkdir(os.path.join(dir_path, "images"))
        os.mkdir(os.path.join(dir_path, "annotations"))
        os.mkdir(os.path.join(dir_path, "labels"))
        
    
    if os.path.isdir(save_root_path):
        print("*"*10, "The directory exists and remove all", "*"*10)
        shutil.rmtree(save_root_path)
    
    os.mkdir(save_root_path)
    train_dir_path = os.path.join(save_root_path, "train")
    val_dir_path = os.path.join(save_root_path, "val")

    mk_sub_dirs(train_dir_path)
    mk_sub_dirs(val_dir_path)

    return 0

def cp_all_images_and_labels(arrival_root_path, img_dir_list, label_path_list, is_train=True):
    '''
        copy all files in img_dir_list and label_path_list
        
            coco (arrival_root_path)
                |- train  or val
                    |- images (all images in img_dir_list)
                    |- lables (all labels in label_path_list)
                    |- annotations
                
        Args :
            arrival_root_path : root_path (./coco)
            img_dir_list : img_directory_list ([0501_V0001, 0502_V002, ...]
            label_path_list : img_directory_list ([0501_V0001.json, 0502_V002.json, ...]
            is_train : select train directory
    '''
    
    
    # Set root path
    if is_train:
        arrival_dir_path = os.path.join(arrival_root_path, 'train')
    else:
        arrival_dir_path = os.path.join(arrival_root_path, 'val')

    # Set images, label directory path
    arrival_img_dir = os.path.join(arrival_dir_path, "images")
    arrival_label_dir = os.path.join(arrival_dir_path, "labels")

    for img_dir_path, label_file_path in zip(img_dir_list, label_path_list):
        # Select img folder
        img_dir_path = os.path.join(img_dir_path, 'image')
        
        file_list = os.listdir(img_dir_path)

        # copy images to arrival_path
        for file_name in file_list:
            file_path = os.path.join(img_dir_path, file_name)

            if os.path.isfile(file_path):
                shutil.copy(file_path, arrival_img_dir)

        # copy labels to arrival_path
        shutil.copy(label_file_path, arrival_label_dir)

    return 0

def exe_arrange_files():
    '''
        Main function for arrange fiels

        Args:
            is_train : set train directory or valid directory
    '''
    
    # Set paths
    path = '/home/etriobj/jupyter/etri/data/'
    save_root_path = "/home/etriobj/jupyter/etri/coco"
    
    # Get directory list
    directory_path_list = get_directory_name_list(path)

    train_dir_path_list, val_dir_path_list = \
        split_train_and_val_dir_list(directory_path_list)

    train_label_path_list = \
        get_label_json_path_list(train_dir_path_list)

    val_label_path_list = \
        get_label_json_path_list(val_dir_path_list)

    train_img_file_path = \
        get_img_files_path_list(train_dir_path_list)

    val_img_file_path = \
        get_img_files_path_list(val_dir_path_list)

    # Make a directory
    mk_dir_coco_root(save_root_path)

    # Copy all files to coco format
        # Train set
    cp_all_images_and_labels(save_root_path, train_dir_path_list, train_label_path_list, True)
        # Val set
    cp_all_images_and_labels(save_root_path, val_dir_path_list, val_label_path_list, False)

if __name__ == "__main__":
    exe_arrange_files()

    
        

    


    
    
    
    
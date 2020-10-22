'''
    util functions to make coco type json file
'''

import json
import os
import cv2
import math
import random
import shutil

def json_load_file(filename):
    '''
        Convert a json file to python dict instance.
    '''
    
    with open(filename, 'r') as jf:
            json_dict = json.load(jf)

    return json_dict

def coco_total(info, licenses, categories, images, annotations):
    '''
        Make a coco_total list

        Args:
            info : dict
            licenses : list
            categories : list
            images : list
            annotations : list

        Returns:
            total : dict
    '''
    total = {}

    total['info'] = info
    total['licenses'] = licenses
    total['categories'] = categories
    total['images'] = images
    total['annotations'] = annotations

    return total

def coco_info():
    # make info
    info = {
            'description' : '',
            'url' : '',
            'version' : '',
            'year' : 2020,
            'contributor' : '',
            'data_created' : '2020-04-14 01:45:18.567988'
            }
    
    return info

def coco_licenses():
    # make licenses
    licenses_list = []
    licenses_0= {
            'id' : '1',
            'name' : 'your_name',
            'url' : 'your_name'
            }
    licenses_list.append(licenses_0)

    ''' if you want to add licenses, copy this code
    licenses_1 = {
        'id': '2',
        'name': 'your_name',
        'url': 'your_name'
    }
    licenses_list.append(licenses_1)
    '''

    return licenses_list

def coco_categories():
    # make categories
    category_list = []
    class_0 = {
            'id':  1,
            'name' : 'defect',
            'supercategory' : 'None'
            }
    category_list.append(class_0)

    '''
    # if you want to add class
    class_1 = {
            'id':  2,
            'name' : 'defect',
            'supercategory' : 'None'
            }
    category_list.append(class_1)
    '''
    return category_list

def coco_bbox(challenge_bbox):
    
    upper_left_x = challenge_bbox[0]
    upper_left_y = challenge_bbox[1]
    width = challenge_bbox[2] - challenge_bbox[0]
    height = challenge_bbox[3] - challenge_bbox[1]

    bbox = [upper_left_x, upper_left_y, width, height]

    return bbox

def coco_segmentation(challenge_bbox):
    upper_left_x = challenge_bbox[0]
    upper_left_y = challenge_bbox[1]
    upper_right_x = challenge_bbox[2]
    upper_right_y = challenge_bbox[1]
    lower_left_x = challenge_bbox[0]
    lower_left_y = challenge_bbox[3]
    lower_right_x = challenge_bbox[2]
    lower_right_y = challenge_bbox[3]

    segmentation_list = [upper_left_x, upper_left_y, upper_right_x, upper_right_y, \
        lower_left_x, lower_left_y, lower_right_x, lower_right_y]

    return segmentation_list

def coco_label_dict(label_count, image_count, class_number, bbox_list, segmentation_list):
    label_dict = {
        'id' : label_count,
        'image_id' : image_count,
        'category_id' : class_number,
        'iscrowd' : 0,
        'area' : int(bbox_list[2] * bbox_list[3]),
        'bbox' : bbox_list,
        'segmentation' : segmentation_list
    }

    return label_dict

def coco_images_dict_list(image_dict_list, image_root_path, image_name):
    '''
        Add coco image type dict to image_dict_list 

        Args:
            image_dict_list : final image information to coco style json format
            image_root_path : image directory path 
                e.g) coco_path = "/home/etriobj/jupyter/etri/coco/train/images"
            image_path : image path
    '''
    
    # Length
    count = len(image_dict_list)

    # Load an image
    image_path = os.path.join(image_root_path, image_name)
    img = cv2.imread(image_path)

    # make a dict
    image_dict = {
        'id' : count,
        'file_name' : image_name,
        'width' : img.shape[1],
        'height' : img.shape[0],
        'date_captured' : '2020-04-14 -1:45:18.567975',
        'license' : 1, # put correct license
        'coco_url' : '',
        'flickr_url' : ''
    }

    image_dict_list.append(image_dict)

    return image_dict_list, count

def coco_annotation_dict_list(root_dir, annotaion_dict_list, image_dict_list, \
    image_file_path, label_name_list):
    '''
        Add coco annotation dict to annotation_dict_list

        Args:
            root_dir : root_dir e.g) "/home/etriobj/jupyter/etri/coco/train"
            annotation_dict_list : final annotation information to coco style json format
            imge_dict_list : final image information to coco style json format
            image_file_path : target image name in which we look for bounding boxes. e.g) 0501_V001_001.jpg
            label_name_list : label_name_name_list 

        Return :
            annotaion_dict_list : final annotation information to coco style json format
    '''
    # Set path
    image_root_path = os.path.join(root_dir, "images")
    label_root_path = os.path.join(root_dir, "labels")

    # annotation size 
    count_anno = len(annotaion_dict_list)

    # Add image information 
    image_dict_list, img_count = coco_images_dict_list(image_dict_list, image_root_path, image_file_path)

    # Add annotation information
    image_file_name = image_file_path.rsplit(".", 1)[0]
    label_file_name, file_number = image_file_name.rsplit("_", 1)[0], image_file_name.rsplit("_", 1)[1]

    # Load label.json
    label_file_path = os.path.join(label_root_path, label_file_name+".json")
    label_dict = json_load_file(label_file_path)

    # Slicing label information
    label_list = label_dict[label_file_name]['videos']['images']

    # Search for file_number
    for label_dict in label_list:
        if label_dict['id'] == ("00" + file_number):
            for instance in label_dict['objects']:
                bbox = instance['position']
                coco_bbox_list = coco_bbox(bbox)
                coco_segmentation_list = coco_segmentation(bbox)

                coco_label_dict_element = coco_label_dict(count_anno, img_count, class_number=1, \
                    bbox_list=coco_bbox_list, segmentation_list=coco_segmentation_list)

                annotaion_dict_list.append(coco_label_dict_element)
                count_anno += 1

    return annotaion_dict_list








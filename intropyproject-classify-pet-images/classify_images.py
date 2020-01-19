#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND-revision/intropyproject-classify-pet-images/classify_images.py
#                                                                             
# PROGRAMMER: Fonkam Loic
# DATE CREATED: 03/01/2020
# REVISED DATE: 25/01/2020
# PURPOSE: Create a function classify_images that uses the classifier function
#          to create the classifier labels and then compares the classifier
#          labels to the pet image labels. This function inputs:
#            -The Image Folder as image_dir within classify_images and function
#             and as in_arg.dir for function call within main.
#            -The results dictionary as results_dic within classify_images
#             function and results for the functin call within main.
#            -The CNN model architecture as model wihtin classify_images function
#             and in_arg.arch for the function call within main.
#           This function uses the extend function to add items to the list
#           that's the 'value' of the results dictionary. You will be adding the
#           classifier label as the item at index 1 of the list and the comparison
#           of the pet and classifier labels as the item at index 2 of the list.
#
##
# Imports classifier function for using CNN to classify images
from classifier import classifier
from os import listdir
from os.path import join, isfile
from get_pet_labels import getLabel
import ast


#
def classify_images(images_dir, results_dic, model):


    with open('imagenet1000_clsid_to_human.txt') as imagenet_classes_file:
        imagenet_classes_dict = ast.literal_eval(imagenet_classes_file.read())

        # print(imagenet_classes_dict)
    imagenet_dogs = []
    for i in range(151, 269, 1):
        imagenet_dogs.insert(i - 151, imagenet_classes_dict[i].lower())

    filenames = [f for f in listdir(images_dir) if isfile(images_dir + f)]
    for idx in range(0, len(filenames), 1):
        myLabel = getLabel(filenames[idx])
        classifier_set = classifier(images_dir + filenames[idx], model).lower().strip()
        if results_dic.get(filenames[idx]) is None:
            results_dic[filenames[idx]] = [myLabel, classifier_set]

        if set(imagenet_dogs) & set(results_dic.get(filenames[idx])) == {}:
            results_dic[filenames[idx]].extend(( classifier_set, 0))
        else:
            results_dic[filenames[idx]].extend(( classifier_set, 1))



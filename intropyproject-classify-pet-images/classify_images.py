#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND-revision/intropyproject-classify-pet-images/classify_images.py
#                                                                             
# PROGRAMMER: Fonkam Loic
# DATE CREATED: 03/01/2020
# REVISED DATE: 06/01/2020
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
import ast


#
def classify_images(images_dir, results_dic, model):
    """
    Creates classifier labels with classifier function, compares pet labels to
    the classifier labels, and adds the classifier label and the comparison of
    the labels to the results dictionary using the extend function. Be sure to
    format the classifier labels so that they will match your pet image labels.
    The format will include putting the classifier labels in all lower case
    letters and strip the leading and trailing whitespace characters from them.
    For example, the Classifier function returns = 'Maltese dog, Maltese terrier, Maltese'
    so the classifier label = 'maltese dog, maltese terrier, maltese'.
    Recall that dog names from the classifier function can be a string of dog
    names separated by commas when a particular breed of dog has multiple dog
    names associated with that breed. For example, you will find pet images of
    a 'dalmatian'(pet label) and it will match to the classifier label
    'dalmatian, coach dog, carriage dog' if the classifier function correctly
    classified the pet images of dalmatians.
     PLEASE NOTE: This function uses the classifier() function defined in
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the
     classifier() function to classify images within this function
     Parameters:
      images_dir - The (full) path to the folder of images that are to be
                   classified by the classifier function (string)
      results_dic - Results Dictionary with 'key' as image filename and 'value'
                    as a List. Where the list will contain the following items:
                  index 0 = pet image label (string)
                --- where index 1 & index 2 are added by this function ---
                  NEW - index 1 = classifier label (string)
                  NEW - index 2 = 1/0 (int)  where 1 = match between pet image
                    and classifer labels and 0 = no match between labels
      model - Indicates which CNN model architecture will be used by the
              classifier function to classify the pet images,
              values must be either: resnet alexnet vgg (string)
     Returns:
           None - results_dic is mutable data type so no return needed.
    """

    with open('imagenet1000_clsid_to_human.txt') as imagenet_classes_file:
        imagenet_classes_dict = ast.literal_eval(imagenet_classes_file.read())

        # print(imagenet_classes_dict)
    imagenet_dogs = []
    for i in range(151, 269, 1):
        imagenet_dogs.insert(i - 151, imagenet_classes_dict[i].lower())

    filenames = [f for f in listdir(images_dir) if isfile(join(images_dir, f))]
    for idx in range(0, len(filenames), 1):
        myLabel = getLabel(filenames[idx])
        classifier_set = classifier(join(images_dir, filenames[idx]), model).lower()
        if results_dic.get(filenames[idx]) is None:
            results_dic[filenames[idx]] = [myLabel, classifier_set]

        if set(imagenet_dogs) & set(results_dic.get(filenames[idx])) == {}:
            results_dic[filenames[idx]].extend(( classifier_set, 0))
        else:
            results_dic[filenames[idx]].extend(( classifier_set, 1))


def getLabel(imageName):
    low_pet_name = imageName.lower()
    word_without_ext = low_pet_name.split(".")
    word_pet_name = word_without_ext[0].split("_")
    pet_name = ""

    for word in word_pet_name:
        if word.isalpha():
            pet_name += word + " "

    pet_name = pet_name.strip()

    return pet_name

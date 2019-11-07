import cv2
import glob
import numpy as np
import multiprocessing
import time
from numba import jit
# import matplotlib.pyplot as plt
from tempfile import TemporaryFile
arrV = TemporaryFile()

# Operators
@jit(nopython = True)
def euclidean_distance(arrVector1, arrVector2):
    # Besar dari arrVector1 dan arrVector2 harus sama
    sum = 0
    for i in range(len(arrVector1)):
        sum += (arrVector1[i] - arrVector2[i])**2
    return sum**0.5

@jit(nopython = True)
def cosine_similarity(arrVector1, arrVector2):
    # Besar dari arrVector1 dan arrVector2 harus sama
    v = 0
    w = 0
    vw = 0
    for i in range(len(arrVector1)):
        v += arrVector1[i]**2
        w += arrVector2[i]**2
        vw += arrVector1[i]*arrVector2[i]
    v = v**0.5
    w = w**0.5
    return vw/(v*w)

# Load data agak lama gara-gara itemnya 10770

# cv2.imshow('Pic',img_database[3])
# cv2.waitKey(0)

def extract_features(image, vector_size=32):
    alg = cv2.KAZE_create()
    kps = alg.detect(image)
    kps = sorted(kps, key = lambda x: -x.response)[:vector_size]
    kps, desc = alg.compute(image, kps)
    desc = desc.flatten()
    needed_size = (vector_size * 64)
    if (desc.size < needed_size):
        desc = np.concatenate([desc, np.zeros(needed_size - desc.size)])
    # except cv2.error as e:
    #     print (("Error: "), e)
    #     return None

    return desc

def best10match_cosine(img, arrDescription, arrImg):
    img_f = extract_features(img)
    temp = []
    for i in range(len(arrDescription)):
        temp.append(cosine_similarity(img_f, arrDescription[i]))
    cv2.imshow('AA', img)
    cv2.waitKey(0)
    top_10_idx = np.argsort(temp)[-10:]
    for i in top_10_idx:
        cv2.imshow('Pic', arrImg[i])
        cv2.waitKey(0)
    
    return

def best10match_euclid(img, arrDescription, arrImg):
    img_f = extract_features(img)
    temp = []
    for i in range(len(arrDescription)):
        temp.append(euclidean_distance(img_f, arrDescription[i]))
    cv2.imshow('AA', img)
    cv2.waitKey(0)
    top_10_idx = np.argsort(temp)[-10:]
    for i in top_10_idx:
        cv2.imshow('Pic', arrImg[i])
        cv2.waitKey(0)

    return

## Maafkan, tapi ngeimport si main.py agak problematic
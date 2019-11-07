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

def main():
    img_database = []
    for img in glob.glob("img/*.jpg"):
        img_database.append(cv2.imread(img))
    print("Image loading done")

    img_description = []
    for i in range(100):
        img_description.append(extract_features(img_database[i]))
    
    # for i in range(5):
    #     print(img_description[i])

    # Save file dan load file (ntar cuman load)
    np.save(arrV, img_description)
    _ = arrV.seek(0)
    a = np.load(arrV)

    print(euclidean_distance(img_description[0], img_description[2]))
    print(cosine_similarity(img_description[0], img_description[2]))
    print(len(img_description[0]))

    print(euclidean_distance(a[0], a[2]))
    print(cosine_similarity(a[0], a[2]))
    print(len(a[0]))

    # Testing (contoh)
    img = cv2.imread("img/Test/zendaya14.jpg")
    # best10match_cosine(img,img_description,img_database)
    best10match_euclid(img,img_description,img_database)

starttime = time.time()
main()
print('That took {} seconds'.format(time.time()-starttime))

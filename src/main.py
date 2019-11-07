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
# @jit(nopython = True)
def euclidean_distance(arrVector1, arrVector2):
    # Besar dari arrVector1 dan arrVector2 harus sama
    sum = 0
    for i in range(len(arrVector1)):
        sum += (arrVector1[i] - arrVector2[i])**2
    return sum**0.5

# @jit(nopython = True)
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


# def batch_extractor(images_path, pickled_db_path="features.pck"):
#     files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

#     result = {}
#     for f in files:
#         print ("Extracting features from image" ,f) 
#         name = f.split('/')[-1].lower()
#         result[name] = extract_features(f)
    
#     # saving all our feature vectors in pickled file
#     pickle_out = open("dict.pickle","wb")
#     pickle.dump(result, pickle_out)
#     pickle_out.close()

# def show_img(path):
#     img = cv2.imread(images_path)
#     plt.imshow(img)
#     plt.show()
    
# def run():
#     images_path = ("D:\Coding\images")
#     files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
#     # getting 3 random images 
#     sample = random.sample(files, 3)
    
#     batch_extractor(images_path)

#     ma = Matcher('features.pck')
    
#     for s in sample:
#         print("Query image ==========================================")
#         show_img(s)
#         names, match = ma.match(s, topn=3)
#         print ("Result images ========================================'")
#         for i in range(3):
#             # we got cosine distance, less cosine distance between vectors
#             # more they similar, thus we subtruct it from 1 to get match value
#             print ("Match",(1-match[i]))
#             show_img(os.path.join(images_path, names[i]))




def main():
    img_database = []
    for img in glob.glob("img/*.jpg"):
        img_database.append(cv2.imread(img))
    print("Image loading done")

    img_description = []
    for i in range(5):
        img_description.append(extract_features(img_database[i]))
    
    # for i in range(5):
    #     print(img_description[i])

    with open('listfile.txt', 'w') as filehandle:
        for listitem in img_description:
            filehandle.write('%s\n' % listitem)

    np.save(arrV, img_description)
    _ = arrV.seek(0)
    a = np.load(arrV)

    print(euclidean_distance(img_description[0], img_description[2]))
    print(cosine_similarity(img_description[0], img_description[2]))
    print(len(img_description[0]))

    print(euclidean_distance(a[0], a[2]))
    print(cosine_similarity(a[0], a[2]))
    print(len(a[0]))

starttime = time.time()
main()
print('That took {} seconds'.format(time.time()-starttime))
# Zaidan ngopas doang ini..
# Gw lanjutin habis makan malem
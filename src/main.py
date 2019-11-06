import cv2
import glob
import numpy as np 


img_database = []
for img in glob.glob("img/*.jpg"):
    img_database.append(cv2.imread(img))
# Load data agak lama gara-gara itemnya 10770

cv2.imshow('Pic',img_database[3])
cv2.waitKey(0)


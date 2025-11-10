import os
import cv2

dir = 'orig'
files = list(filter(lambda x: x.endswith('.png'), os.listdir(dir)))

for f in files:
    im = cv2.imread(os.path.join(dir, f))
    im = cv2.resize(im, None, fx=0.75, fy=0.75)
    cv2.imwrite(f, im)
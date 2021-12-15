import argparse
import sys

import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
import tensorflow as tf
import numpy as np
import time


parser = argparse.ArgumentParser(
    description='convert model')

parser.add_argument('--img_path', default='./image', type=str,
                    help='Image path for inference')
args = parser.parse_args()

#os.environ['CUDA_VISIBLE_DEVICES'] = "-1"

def main():
    t0 = time.time()

    model = tf.keras.models.load_model("./Models/RFB.h5",compile=False)
    #model.save("RFB.h5")
    #sys.exit(1)
    print(time.time()-t0)

    print("开始处理图片：")
    listdir = os.listdir(args.img_path)

    img_recs = []
    for path in listdir:
        print(path)
        img = cv2.imread('./image/'+path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, _ = img.shape
        img_resize = cv2.resize(img, (320, 240))
        img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
        img_resize = img_resize - 127.0
        img_resize = img_resize / 128.0
        results = model.predict(np.expand_dims(img_resize, axis=0))  # result=[background,face,x1,y1,x2,y2]

        temp_recs = []
        for result in results:
            #print(result[2],result[3],result[4],result[5])
            #if abs(result[2] - result[4]) <= 10 or abs(result[3] - result[5]) <= 10:
            #    continue
            start_x = int(result[2] * w)
            start_y = int(result[3] * h)
            end_x = int(result[4] * w)
            end_y = int(result[5] * h)
            temp_recs.append((start_x, start_y, end_x, end_y))
            cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        cv2.imwrite(f'test_image/RFB_{path}', img)
        #img_recs.append(temp_recs)

    #for recs in img_recs:
        #print(recs)
    print(time.time()-t0)


if __name__ == '__main__':
    main()

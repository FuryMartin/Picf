import sys
import pickle
import shutil
import argparse
import cv2
import numpy as np
import os
import logging
import time
#------------------------------------------------------------------------------------------------
# 旧检测模型 TEST : 161 images , Time Consume : 95.4s , 2021.11.26 2:05   每秒1.69张
#------------------------------------------------------------------------------------------------
# 新检测模型 TEST : 161 images , Time Consume : 48.9s , 2021.11.26 1:39   每秒3.29张，速度提高94%
#------------------------------------------------------------------------------------------------
# 新检测模型 TEST : 161 images , Time Consume : 48.9s , 2021.11.26 1:39   CPU = 16
# 新检测模型 TEST : 161 images , Time Consume : 48.8s , 2021.11.26 18:33  CPU = 8
#------------------------------------------------------------------------------------------------

# Prevent tensorflow from logging in multiple processes simultaneously
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
import tensorflow as tf
tf.get_logger().setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore")

from multiprocessing import Pool, cpu_count
from math import ceil
from utils.facenet import compute_embedding
from tensorflow.keras.models import load_model
from tqdm import tqdm
from utils.display_by_person import load_json,get_persons,write_json


def differ_paths(paths, root_dir):
    #从paths中剔除已存在于output.json中的图片并返回
    images = load_json("output.json")
    existed_paths = []
    for image in images:
        existed_paths.append(os.path.join(root_dir, image["pic_name"]))
    new_paths = []
    for path in paths:
        if path not in existed_paths:
            new_paths.append(path)
    return new_paths

def get_image_paths(root_dir):
    """Generates a list of paths for the images in a root directory and ignores rest of the files
    Args:
        root_dir : string containing the relative path to root directory
    Returns:
        paths : list containing paths of the images in the directory
    """
    if not os.path.exists(root_dir):
        print("Directory not found, please enter valid directory..")
        sys.exit(1)

    paths = []
    for rootDir, directory, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                paths.append(os.path.join(rootDir, filename))

    return paths

def save_embeddings(process_data):
    """Function used by each processing pool to compute embeddings for part of a dataset.
    The embeddings are saved into a temporary folder

    Args:
        process_data : dictionary consisting of data to be used by the pool 
    """
    # load the model for each process

    
    model = load_model("Models/facenet.h5")
    model_detector = load_model("Models/RFB.h5",compile=False)
    # progress bar to track 
    #bar = tqdm(total=len(process_data['image_paths']),#position=process_data['process_id']) #进度条

    output = []
    for count, path in enumerate(process_data['image_paths']):
        #调用facenet.py中的compute_embedding()方法，返回特征值
        embeddings = compute_embedding(path,model,model_detector) 

        # in case no faces are detected
        if embeddings is None:
            continue
        
        # multiple faces in an image
        if embeddings.shape[0] > 1:#若有多张脸，将每张脸加入output
            for embedding in embeddings:
                output.append({"path": path, "embedding": embedding})
        else:#若只有一张脸，将这张脸加入output
            output.append({"path": path, "embedding": embeddings[0]})

        #bar.update()
    #bar.close()

    #bar.clear()

    # write the embeddings computed by a process into the temporary folder
    with open(process_data['temp_path'], "wb") as f:
        pickle.dump(output, f)
    

def embedder(source):
    #t1 = time.time()
    args = {'source':source,'processes':8}
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-src","--source", required=True, help="Path of the root directory where images are stored")
    
    parser.add_argument(
        "--processes", required=False, type=int, default=cpu_count(),help="Number of cores to be used to compute embeddings"
    )

    args = vars(parser.parse_args())
    '''

    image_paths = get_image_paths(args['source'])
    image_paths = differ_paths(image_paths, args['source'])

    if len(image_paths) == 0:
        print("Found 0 new images.")
        return None

    print("Found {} images..".format(len(image_paths)))

    # Define the number of processes to be used by the pool
    # Each process takes one core in the CPU
    processes = args["processes"]
    if len(image_paths) < processes *10:
        processes = 4


    if processes > cpu_count():
        print("Number of processes greater than system capacity..")
        processes = cpu_count()
        print("Defaulting to {} parallel processes..".format(processes))

    # Split the images into equal sized batches for each process
    # Since we only need the embeddings for all the images the data can be split
    # into equal sized batches and each process can then independently compute the embeddings for the images.
    # The embeddings can then be concatenated after all of them are finished
    
    imgs_per_process = ceil(len(image_paths)/processes)

    split_paths = []
    for i in range(0, len(image_paths), imgs_per_process):
        split_paths.append(image_paths[i:i+imgs_per_process])

    # Each process saves the embeddings computed by it into a pickle file in a temporary folder.
    # The temporary pickle files can then be loaded and we can generate a single pickle file containing all the embeddings for our data
    if not os.path.exists("temp"):
        os.mkdir("temp")

    split_data = []
    for process_id, batch in enumerate(split_paths):
        temp_path = os.path.join("temp", "process_{}.pickle".format(process_id))

        process_data = {
            "process_id": process_id,
            "image_paths": batch,
            "temp_path": temp_path
        }
        split_data.append(process_data)

    #print(time.time()-t1)
    # Create a pool which can execute more than one process paralelly
    pool = Pool(processes=processes)
    # Map the function
    print("Started {} processes..".format(processes))

    pool.map(save_embeddings, split_data)

    # Wait until all parallel processes are done and then execute main script
    pool.close()
    pool.join()
    #print(time.time()-t1)
    # Once all processes are done load the pickle files in the temporary folder 'temp' and save them all in one file.
    # After that the temporary folder is deleted
    concat_embeddings = []

    for filename in os.listdir("temp"):
        data = pickle.load(open(os.path.join("temp", filename), "rb"))

        for dictionary in data:
            # dictionary是提取到人脸的图片
            # 将新增识别到的人脸数据添加到concat_embeddings中
            concat_embeddings.append(dictionary)
            #将提取到人脸的图片从image_paths中剔除，则image_paths中是新添加的、未检测到人脸的图片
            if dictionary['path'] in image_paths:
                image_paths.remove(dictionary['path'])

    # 将新识别到的人脸数据与已存在的人脸数据合并
    try:
        existed_data = pickle.load(open("embeddings.pickle","rb"))
    except FileNotFoundError:
        existed_data = []
    #print(existed_data)
    with open("embeddings.pickle", "wb") as f: 
        pickle.dump(concat_embeddings + existed_data, f)

    # 删除识别过程中的临时文件
    shutil.rmtree("temp") #delete ./temp
    print("Saved embeddings of {} faces to disk..".format(len(concat_embeddings)))
    # By now a single pickle file is created and the temporary files are deleted

    # 将新添加的、未检测到人脸的图片与output.json中的“未命名”分类合并
    persons = get_persons("output.json")
    if "未命名" not in persons:
        persons["未命名"] = []
    persons["未命名"].extend(image_paths)
    
    write_json(persons)

    return True

    """
    """
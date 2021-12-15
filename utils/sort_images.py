import pickle
import numpy as np
import networkx as nx
import os
import shutil
import argparse
import sys
import json

from utils.CW import draw_graph,chinese_whispers
from utils.display_by_person import print_by_person,get_persons
from utils.display_by_person import get_persons, sort_by_person, load_json, get_persons_more

def image_sorter(G):
    """Copies images from the source and pastes them to a directory.
    Each sub directory represents a cluster which contains images of the cluster assigned by
    the clustering algorithm

    Args:
        graph : networkx graph on which the clustering algorithm has been done on
    """
    #读取output.json中的分类信息，以[{"name":name, "pic_name":path}]的形式保存到existed_images中
    existed_images = load_json("output.json")
    #将分类信息格式化，方便检测是否已有分类信息，以{path:name}的形式保存到existed_images_dic中
    existed_images_dic = {}
    for existed_image in existed_images:
        name = existed_image["person"]
        path = existed_image["pic_name"]
        existed_images_dic[path] = name

    #将图聚类结果格式化，以{name:[paths]}的形式保存到image_dic中
    image_dic = {}
    for node,attribute in G.nodes.items():
        # Get the image path from the node of the graph and copy it to a subdirectory with the name of the cluster
        path = os.path.basename(attribute["source"])
        name = attribute["cluster"]
        if name not in image_dic:
            image_dic[name] = []
        image_dic[name].append(path)

    for name, paths in image_dic.items():

        # 对于image_dic中的每一项name, [paths]
        # 检测[paths]的每一项path是否已经有分类信息(是否存在于existed_images_dic)
        # 如果已有分类信息，则将path已经存在的分类标签加入tag_counter中。
        # 如果没有分类信息，将path添加到image_to_edit中等待进一步打标签
        image_to_edit = []
        tag_counter = []
        for path in set(paths):
            if path in existed_images_dic:
                tag_counter.append(existed_images_dic[path])
            else:
                image_to_edit.append(path)

        # paths遍历完成后，得到tag_counter和image_to_edit两个列表。
        # image_to_edit存储待打标签的图片，tag_counter存储待打标签图片的同类节点的分类信息
        # 对tag_counter中的标签进行统计，将出现次数最多的标签保存在max_tag中，记max_tag为这一类节点的标签
        max_times = 0
        if len(tag_counter) != 0:
            max_tag = ''
            #print(tag_counter)
            for tag in set(tag_counter):
                temp_times = tag_counter.count(tag)
                if temp_times > max_times:
                    max_tag = tag
                    max_times = temp_times
        else:
            max_tag = name
        
        # 将image_to_edit中的每一张图片打上max_tag的标签，以{"name":max_tag,"pic_name":path}的形式合并到existed_images中
        for path in image_to_edit:
            temp_dic = {}
            temp_dic["person"] = max_tag
            temp_dic["pic_name"] = path
            existed_images.append(temp_dic)

    return existed_images


    #将existed_images写入output.json

        

def sort_images():

    #args = {'threshold': 0.60, 'iterations': 40}
    args = {'threshold': 0.67, 'iterations': 30}
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--threshold", type=float, required=False, default=0.67, help="minimum  distance required between face embeddings to form a edge")
    
    parser.add_argument(
        "-itr", "--iterations", type=int, required=False, default=30, help="number of iterations for the Chinese Whispers algorithm")

    args = vars(parser.parse_args())
    '''
    
    #Load the embeddings
    try:
        data = pickle.load(open("embeddings.pickle","rb"))
        
    except FileNotFoundError:
        print("No saved embeddings found. Please run the script embedder.py")
        sys.exit(1)
    
    # Draw the initial graph. Using CW.py:draw_graph()
    graph = draw_graph(data,args["threshold"])

    # Run the clustering algorithm on the graph. Using CW.py:chinese_whispers()
    graph = chinese_whispers(graph,args["iterations"])

    # Sort the images using the clusters
    images = image_sorter(graph)
    images = sorted(images, key=lambda x: x["pic_name"])
    with open('output.json','w',encoding='utf-8') as f:
        f.write(json.dumps(images,indent=4,ensure_ascii=False, sort_keys=True))


import json
import pickle
import os

def load_json(jsonfile):
    #输入json文件名，返回[{"person":name,"pic_name":path}]形式的列表
    with open(jsonfile, 'r',encoding='utf-8') as f:
        images = json.load(f)
    return images

def sort_by_person(images):
    #输入[{"person":name,"pic_name":path}]形式的列表，返回{name:[paths]}形式的字典
    persons = {}
    for image in images:
        path = image['pic_name']
        name = image['person']
        if name not in persons:
            persons[name] = []
        persons[name].append(path)
    return persons

def get_persons(jsonfile):
    #输入json文件名，返回{name:[paths]}形式的字典
    images = load_json(jsonfile)
    persons = sort_by_person(images)
    return persons

def get_persons_more(persons):
    #输入{name:[paths]}形式的字典，去除paths个数小于等于3的节点，返回{name:[paths]}形式的字典
    person_to_delete = []
    for name, paths in list(persons.items()):
        if name == "未命名":
            continue
        if len(paths) <= 3 or name == "错误分类":
            person_to_delete.append(name)
    for person in person_to_delete:
        persons.pop(person)
    return persons

def write_json(persons):
    #输入{name:[paths]}形式的字典，以[{"person":name,"pic_name":path}]的形式写入output.json中
    images = []
    for name, paths in persons.items():
        for path in paths:
            image_dic = {}
            image_dic['pic_name'] = os.path.basename(path)
            #print(image_dic['pic_name'])
            image_dic['person'] = name
            images.append(image_dic)
    images = sorted(images, key=lambda x: x["person"])
    with open('output.json','w',encoding='utf-8') as f:
        f.write(json.dumps(images,indent=4,ensure_ascii=False,sort_keys=True))

def print_by_person(persons):
    #将{name:[paths]}形式的字典按"人名:图片组"的形式格式化输出
    for name, paths in persons.items():
        print("------------------------------")
        print()
        print("Name:{}".format(name))
        for count,path in enumerate(paths):
            index = path.rfind('\\',0,len(path))
            print("{}:{}".format(count,path[index+1:]))
        print()
    print("------------------------------")

def edit_group_name(new_group_name,old_group_name, persons):
    #输入新名称、旧名称、{name:[paths]}形式的字典，返回更名后的{name:[paths]}形式的字典
    if new_group_name not in persons:
        persons[new_group_name] = persons.pop(old_group_name)
    else:
        persons[new_group_name].extend(persons.pop(old_group_name))
    return persons

def edit_single_group_name(new_group_name, path, persons):
    #输入新名称、图片路径、{name:[paths]}形式的字典，返回更名后的{name:[paths]}形式的字典
    name_to_delete = -1
    for name, paths in persons.items():
        if path in paths:
            paths.remove(path)
        if len(paths)==0:
            name_to_delete = name
    if name_to_delete != -1:
        persons.pop(name_to_delete)
    if new_group_name in persons:
        persons[new_group_name].append(path)
    else:
        persons[new_group_name] = [path]
    return persons

def load_pickle(picklefile):
    #输入embeddings.pickle的路径，返回[{"path":path,"embedding":np_array}]类型的列表
    datas = pickle.load(open(picklefile,"rb"))
    return datas

def write_pickle(datas):
    #输入[{"path":path,"embedding":np_array}]类型的列表，写入embeddings.pickle
    with open("embeddings.pickle", "wb") as f: 
        pickle.dump(datas, f)

def delete_single_pic(target_path, persons):
    # 输入图片路径target_path和{name:[paths]}形式的字典
    # 将target_path对应的图片从embeddings.pickle中删除，
    # 将target_path对应的图片从{name:[paths]}形式的字典中删除，返回修改过的{name:[paths]}形式的字典

    #从persons里删除单张照片
    empty_names =[]
    for name, paths in persons.items():
        if target_path in paths:
            paths.remove(target_path)
            persons[name] = paths
            try:
                os.remove(target_path)
            except FileNotFoundError:
                pass
        if len(paths) == 0:
            empty_names.append(name)
    for name in empty_names:
        persons.pop(name)

    #从embeddings.pickle里删除单张照片
    pickle_datas = load_pickle("embeddings.pickle")
    pickle_to_delete = []
    for index, pickle_data in enumerate(pickle_datas):
        if target_path == pickle_data["path"]:
            pickle_to_delete.append(index)
    for index in pickle_to_delete:
        pickle_datas.pop(index)
    write_pickle(pickle_datas)

    return persons

def delete_multi_pic(rootdir, target_paths, persons):
    pickle_datas = load_pickle("embeddings.pickle")

    for target_path in target_paths:
        target_path = target_path
        empty_names =[]
        for name, paths in persons.items():
            if target_path in paths:
                paths.remove(target_path)
                persons[name] = paths
                try:
                    os.remove(os.path.join(rootdir, target_path))
                except FileNotFoundError:
                    print("Not Found: {}".format(target_path))
                    pass
                #print(persons[name])
            if len(paths) == 0:
                empty_names.append(name)
        for name in empty_names:
            persons.pop(name)

        pickle_to_delete = []
        for index, pickle_data in enumerate(pickle_datas):
            if target_path == os.path.basename(pickle_data["path"]):
                pickle_to_delete.append(index)
        for index in pickle_to_delete:
            pickle_datas.pop(index)
        
    write_pickle(pickle_datas)
    return persons

if __name__ == "__main__":
    jsonfile = 'output.json'
    images = load_json(jsonfile)
    persons = sort_by_person(images)
    #print(persons)
    #print_by_person(persons)
    '''
    更改人脸名测试
    persons = edit_group_name("TEST_2","Person 8",persons)
    write_json(persons)
    '''
    #删除人脸测试
    #persons = delete_pic("./image\\08.jpg",persons)
    #print_by_person(persons)
    persons = edit_single_group_name("Person 46","./image\\08.jpg",persons)
    print_by_person(persons)
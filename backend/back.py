import json
import albumentations
import cv2
import imageio
import numpy as np
import tensorflow.compat.v1 as tf
import torch
import torchvision as tv
from flask import session
from backend.labels import *

imsave = imageio.imsave
imread = imageio.imread
from scipy.spatial.distance import cosine
import pickle
import os
from tensorflow.python.platform import gfile

BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
BOTTLENECK_TENSOR_SIZE = 2048
MODEL_INPUT_WIDTH = 299
MODEL_INPUT_HEIGHT = 299
MODEL_INPUT_DEPTH = 3
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'
RESIZED_INPUT_TENSOR_NAME = 'ResizeBilinear:0'
MAX_NUM_IMAGES_PER_CLASS = 2 ** 27 - 1  # ~134M


class HCILab2Model(torch.nn.Module):
    def __init__(self):
        super(HCILab2Model, self).__init__()
        self.feature_resnet = tv.models.resnet34(pretrained=True, progress=True)
        self.feature_resnet.layer4.register_forward_hook(self.resnet_hook)
        self.feature_output = None
        self.flatten = torch.nn.Flatten()

    def resnet_hook(self, module, input_, output):
        self.feature_output = output

    def forward(self, x):
        y = self.feature_resnet(x)
        x = self.flatten(self.feature_output)
        return x, y


def get_result(**kwargs):
    return {
        'image': r'',
        'labels': 'Animal',
        'title': 'Giant Panda',
        'description': '',
    }


model = HCILab2Model()
indexes = {}
indexed_label = {}
use_tensorflow = False
im_src = "http://localhost:5000/image/"


def set_tf():
    global use_tensorflow
    use_tensorflow = True


def index_for_tensorflow(base_path, extracted_feats):
    # index labels
    print("Index Labels")
    ds = {}
    ls = os.listdir(base_path + "/database/tags_rn/")
    for i in range(len(ls)):
        data = ""
        data_s = []
        with open(base_path + "/database/tags_rn/" + ls[i]) as f:
            data = f.read()
            data_s = data.split('\n')
        data_g = []
        for k in data_s:
            if k.isnumeric():
                data_g.append(int(k))
                ds[int(k)] = ls[i].split(".")[0]
    print("Index Features")

    for i in range(extracted_feats.shape[0]):
        if i % 10 == 0:
            print(i, " of ", (extracted_feats.shape[1]))
        if (i + 1) in ds:
            path = "/im" + str(i) + ".jpg"
            indexes[path] = extracted_feats[i,:]
            indexed_label[path] = ds[i + 1]
        else:
            print("Drop", i + 1)


def index_image(base_path, path, test=False):
    if use_tensorflow:
        if base_path is None:
            feat = recommend(path)
        else:
            feat = recommend(base_path + "/" + path)
        logit = []
    else:
        if base_path is None:
            image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        else:
            image = cv2.imdecode(np.fromfile(base_path + "/" + path, dtype=np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        sample = albumentations.Compose([
            albumentations.Resize(512, 512),
            albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
        ])(image=image)
        image = sample['image']
        image = np.transpose(image, (2, 0, 1))
        mmax = np.max(image)
        mmin = np.min(image)
        image = (image - mmin) / (mmax - mmin)
        image = np.expand_dims(image, axis=0)
        image = torch.tensor(image).to(torch.float32)
        feat, logit = model(image)
        logit = np.squeeze(logit.detach().numpy())
        feat = np.squeeze(feat.detach().numpy())
        logit = np.argmax(logit)
        if not test:
            indexes[path] = feat
            indexed_label[path] = logit
    return feat, logit


def similarity(feat_vector, logit, add_label: str = None):
    sorted_result = []
    fav_list = temporary_bookmark_get()
    if add_label is not None:
        label_list = add_label.split(" ")
    else:
        label_list = None
    for key in indexes.keys():
        d1 = np.sqrt(np.sum(np.square(feat_vector)))
        d2 = np.sqrt(np.sum(np.square(indexes[key])))
        if d2 < 1e-5:
            continue
        dist = np.dot(feat_vector, indexes[key]) / d1 / d2
        if dist < 0.4:
            continue
        if add_label is not None:
            ins = False
            for i in label_list:
                if key.find(i) != -1:
                    ins = True
                if use_tensorflow:
                    if indexed_label[key].find(i) != -1:
                        ins = True
                else:
                    if image_label()[indexed_label[key]].find(i) != -1:
                        ins = True
            if ins:
                if use_tensorflow:
                    cate_f = key.split("-")[0]
                    sorted_result.append({
                        "image": "http://localhost:5000/image/" + key,
                        "coef": int(dist * 10000),
                        "labels": cate_f + ", " + indexed_label[key],
                        "title": key,
                        "fav": int(key in fav_list),
                        "description": "No additional descriptions.",

                    })
                else:
                    cate_f = key.split("-")[0]
                    sorted_result.append({
                        "image": "http://localhost:5000/image/" + key,
                        "coef": int(dist * 10000),
                        "labels": cate_f + ", " + image_label()[indexed_label[key]],
                        "title": key,
                        "fav": int(key in fav_list),
                        "description": "No additional descriptions.",

                    })
        else:
            if use_tensorflow:
                cate_f = key.split("-")[0]
                sorted_result.append({
                    "image": "http://localhost:5000/image/" + key,
                    "coef": int(dist * 10000),
                    "labels": cate_f + ", " + indexed_label[key],
                    "title": key,
                    "fav": int(key in fav_list),
                    "description": "No additional descriptions.",

                })
            else:
                cate_f = key.split("-")[0]
                sorted_result.append({
                    "image": "http://localhost:5000/image/" + key,
                    "coef": int(dist * 10000),
                    "labels": cate_f + ", " + image_label()[indexed_label[key]],
                    "title": key,
                    "fav": int(key in fav_list),
                    "description": "No additional descriptions.",

                })

    sorted_result.sort(key=lambda x: -x["coef"])
    if len(sorted_result)>100:
        sorted_result = sorted_result[:100]
    return sorted_result


def get_fav_list(add_label: str = None):
    sorted_result = []
    fav_list = temporary_bookmark_get()
    if add_label is not None:
        label_list = add_label.split(" ")
    else:
        label_list = None
    for key in indexes.keys():
        if add_label is not None:
            ins = False
            for i in label_list:
                if key.find(i) != -1:
                    ins = True
                if use_tensorflow:
                    if indexed_label[key].find(i) != -1:
                        ins = True
                else:
                    if image_label()[indexed_label[key]].find(i) != -1:
                        ins = True
            if ins and key in fav_list:
                cate_f = key.split("-")[0]
                if use_tensorflow:
                    sorted_result.append({
                        "image": "http://localhost:5000/image/" + key,
                        "coef": 1,
                        "labels": cate_f + ", " + indexed_label[key],
                        "title": key,
                        "fav": 1,
                        "description": "No additional descriptions.",

                    })
                else:
                    sorted_result.append({
                        "image": "http://localhost:5000/image/" + key,
                        "coef": 1,
                        "labels": cate_f + ", " + image_label()[indexed_label[key]],
                        "title": key,
                        "fav": 1,
                        "description": "No additional descriptions.",

                    })
        else:
            if key in fav_list:
                cate_f = key.split("-")[0]
                if use_tensorflow:
                    sorted_result.append({
                        "image": "http://localhost:5000/image/" + key,
                        "coef": 1,
                        "labels": cate_f + ", " + indexed_label[key],
                        "title": key,
                        "fav": 1,
                        "description": "No additional descriptions.",

                    })
                else:
                    sorted_result.append({
                        "image": "http://localhost:5000/image/" + key,
                        "coef": 1,
                        "labels": cate_f + ", " + image_label()[indexed_label[key]],
                        "title": key,
                        "fav": 1,
                        "description": "No additional descriptions.",

                    })
    sorted_result.sort(key=lambda x: -x["coef"])
    return sorted_result


def index_dataset(path):
    global model
    model.eval()
    lst = os.listdir(path)
    for i in lst:
        feat, logit = index_image(path, i)
        print("Indexing data", path + "\\" + i, logit, image_label()[logit])


def temporary_bookmark_add(id):
    print(session)
    if 'favlist' not in session:
        print("FAV RESET")
        session['favlist'] = "[]"
    fav_list = json.loads(session['favlist'])
    fav_list = set(fav_list)
    fav_list.add(id)
    fav_list = list(fav_list)
    fav_list = json.dumps(fav_list)
    session['favlist'] = fav_list
    print("ADDED", fav_list)
    print("ADDED", session)


def temporary_bookmark_remove(id):
    if 'favlist' not in session:
        print("FAV RESET")
        session['favlist'] = "[]"
    fav_list = json.loads(session['favlist'])
    fav_list = set(fav_list)
    fav_list.remove(id)
    fav_list = list(fav_list)
    fav_list = json.dumps(fav_list)
    session['favlist'] = fav_list


def temporary_bookmark_get():
    if 'favlist' not in session:
        print("FAV RESET")
        session['favlist'] = "[]"
    fav_list = json.loads(session['favlist'])
    fav_list = set(fav_list)
    print("GET", fav_list)
    return fav_list


def temporary_bookmark_remove_all(id):
    session['favlist'] = "[]"


# Tensorflow Part


# show_neighbors(random.randint(0, len(extracted_features)), indices, neighbor_list)

def get_top_k_similar(image_data, pred, pred_final, k):
    print("total data", len(pred))
    print(image_data.shape)
    # for i in pred:
    # print(i.shape)
    # break
    os.mkdir('static/result')

    # cosine calculates the cosine distance, not similiarity. Hence no need to reverse list
    top_k_ind = np.argsort([cosine(image_data, pred_row) \
                            for ith_row, pred_row in enumerate(pred)])[:k]
    print(top_k_ind)

    for i, neighbor in enumerate(top_k_ind):
        print("WWWWWWW")
        print(pred_final)
        print(len(pred_final))
        print(neighbor)
        image = imread(pred_final[neighbor])
        # timestr = datetime.now().strftime("%Y%m%d%H%M%S")
        # name= timestr+"."+str(i)
        name = pred_final[neighbor]
        tokens = name.split("\\")
        img_name = tokens[-1]
        print(img_name)
        name = 'static/result/' + img_name
        imsave(name, image)


def create_inception_graph():
    """"Creates a graph from saved GraphDef file and returns a Graph object.

    Returns:
      Graph holding the trained Inception network, and various tensors we'll be
      manipulating.
    """
    with tf.Session() as sess:
        model_filename = os.path.join(
            'imagenet', 'classify_image_graph_def.pb')
        print(model_filename)
        with gfile.FastGFile(model_filename, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            bottleneck_tensor, jpeg_data_tensor, resized_input_tensor = (
                tf.import_graph_def(graph_def, name='', return_elements=[
                    BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME,
                    RESIZED_INPUT_TENSOR_NAME]))
    return sess.graph, bottleneck_tensor, jpeg_data_tensor, resized_input_tensor


def run_bottleneck_on_image(sess, image_data, image_data_tensor,
                            bottleneck_tensor):
    bottleneck_values = sess.run(
        bottleneck_tensor,
        {image_data_tensor: image_data})
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values


def recommend(imagePath):
    tf.reset_default_graph()
    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )
    sess = tf.Session(config=config)
    graph, bottleneck_tensor, jpeg_data_tensor, resized_image_tensor = (create_inception_graph())
    image_data = gfile.FastGFile(imagePath, 'rb').read()
    features = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)
    with open('neighbor_list_recom.pickle', 'rb') as f:
        neighbor_list = pickle.load(f)
    print("loaded images")
    return features

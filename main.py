import json
from flask import session
from flask import Flask, request, make_response
from flask import render_template
from flask_cors import cross_origin
from backend.back import *

INFER_FRAMEWORK = "pytorch"  # pytorch or tensorflow

app = Flask(__name__)
app.secret_key = b'\x1d\xa7mZ\xb6q\xb3\xe89|\x94?y\xd4\x95$'


# Frontend Mapping
@app.route("/")
@app.route("/index.html")
@app.route("/search")
@app.route("/search/")
@app.route("/bookmarks")
@app.route("/bookmarks/")
def hello_world():
    return render_template('dist/index.html')


@app.route("/assets/<file>")
@cross_origin()
def hci_get_assets(file=None):
    path = os.path.abspath(__file__)
    path = "\\".join(path.split("\\")[:-1])
    with open(path + "/templates/dist/assets/" + file, "r") as f:
        ret = f.read()
    tp = "none"
    if file.endswith(".js"):
        tp = 'application/x-javascript'
    if file.endswith(".css"):
        tp = 'text/css'
    if file.endswith(".svg"):
        tp = 'image/svg+xml'
    return ret, 200, {'Content-Type': tp}


@app.route("/image/<file>")
@cross_origin()
def get_assets(file=None):
    path = os.path.abspath(__file__)
    path = "\\".join(path.split("\\")[:-1])
    st = "/image/"
    if INFER_FRAMEWORK == "tensorflow":
        st = "/database/dataset/"
    with open(path + st + file, "rb") as f:
        ret = f.read()
    tp = "none"
    if file.endswith(".png"):
        tp = 'image/png'
    if file.endswith(".jpg"):
        tp = 'image/jpg'
    if file.endswith(".jfif"):
        tp = 'image/jfif'
    response = make_response(ret)
    response.headers['Content-Type'] = tp
    return response


# Mocked API
@app.route("/api/findSimilarImages", methods=['post'])
@cross_origin()
def api_find_similar_images():
    basedir = os.path.abspath(os.path.dirname(__file__))
    img = request.files.get('image')
    path = basedir + "/static/image/"
    file_path = path + img.filename
    img.save(file_path)
    feat, logit = index_image(None, file_path, test=True)
    sim_list = similarity(feat, logit)
    if INFER_FRAMEWORK == "tensorflow":
        dict_result = {
            "feature": feat.tolist(),
            "argmax_class": 0,
            "argmax_label": "Not supported for TF",
            "similarity_list": json.dumps(sim_list),
            "save_path": "http://localhost:5000/" + "/static/image/" + img.filename,
            "intern_path": "/static/image/" + img.filename
        }
    else:
        dict_result = {
            "feature": feat.tolist(),
            "argmax_class": int(logit),
            "argmax_label": image_label()[logit],
            "similarity_list": json.dumps(sim_list),
            "save_path": "http://localhost:5000/" + "/static/image/" + img.filename,
            "intern_path": "/static/image/" + img.filename
        }
    return json.dumps(dict_result), 200, {'Content-Type': 'application/json',
                                          "Access-Control-Allow-Headers": 'Content-Type',
                                          'Access-Control-Allow-Credentials': 'true',
                                          'Access-Control-Allow-Methods': "POST"
                                          }


@app.route("/api/findSimilarImagesRefined", methods=['post'])
@cross_origin()
def api_find_similar_images_refined():
    basedir = os.path.abspath(os.path.dirname(__file__))
    rf = json.loads(request.get_data(as_text=True))
    label = rf.get('label')
    path = rf.get('path')
    file_path = basedir + path
    feat, logit = index_image(None, file_path, test=True)
    sim_list = similarity(feat, logit, label)
    if INFER_FRAMEWORK == "tensorflow":
        dict_result = {
            "feature": feat.tolist(),
            "argmax_class": 0,
            "argmax_label": "Not supported for TF",
            "similarity_list": json.dumps(sim_list),
            "save_path": "http://localhost:5000/" + file_path,
            "intern_path": path
        }
    else:
        dict_result = {
            "feature": feat.tolist(),
            "argmax_class": int(logit),
            "argmax_label": image_label()[logit],
            "similarity_list": json.dumps(sim_list),
            "save_path": "http://localhost:5000/" + file_path,
            "intern_path": path
        }
    return json.dumps(dict_result), 200, {'Content-Type': 'application/json',
                                          "Access-Control-Allow-Headers": 'Content-Type',
                                          'Access-Control-Allow-Credentials': 'true',
                                          'Access-Control-Allow-Methods': "POST"
                                          }


@app.route("/api/addBookmark", methods=['post'])
@cross_origin()
def api_add_favorite():
    print(request.origin)
    rf = json.loads(request.get_data(as_text=True))
    id = rf['id']
    temporary_bookmark_add(id)
    return json.dumps({'code': 200, 'data': 'success'}), 200, {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Headers": 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': "POST"
    }


@app.route("/api/removeBookmark", methods=['post'])
@cross_origin()
def api_delete_favorite():
    rf = json.loads(request.get_data(as_text=True))
    id = rf['id']
    temporary_bookmark_remove(id)
    return json.dumps({'code': 200, 'data': 'success'}), 200, {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Headers": 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': "POST"
    }


@app.route("/api/getBookmark", methods=['post', 'get'])
@cross_origin()
def api_get_favorite():
    st = list(temporary_bookmark_get())
    return json.dumps({'code': 200, 'data': json.dumps(st)}), 200, {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Headers": 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': "POST"
    }


@app.route("/api/clearBookmark", methods=['post'])
@cross_origin()
def api_get_favorite_remove():
    temporary_bookmark_remove_all(0)
    return json.dumps({'code': 200, 'data': 'success'}), 200, {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Headers": 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': "POST"
    }


@app.route("/api/getBookmarkList", methods=['post', 'get'])
@cross_origin()
def api_get_favorite_list():
    rf = json.loads(request.get_data(as_text=True))
    if 'label' in rf:
        sim_list = get_fav_list(rf['label'])
    else:
        sim_list = get_fav_list()
    return json.dumps({'code': 200, 'data': json.dumps(sim_list)}), 200, {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Headers": 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': "POST,GET"
    }


# Caching
def cache():
    path = os.path.abspath(__file__)
    path = "\\".join(path.split("\\")[:-1])
    index_dataset(path + "/image")


if INFER_FRAMEWORK == "tensorflow":
    print("Using Tensorflow+InceptionV3")
    extracted_features = np.zeros((3000, 2048), dtype=np.float32)
    with open('saved_features_recom.txt') as f:
        for i, line in enumerate(f):
            extracted_features[i, :] = line.split()
    set_tf()
    path = os.path.abspath(__file__)
    path = "\\".join(path.split("\\")[:-1])
    index_for_tensorflow(path, extracted_features)
    print("loaded extracted_features")

else:
    print("Using PyTorch+ResNet34")
    print("\n【About Assignment】 PyTorch implementation does not based on the code provided in the QQ Group."
          "This will use SMALLER dataset and DIFFERENT feature extraction methods."
          "To use Tensorflow+InceptionV3 and larger dataset provided by teacher, refer to `before-running.md`"
          "and modify the code.\n")
    print("\n【Model Download】 Pytorch might download the pretrained model from PyTorchHub. Please make sure your network"
          "is successfully established.\n")
    cache()

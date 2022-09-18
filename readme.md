<h2 align = "center"> Assignment 2 for Human Computer Interaction</h2>
<h3 align = "center"> Information Retrieval</h3>
<p align="center">Aeroraven</p>

### A. How to Run

Deep Learning models are not uploaded for they are too large!

Inference Database is not uploaded too.

#### Choose Model & Framework (PyTorch/TensorFlow)

Several codes had been written before the requirements was released. Therefore, PyTorch is used for the default inference framework. The app now supports PyTorch(ResNet) and  Tensorflow(InceptionV3, provided by teacher)

To change the inference model, please modify the code in `main.py`

```python
# main.py line 8
INFER_FRAMEWORK = "pytorch"  # pytorch or tensorflow
```

**Whether you use TensorFlow or PyTorch, both packages should be installed.**



#### Standard

**For Windows:** Just execute the batchfile `flask_run.bat` or `run.bat`

**For Linux:** Execute the instructions in the terminal

```shell
export FLASK_APP=main
flask run
```



#### Advanced

When modifications are done to the layouts and the styles of the web pages, following steps are needed.

First download `Node.js` here: <https://nodejs.org>

Then, check if `Node.js` is installed

```shell
node -v
```

**For Windows:** Just execute the batchfile `advanced_run.bat`

**For Linux:** Execute the instructions in the terminal

```shell
cd frontend
npm install
npm run build
cd templates
mkdir dist
cd dist
mkdir assets
cd ..
cd ..
rm -rf templates/dist/assets/*
cp frontend/dist templates/dist
cp frontend/dist/assets templates/dist/assets
export FLASK_APP=main
flask run
```



### B. Running Instruction & Prerequisites

#### Development Environment

- Windows == 10
- Python == 3.9
- Chrome == 101
- Node == 14.17

Backend: Python(Flask)
Fronted: Vue3(TypeScript+CSS3)

#### System & Environment Requirements

- Network Connection
  - Access to <https://download.pytorch.org/>
    - This aims to download the pretrained model
    - Sometimes this access requires virtual private network.
- Python >= 3.7
  - Python == 3.9 is used in the development
- Proper Web Browser
  - IE, Baidu Browser, UC Browser is not supported
  - Edge >= 79
  - Chrome >=63
  - Safari >= 11.1
  - FireFox >= 67
  - Opera >= 50
- Port 5000 is available

#### Optional System & Environment Requirements

Following requirements are needed only when you want to modify front-end pages

- Node.js & NPM
  - Vue-CLI

Following requirements are needed only when you want to accelerate your inference speed

- CUDA >= 10.2

#### Required Python Packages

| Package        | Version      | Function                |
| -------------- | ------------ | ----------------------- |
| Flask          | 2.0.3        | Server Establishment    |
| Flask-Cors     | 3.0.10       | Cross-Origin Processing |
| Flask-HTTPAuth | 4.5.0        |                         |
| torch          | 1.9.0+cu102  | Model inference         |
| torchvision    | 0.10.0+cu102 | ResNet Provision        |
| tensorflow     | 2.8.0        | InceptionV3 Inference   |
| opencv-python  | 4.5.3.56     | Image Processing        |
| albumentations | 1.0.3        | Image Processing        |
| numpy          | 1.22.3       | Math                    |

Use following instruction to install python packages

```shell
pip3 install <package_name>==<version>
```

Or, use the following instructions.

```shell
pip3 install Flask
pip3 install torch torchvision torchaudio
pip3 install albumentations
pip3 install tensorflow
pip3 install Flask-Cors
pip3 install opencv-python
pip3 install tensorflow
```





### 1. Requirements of Image Search Task

The image search task is a promising variant of web search. Its significant characteristics is that user can upload the images, instead of plain text, to find related information.

All image search engines are established based on following aspects.

- **Problem Formulation**: Users' needs should be gathered and investigated to define the outline for system.
- **Database Establishment**: Images should be collected and a database containing images should be established. This step can be done via spiders, or using existing databases.
- **Algorithm Adoption**: All images contained in the database should be preprocessed via few algorithms. First, features of images should be extracted and be vectorized. Neural networks can serve as the algorithm for the feature extraction. Second, similarity algorithm should be defined in order to give users results with high relevance.

Like the traditional web search, image search also works under the five-stage framework, that is, formulation, initiation of action, result review, refinement and use. And the user-side requirement can be elicited from these five steps.

- **Formulation**:
  - Images can be uploaded via a proper interface
  - Images can be previewed or changed after being uploaded
  - A button for search initiation should exist
- **Action Initiation**:
  - Explicit actions can be initiated by buttons with consistent labels. (Including image uploading, search, bookmark and refining)
- **Review of Results**:
  - Keeps uploaded images and refinement information visible
  - Provide the overview of results (including numbers of results)
  - Resemble results should be prioritized
  - Detail of each result (like the high-resolution image, tags and other information) can be inspected
- **Refinement**:
  - Search suggestions(like the inferred user intention, inferred tag of upload information) can be given to users.
  - Allow users to make changes to the parameters of the search, and allow users to initiate a refined search within current result (using certain keywords or certain tags).
- **Use**:
  - Explore collecting explicit feedback. (Allow users to add bookmarks)

Requirements mentioned in `five-step framework` above are all implemented in the assignment.

### 2. Description of Implementation Details

#### Some Notes

Snapshots below are the result using PyTorch and image-net pretrained ResNet34 model. And the smaller dataset (different from the one provided in the QQ Group) is used when the screen was captured.

#### Image Upload

User can choose and upload the image by clicking on the eclipse input area. If the wrong picture is selected, they can click on the area again and reselect an image. Dragging file to the area is also acceptable!

Users need a feedback which tells them whether the image is successfully uploaded or not. Thus a notification is added and will pop up when the browser fails to upload the image.

Layout(HTML Code):

```html
<n-spin :show="show">
  <input id="get_file" type="file" class="" style="display:none;visibility:hidden;" 
  placeholder="You can drag the image or paste the URL here!"
  v-on:change="onFileChange"/>
  <label for="get_file" class="zw-hci2-main-search-box" style="color:#ccc">{{filename}}</label>
  <template #description>
    Uploading the image. Please wait.
  </template>
</n-spin>
```

Action(TypeScript Code):

```typescript
function onFileChange(event:Event){
  let obj:HTMLInputElement = <HTMLInputElement>document.getElementById('get_file')
  if(obj!=null){
    if(obj.files!=null){
      uploaded = true
      filename.value = obj.files[0].name + " (Click here to change the file)"
      imageUrl.value = window.URL.createObjectURL(obj.files[0])
      return
    }
  }
  message.error(
    "Seems the image you just uploaded is not valid.",
    { duration: 5000 }
  )
}

```

![img](./img/2.PNG)

#### Image Preview

After the users upload the image to the server, they can check their uploaded picture by simply clicking on `View Image` button. Tips will show if users click on the button withou uploading images.

The implementation involves a modal window provided by `Naive-UI` to improve the visual feeling.

Layout(HTML Code):

```html
<n-modal v-model:show="showModal">
  <n-card
    style="width: 600px"
    :bordered="false"
    size="huge"
    role="dialog"
    aria-modal="true"
  >
    <template #header>
      <div class="zw-hci2-modal-title">Image Preview</div>
    </template>
    <template #header-extra>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button quaternary circle type="info" size="large" @click="showModal=false">
            <template #icon >
              <n-icon size="20">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" style="color:#444"><path d="M289.94 256l95-95A24 24 0 0 0 351 127l-95 95l-95-95a24 24 0 0 0-34 34l95 95l-95 95a24 24 0 1 0 34 34l95-95l95 95a24 24 0 0 0 34-34z" fill="currentColor"></path></svg>
              </n-icon>
            </template>
          </n-button>
        </template>
        Close
      </n-tooltip>
    </template>
    You can check your uploaded image here.<br/><br/>
    <n-alert title="No Image" type="info" v-if="imageUrl==''">
      You have not upload any image yet.
    </n-alert>
    <img :src="imageUrl" style="max-width:500px;"/>
  </n-card>
</n-modal>
```

![image](./img/1.PNG)

#### Search Initiation

By clicking on `Search Now`, the image will be uploaded to the server. Here, network delay should be considered because some high-resolution images often have large size. If the network request timeout exceeded, the proper information should be told to users.

Here a circular progress bar is added to indicate whether the image is being uploaded to the server. And information will show if the exception occurs.

Script(TypeScript Code):

```typescript
function submit(){
  if(uploaded==false){
    message.error(
      "You need to upload a valid image before initiate the query!",
      { duration: 5000 }
    )
    return ;
  }
  show.value = true
  let formData = new FormData()
  let imagefile = <HTMLInputElement>document.getElementById('get_file')
  if(imagefile!=null){
    if(imagefile.files!=null){
      formData.append("image",imagefile.files[0])
    }
  }
  Backend.apiFindSimilarImages(formData).then((response:any)=>{
    console.log(response)
    Router.push({name:'search',params:response})
  }).catch((exception:any)=>{
    message.error(
      "An unexpected problem occurred:"+exception,
      { duration: 5000 }
    )
  })
}
```

![image](./img/3.PNG)

#### Result Overview & Refinement Suggestion

After the request is well handled by the server, users can see the overview of the results, which contain similar pictures(including their brief description, like tags). Users can also the number of result entries under the title `Search Result`.

Also, a refinement suggestion is given at the left column. The image the user uploaded is fed into the `ResNet-34` classifier and obtained a logit tensor. Argmax is performed on this tensor to get the most possible tag of the submitted picture to obtain the most possible class. The refinment suggestion will show in the form of `Are you looking for *** ?`

In this phase, the code of the back-end is modified. Following are server-side codes.

Model Inference Code (Python Code):

```Python
def index_image(base_path, path, test=False):
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
```

Similarity Calculation (Python Code):

```python
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
        dist = np.dot(feat_vector, indexes[key]) / d1 / d2
        if dist < 0.4:
            continue
        if add_label is not None:
            ins = False
            for i in label_list:
                if key.find(i) != -1:
                    ins = True
                if image_label()[indexed_label[key]].find(i) != -1:
                    ins = True
            if ins:
                cate_f = key.split("-")[0]
                sorted_result.append({
                    "image": "http://localhost:5000/image/" + key,
                    "coef": int(dist * 10000),
                    "labels": cate_f+", "+image_label()[indexed_label[key]],
                    "title": key,
                    "fav": int(key in fav_list),
                    "description": "No additional descriptions.",

                })
        else:
            cate_f = key.split("-")[0]
            sorted_result.append({
                "image": "http://localhost:5000/image/" + key,
                "coef": int(dist * 10000),
                "labels": cate_f+", "+image_label()[indexed_label[key]],
                "title": key,
                "fav": int(key in fav_list),
                "description": "No additional descriptions.",

            })
    sorted_result.sort(key=lambda x: -x["coef"])
    return sorted_result
```

Backend API (Python Code):

```Python
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
```

And a new `Vue` view is created for the overview page.

Layout for the Result Entries (HTML Code):

```html
<div class="zw-hci2-fvkgrid-right zw-hci2-fvkgrid-right-media" >
  <div class="zw-hci2-result-panel zw-hci2-panel" style="grid-column: span 8 / span 8">
    <div class="zw-hci2-blue">
      <n-icon size="25" class="zw-hci2-icon-modifier">
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32"><path d="M11.61 29.92a1 1 0 0 1-.6-1.07L12.83 17H8a1 1 0 0 1-1-1.23l3-13A1 1 0 0 1 11 2h10a1 1 0 0 1 .78.37a1 1 0 0 1 .2.85L20.25 11H25a1 1 0 0 1 .9.56a1 1 0 0 1-.11 1l-13 17A1 1 0 0 1 12 30a1.09 1.09 0 0 1-.39-.08zM17.75 13l2-9H11.8L9.26 15h5.91l-1.59 10.28L23 13z" fill="currentColor"></path></svg>
      </n-icon>
      <b class="zw-hci2-user-panel-title zw-hci2-user-panel-title-bw">Search Result</b>
    </div>
    <div style="margin-bottom:5px">
      Showing {{resultList.length}} {{resultList.length>1?'results':'result'}}
    </div>
    <div style="height:80%;position:relative;">
      <n-grid cols="60" item-responsive style="overflow-y:scroll; padding-left:8px;height:100%">
        <n-grid-item span="58" style="width:100%">
          <div>
            <n-alert title="Empty Result" type="info" v-if="resultList.length==0" style="width:100%">
              There's no results that match your requirements.
            </n-alert>
          </div>
        </n-grid-item>
        
        <n-grid-item span="30 600:20 800:15 1200:12" v-for="i in resultList.length" :key="i">
          <div class="zw-hci2-recommend">
            <div>
              <img class="zw-hci2-image" :src="resultList[i-1].image"/>
            </div>
            <div class="zw-hci2-recommend-content">
              <div class="zw-hci2-recommend-content-title">
                {{resultList[i-1].title}}
              </div>
              <hr color="#cccccc" class="zw-hci2-recommend-content-hr"/>
              <div class="zw-hci2-recommend-content-body">
                
                <b>Tags:</b> 
                  <span style="text-transform:capitalize">{{resultList[i-1].labels}} </span>
                <br/>
                <b>Description:</b>{{resultList[i-1].description}}
                <br/>
                <br/>
              </div>
              <div>
                <n-tooltip trigger="hover">
                  <template #trigger>
                    <n-button quaternary circle type="info" size="large" @click="showDetail(i)">
                      <template #icon >
                        <n-icon size="20">
                          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24" style="color:#444"><path d="M2 6c.55 0 1-.45 1-1V4c0-.55.45-1 1-1h1c.55 0 1-.45 1-1s-.45-1-1-1H4C2.34 1 1 2.34 1 4v1c0 .55.45 1 1 1zm3 15H4c-.55 0-1-.45-1-1v-1c0-.55-.45-1-1-1s-1 .45-1 1v1c0 1.66 1.34 3 3 3h1c.55 0 1-.45 1-1s-.45-1-1-1zM20 1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1c.55 0 1 .45 1 1v1c0 .55.45 1 1 1s1-.45 1-1V4c0-1.66-1.34-3-3-3zm2 17c-.55 0-1 .45-1 1v1c0 .55-.45 1-1 1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1c1.66 0 3-1.34 3-3v-1c0-.55-.45-1-1-1zm-3-3.13V9.13c0-.72-.38-1.38-1-1.73l-5-2.88c-.31-.18-.65-.27-1-.27s-.69.09-1 .27L6 7.39c-.62.36-1 1.02-1 1.74v5.74c0 .72.38 1.38 1 1.73l5 2.88c.31.18.65.27 1 .27s.69-.09 1-.27l5-2.88c.62-.35 1-1.01 1-1.73zm-8 2.3l-4-2.3v-4.63l4 2.33v4.6zm1-6.33L8.04 8.53L12 6.25l3.96 2.28L12 10.84zm5 4.03l-4 2.3v-4.6l4-2.33v4.63z" fill="currentColor"></path></svg>
                        </n-icon>
                      </template>
                    </n-button>
                  </template>
                  View Details
                </n-tooltip>

                <n-tooltip trigger="hover" v-if="resultList[i-1].fav==0">
                  <template #trigger>
                    <n-button quaternary circle type="info" size="large" @click="addBookmark(i)">
                      <template #icon >
                        <n-icon size="20">
                          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32" style="color:#444"><path d="M22.45 6a5.47 5.47 0 0 1 3.91 1.64a5.7 5.7 0 0 1 0 8L16 26.13L5.64 15.64a5.7 5.7 0 0 1 0-8a5.48 5.48 0 0 1 7.82 0l2.54 2.6l2.53-2.58A5.44 5.44 0 0 1 22.45 6m0-2a7.47 7.47 0 0 0-5.34 2.24L16 7.36l-1.11-1.12a7.49 7.49 0 0 0-10.68 0a7.72 7.72 0 0 0 0 10.82L16 29l11.79-11.94a7.72 7.72 0 0 0 0-10.82A7.49 7.49 0 0 0 22.45 4z" fill="currentColor"></path></svg>
                        </n-icon>
                      </template>
                    </n-button>
                  </template>
                  Favorite
                </n-tooltip>
                <n-tooltip trigger="hover" v-if="resultList[i-1].fav==1">
                  <template #trigger>
                    <n-button quaternary circle type="info" size="large" @click="removeBookmark(i)">
                      <template #icon >
                        <n-icon size="20">
                          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 28 28" style="color:#444"><g fill="none"><path d="M14.604 6.193a6.519 6.519 0 1 1 9.509 8.913l-9.58 9.672a.75.75 0 0 1-1.066 0l-9.58-9.672a6.518 6.518 0 0 1-.263-8.892c2.588-2.943 7.17-2.953 9.772-.021l.604.68l.604-.68z" fill="currentColor"></path></g></svg>
                        </n-icon>
                      </template>
                    </n-button>
                  </template>
                  Cancel Favorite
                </n-tooltip>

              </div>
            </div>
          </div>
        </n-grid-item>
      </n-grid>
    </div>
  </div>
    
</div>
```

Layout for the Left Column(HTML Code):

```html
<div class="zw-hci2-fvkgrid-left zw-hci2-fvkgrid-left-media">
  <div class="zw-hci2-user-panel zw-hci2-panel">
    <!--Title-->
    <div>
      <n-icon size="25" class="zw-hci2-icon-modifier">
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512"><path d="M473.66 210c-16.56-12.3-37.7-20.75-59.52-24c-6.62-39.18-24.21-72.67-51.3-97.45c-28.69-26.3-66.63-40.76-106.84-40.76c-35.35 0-68 11.08-94.37 32.05a149.61 149.61 0 0 0-45.32 60.49c-29.94 4.6-57.12 16.68-77.39 34.55C13.46 197.33 0 227.24 0 261.39c0 34.52 14.49 66 40.79 88.76c25.12 21.69 58.94 33.64 95.21 33.64h104V230.42l-48 48l-22.63-22.63L256 169.17l86.63 86.62L320 278.42l-48-48v153.37h124c31.34 0 59.91-8.8 80.45-24.77c23.26-18.1 35.55-44 35.55-74.83c0-29.94-13.26-55.61-38.34-74.19z" fill="currentColor"></path><path d="M240 383.79h32v80.41h-32z" fill="currentColor"></path></svg>
      </n-icon>
      <b class="zw-hci2-user-panel-title">Uploaded Image</b>
    </div>
    <!--Image-->
    <div class="zw-hci2-up-image-frame-wrapper">
      <div class="zw-hci2-up-image-frame">
        <div class="zw-hci2-up-image-frame-in">
          <img class="zw-hci2-image2" :src="save_path"/>
        </div>
      </div>
    </div>
    <!--Refinement-->
    <br/>
    <div>
      <n-icon size="25" class="zw-hci2-icon-modifier">
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 20 20"><g fill="none"><path d="M9.104 2.9a1 1 0 0 1 1.794 0l1.93 3.91l4.317.628a1 1 0 0 1 .554 1.706l-3.124 3.044l.738 4.3a1 1 0 0 1-1.451 1.054l-3.86-2.03l-3.862 2.03a1 1 0 0 1-1.45-1.055l.737-4.299l-3.124-3.044a1 1 0 0 1 .554-1.706l4.317-.627l1.93-3.912zM4.39 12.687a.5.5 0 0 1-.078.703l-2.5 2a.5.5 0 1 1-.624-.781l2.5-2a.5.5 0 0 1 .702.078zM4.312 5.11a.5.5 0 1 1-.624.78l-2.5-2a.5.5 0 1 1 .624-.78l2.5 2zm11.297 7.578a.5.5 0 0 0 .079.703l2.5 2a.5.5 0 1 0 .624-.781l-2.5-2a.5.5 0 0 0-.703.078zm.079-7.578a.5.5 0 0 0 .624.78l2.5-2a.5.5 0 1 0-.624-.78l-2.5 2z" fill="currentColor"></path></g></svg>
      </n-icon>
      <b class="zw-hci2-user-panel-title">Result Refinement</b>
    </div>
    <p>Not satisfied with the result? You can try these options below!</p>
    <p>Are you looking for: <u><a @click="refineRecommend">{{recommend_tag}}</a> </u> ?</p>
    <input class="zw-hci2-refine-input" v-model="search_label" placeholder="Put extra labels here to refine the result"/>
    <n-tooltip trigger="hover" placement="bottom">
      <template #trigger>
        <n-button color="#ffffff" type="info" size="large" class="zw-hci2-main-search-btn" style="width:100%" v-on:click="submitRefine">
          <template #icon >
            <n-icon size="20">
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32"><path d="M30 6h-4V2h-2v4h-4v2h4v4h2V8h4V6z" fill="currentColor"></path><path d="M24 28.586l-5.975-5.975a9.023 9.023 0 1 0-1.414 1.414L22.586 30zM4 17a7 7 0 1 1 7 7a7.008 7.008 0 0 1-7-7z" fill="currentColor"></path></svg>
            </n-icon>
          </template>
          Refine Search
        </n-button>
      </template>
      Refine the search result using the additional label information
    </n-tooltip>
    <center style="margin-top:10px;margin-bottom:10px;display:inline-block;text-align:center;width:100%;">or</center>
    <n-tooltip trigger="hover" placement="bottom">
      <template #trigger>
        <n-button color="#ffffff" type="info" size="large" class="zw-hci2-main-search-btn" style="width:100%" v-on:click="backHome">
          <template #icon >
            <n-icon size="20">
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24"><path d="M9 13L5 9l4-4M5 9h11a4 4 0 0 1 0 8h-1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg></n-icon>
          </template>
          Reselect Image
        </n-button>
      </template>
      Go back to Home and initiate a new visual query
    </n-tooltip>
  </div>
</div>
```

Client-side Script(TypeScript Code):

```TypeScript
let detailedItem = ref<ResultList>({
  image:"",
  labels:"",
  title:"",
  description:"",
  coef:0,
  fav:0
});
let resultList = ref<ResultList[]>([
  {image:"",labels:"Animal",title:"Nope",description:"No?",coef:0,fav:0}
])
let route = useRoute()
console.log(<string><unknown>(route.params))
if(JSON.stringify(<unknown>(route.params)) =="{}"){
  backHome()
}else{
  resultList.value = <ResultList[]><unknown>JSON.parse(<string>route.params.similarity_list)
  save_path.value = <string>route.params.save_path;
  intern_path.value = <string>route.params.intern_path;
  recommend_tag.value = (<string>route.params.argmax_label).split(",")[0];
  console.log(route.params.save_path)
}
```

![image](./img/4.PNG)

#### Result Detail

By clicking on the cube icon in the card of each entry, users can see the detail of the search results, including the detailed tags, similarity and the high-resolution view of the result image.

The detail information of the entry will show in a modal window.

Layout (HTML Code):

```html
<n-modal v-model:show="showModal" class="zw-hci2-modal">
  <n-card
    style="width: 600px"
    :bordered="false"
    size="huge"
    role="dialog"
    aria-modal="true"
  >
    <template #header>
      <div class="zw-hci2-modal-title">Image Detail</div>
    </template>
    <template #header-extra>
      <n-tooltip trigger="hover">
        <template #trigger>
          <n-button quaternary circle type="info" size="large" @click="showModal=false">
            <template #icon >
              <n-icon size="20">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" style="color:#444"><path d="M289.94 256l95-95A24 24 0 0 0 351 127l-95 95l-95-95a24 24 0 0 0-34 34l95 95l-95 95a24 24 0 1 0 34 34l95-95l95 95a24 24 0 0 0 34-34z" fill="currentColor"></path></svg>
              </n-icon>
            </template>
          </n-button>
        </template>
        Close
      </n-tooltip>
    </template>
    <img :src="detailedItem.image" class="zw-hci2-large-im"/>
    <div class="zw-hci2-recommend-content-title" style="font-size:20px !important;">
      {{detailedItem.title}}
    </div>
    <hr color="#cccccc" class="zw-hci2-recommend-content-hr"/>
    <big><b style="color:#0099ff">Similarity</b>: <b>{{detailedItem.coef/100}} % </b> </big> 

    <n-tooltip trigger="hover" placement="bottom">
      <template #trigger>
        <n-button quaternary circle type="info" size="large" style="position:relative;top:5px;">
          <template #icon >
            <n-icon size="17">
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" style="color:#444;"><path d="M504 256c0 136.997-111.043 248-248 248S8 392.997 8 256C8 119.083 119.043 8 256 8s248 111.083 248 248zM262.655 90c-54.497 0-89.255 22.957-116.549 63.758c-3.536 5.286-2.353 12.415 2.715 16.258l34.699 26.31c5.205 3.947 12.621 3.008 16.665-2.122c17.864-22.658 30.113-35.797 57.303-35.797c20.429 0 45.698 13.148 45.698 32.958c0 14.976-12.363 22.667-32.534 33.976C247.128 238.528 216 254.941 216 296v4c0 6.627 5.373 12 12 12h56c6.627 0 12-5.373 12-12v-1.333c0-28.462 83.186-29.647 83.186-106.667c0-58.002-60.165-102-116.531-102zM256 338c-25.365 0-46 20.635-46 46c0 25.364 20.635 46 46 46s46-20.636 46-46c0-25.365-20.635-46-46-46z" fill="currentColor"></path></svg>
            </n-icon>
          </template>
        </n-button>
      </template>
      The similarity measurement adopted is the consine similarity of the last convolution feature obtained by the ImageNet-pretrained ResNet-34 model.
    </n-tooltip>
    <br/>

    <b>Auto-labeled Tags</b>: <span style="text-transform:capitalize">{{detailedItem.labels}}</span><br/>
    <b>Description</b>: {{detailedItem.description}}<br/>
  </n-card>
</n-modal>
```

![image](./img/5.PNG)

#### Result Refinement

After the initial search, users can refine the search results by adding additional informations(like the tag) to the image and then click on `Refine Search` button. Then the result will only contain entries that meets the requirement given in the additional information.

Here is the example.

Before Refinement:

![image](./img/6.PNG)

After Refinement:

![image](./img/7.PNG)

Following is the implementation detail.

Server-side API (Python Code):

```python
@cross_origin()
def api_find_similar_images_refined():
    basedir = os.path.abspath(os.path.dirname(__file__))
    rf = json.loads(request.get_data(as_text=True))
    label = rf.get('label')
    path = rf.get('path')
    file_path = basedir + path
    feat, logit = index_image(None, file_path, test=True)
    sim_list = similarity(feat, logit, label)
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
```

Client-side Script(TypeScript Code):

```typescript
function refineRecommend(){
  let x = {
    'path':intern_path.value,
    'label':recommend_tag.value
  }
  Backend.apiFindSimilarImagesRefined(x).then((response:any)=>{
    resultList.value = <ResultList[]><unknown>JSON.parse(<string>response.similarity_list)
    message.success(
      "Results are refined",
      { duration: 5000 }
    )
  })
}
function submitRefine(){
  let x = {
    'path':intern_path.value,
    'label':search_label.value
  }
  Backend.apiFindSimilarImagesRefined(x).then((response:any)=>{
    resultList.value = <ResultList[]><unknown>JSON.parse(<string>response.similarity_list)
    message.success(
      "Results are refined",
      { duration: 5000 }
    )
  })
}
```

#### Bookmark Addition & Removal

By clicking on the `heart` icon, users can add the image to the favourite list or remove it from the list. The `filled hear` icon means the user has already added it to the favourite list.

For no remote data bases (like `MySQL`) are provided, `localStorage` provided by the web browser is adopted to simulate the data store.

![image](./img/8.PNG)
(The Image-net does not contain the category `Giant Panda`, thus the auto-labeled tags is not accurate.)

Server-side API(Python Code):

```Python
@app.route("/api/addBookmark", methods=['post'])
@cross_origin()
def api_add_favorite():
    print(request.origin)
    rf = json.loads(request.get_data(as_text=True))
    id = rf['id']
    temporary_bookmark_add(id)
    return json.dumps({'code':200,'data':'success'}), 200, {
        'Content-Type': 'application/json',
        "Access-Control-Allow-Headers": 'Content-Type',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods':"POST"
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
        'Access-Control-Allow-Methods':"POST"
    }
```

Client-side Script (TypeScript Code):

```typescript
function addBookmark(i:number){
  detailedItem.value = resultList.value[i-1]
  let x = {id:detailedItem.value.title}
  Backend.apiAddFavorite(x).then((response:any)=>{
    resultList.value[i-1].fav=1,
    message.success(
      "Bookmark added.",
      { duration: 5000 }
    )
  })
}
function removeBookmark(i:number){
  detailedItem.value = resultList.value[i-1]
  let x = {id:detailedItem.value.title}
  Backend.apiRemoveFavorite(x).then((response:any)=>{
    resultList.value[i-1].fav=0,
    message.success(
      "Bookmark removed.",
      { duration: 5000 }
    )
  })
}
```

#### Bookmark Overview

By clicking on the `star` icon at the right-top corner, users can review images which they have already marked as favourite images. The `Bookmark` page works resembles normal search result page, which users can see the details of the images (like the similarities and tags), remove the bookmark, refine the result, undo the bookmark removal (before reload the page).

Besides, users can reset the favourite list by clicking on `Reset Bookmarks` if they found their tastes shift as time flows.

Page Overview:
![image](./img/9.PNG)

After Refinement:
![image](./img/10.PNG)

#### Other Miscellaneous Implementation Details

##### Request Timeout

To ensure that user can have a quick response from their action, a timeout configuration is set to every network request initiated by the client browser. When the time limit exceeded, the request will be interrupted and intercepted, and users will see the notification on the screen. This can avoid users being tempered for waiting without knowing when the result will be shown.

This is achieved by simply added a configuration entry to `axios`.

TypeScript Code:

```Typescript
const service = axios.create({
  baseURL: "http://localhost:5000/",
  withCredentials:true,
  timeout: 20000,
});
```

##### Front-end And Back-end Separation

To ensure the designs(visual layout, styles, static contents) and transactions(request handling, model inferencing) can be tackled individually, the idea of separating the front-end(designs) and the backend(transaction processing) is introduced in this lab. This allows the designs not be limited by the `Flask` framework, which only provides pure HTML and simple template supports. And the `Flask` server can be simply focusing on tackling transactions.

Thus, the front-end is developed via `Vue3` framework. This provides high flexibility to the page design.

And inorder to host the front-end and back-end on the same port. The front-end pages are compiled using `Vite` (the output is a standalone HTML and a standalone JavaScript file)and then copied to the folder which `Flask` server can handle.

Python Code:

```Python
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
    with open(path + "/image/" + file, "rb") as f:
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
```

##### Decorative Icons

Some icons are attached to buttons to make them prettier. These icons are refernced from `ant-design-icons` (MIT), `fluentui-system-icons`(MIT), `ionicons`(MIT), `carbon`(MIT), `material-design-icons`(MIT) and `tabler-icons`(MIT).

##### Stylesheets

CSS and SCSS is used to beautify the page.

Global Stylesheet (SCSS Code):

```scss
$background_url: "https://wallup.net/wp-content/uploads/2018/10/08/252927-water-animals-dolphins.jpg";
.zw-hci2-main-wrapper{
  background: url($background_url) no-repeat;
  background-size:cover;
  background-position: center top;
  margin: 0px 0px 0px 0px;
  padding: 0px 0px 0px 0px;
  height: 100%;
  position: relative;
}
.zw-hci2-top-bar{
  position: absolute;
  width:100%;
  z-index: 2;
  box-sizing: border-box;
  box-shadow: 0 10px 20px rgba(64,64,64,0.5);
  padding-left:40px;
  padding-top:11px;
  padding-bottom:11px;
  font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-size:20px;
  vertical-align: top;
}
.zw-hci2-top-bar-title-override{
  font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-size:20px;
  padding-left:10px;
  font-weight:bold;
}
.zw-hci2-top-bar::after{
  content: '';
  position: absolute;
  top:0;
  left:0;
  right:0;
  bottom: 0;
  background-position: center top;
 background-size: cover;
 background-attachment: fixed;
  //background: url($background_url) no-repeat;
  background-color: #fff;
  z-index: -3;
  
}
.zw-hci2-top-bar-title{
  font-weight:bold;
}
.zw-hci2-naive-icon-modifier{
  display: inline-block;
  position:relative;
  top:5px;
}
.zw-hci2-vdivider{
  border-width: 5px !important;
}
.zw-hci2-right-topbar{
  float:right;
  padding-right:20px;
  position:relative;
  top:2px;
}
.slide-fade-enter-active {
  transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
}
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}
.slide-fade-enter, .slide-fade-leave-to
  /* .slide-fade-leave-active for below version 2.1.8 */ {
  transform: translateY(1.5vh);
  opacity: 0;
}
```

Home Page (CSS Code):

```css
.zw-hci2-main-title{
  transform:translate(-50%,-50%);
  left:50%;
  top:50%;
  position:absolute;
  text-align:center;
  width:100%
}
.zw-hci2-main-title-c{
  font-size:72px;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-weight: bold;
  font-variant:small-caps;
  color:#fff;
  letter-spacing: 2px;
  word-spacing: 20px;
}
.zw-hci2-main-search-box{
  display:inline-block;
  background-color:#fff;
  border-radius:40px;
  padding-top:15px;
  padding-bottom:15px;
  padding-left: 20px;
  font-size:22px;
  margin-top:0px;
  width:60%;
  border: 1px solid #333;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}
.zw-hci2-main-search-btn{
  //background-color:#fff;
  color:#0099ff !important;
  transform: scale(120%,120%);
  padding-left: 20px;
  padding-right:25px;
}
.zw-hci2-main-search-btn:hover{
  color:#0099ff !important;
}

.zw-hci2-main-search-btn-c{
  transform: scale(120%,120%);
  padding-left: 20px;
  padding-right:25px;
}
.zw-hci2-spacer{
  display:inline-block;
  width:70px;
}
::-webkit-input-placeholder{
  color: #ccc;
}
.n-spin-container{
  --n-text-color:#fff !important;
  --n-color:#fff !important;
}
.n-card-header__main{
  color:#0099ff !important;
  --n-text-color:#0099ff !important;
  font-weight:bold;
}
.zw-hci2-modal-title{
  color:#0099ff !important;
  --n-text-color:#0099ff !important;
  font-weight:bold;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-size:18px;
}
```

Search Overview (CSS Code):

```css

.zw-hci2-main-title{
    position:absolute;
    top:58px;
    width:100%;
    bottom:0px;
}
.zw-hci2-streched-height{
    height:100% !important;
}
.zw-hci2-user-panel{
    background-color:#0099ff;
    height:100%;
    color: #fff;
}
.zw-hci2-result-panel{
    background-color:#fafafa;
}
.zw-hci2-panel{
  font-size:16px;
  padding-top:25px;
  padding-left:30px;
  padding-right:30px;
  height:100% !important;
  font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}
.zw-hci2-user-panel-title{
  font-weight:bold;
  font-size:20px;
  padding-left:10px;
}
.zw-hci2-icon-modifier{
  position:relative;
  top:7px;
}
.zw-hci2-up-image-frame{
  background-color:white;
  width:22vw;
  height:22vw;
  display:inline-block;
  margin-top:20px;
  border-radius: 15px;
  position:relative;
}
.zw-hci2-up-image-frame-in{
  position:absolute;
  left:10px;
  top: 10px;
  right:10px;
  bottom:10px;
  border-radius: 15px;;
  background-color:#eee;
  padding-bottom:20%;
}
.zw-hci2-up-image-frame-wrapper{
  text-align: center;
}
.zw-hci2-blue{
  color:#0099ff;
  padding-bottom: 10px;
}
.zw-hci2-user-panel-title-bw{
  padding-bottom: 50px;
}
.zw-hci2-recommend{
  background-color:#fff;
  margin-bottom:14px;
  border-radius:5px;
  box-shadow: 0px 5px 10px #aaa;
  margin-right:20px;
}
.zw-hci2-image{
  width:100%;
  aspect-ratio: 4/3;
  border-radius:5px 5px 0 0;
}

.zw-hci2-image2{
  width:100%;
  aspect-ratio: 1;
}
.zw-hci2-recommend-content{
  margin-left:10px;
  padding-bottom:10px;
  margin-right:10px;
}
.zw-hci2-recommend-content-title{
  font-weight:bold;
}
.zw-hci2-recommend-content-hr{
  border-color: #ccc;
  border-width: 1px;
  border-top-width: 0px;
}
.zw-hci2-recommend-content-body{
  font-size:14px;
  height:85px;
  overflow-y: hidden;
}

.zw-hci2-main-search-btn{
  //background-color:#fff;
  color:#0099ff !important;
  padding-left: 20px;
  padding-right:25px;
}
.zw-hci2-main-search-btn:hover{
  color:#0099ff !important;
}

.zw-hci2-refine-input{
  width:99%;
  margin-bottom:4px;
  border-radius:4px;
  height:28px;
  border:none;
}
::-webkit-input-placeholder{
  color: #ccc;
}
.zw-hci2-modal-title{
  color:#0099ff !important;
  --n-text-color:#0099ff !important;
  font-weight:bold;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-size:18px;
}
.zw-hci2-fvkgrid-left{
  position: relative;

  display: inline-block;
  height:100%;
}
.zw-hci2-fvkgrid-right{
  position:fixed;

  right:0%;
  bottom:0%;
  top:55px;
  display: inline-block;
}
.zw-hci2-fvkgrid{
  width:100%;
  position:relative;
  height:100%;
}

@media only screen and (max-width: 1100px){
  .zw-hci2-fvkgrid-right-media{
    left:35%;
  }
  .zw-hci2-fvkgrid-left-media{
    width:35%;
  }
}

@media only screen and (min-width: 1100px){
  .zw-hci2-fvkgrid-right-media{
    left:30%;
  }
  .zw-hci2-fvkgrid-left-media{
    width:30%;
  }
}

@media only screen and (min-width: 1500px){
  .zw-hci2-fvkgrid-right-media{
    left:25%;
  }
  .zw-hci2-fvkgrid-left-media{
    width:25%;
  }
}

.zw-hci2-large-im{
  width:500px;
  aspect-ratio: 4/3;
}
.zw-hci2-modal{
  font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}
```


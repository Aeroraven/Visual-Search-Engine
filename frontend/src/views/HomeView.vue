<script setup lang="ts">
import type { AxiosResponse } from 'axios'
import {ref} from 'vue'
import Backend from '../apis/backend'
import Router from '../router/index'
import { useMessage } from 'naive-ui'
import type { MessageProviderProps } from 'naive-ui'
let filename = ref("Click here to choose an image to upload!")
let show = ref(false)
let uploaded = false
let showModal = ref(false)
let imageUrl = ref("")
const message = useMessage()
const placementRef = ref<MessageProviderProps['placement']>('bottom')

interface HTM extends HTMLElement{
  file?:File[]
}
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
</script>

<template>
  <div class="zw-hci2-main-title">
    <div class="zw-hci2-main-title-c">
      Image Search
    </div>
    <br/><br/><br/>
    <n-spin :show="show">
      <input id="get_file" type="file" class="" style="display:none;visibility:hidden;" 
      placeholder="You can drag the image or paste the URL here!"
      v-on:change="onFileChange"/>
      <label for="get_file" class="zw-hci2-main-search-box" style="color:#ccc">{{filename}}</label>
      <template #description>
        Uploading the image. Please wait.
      </template>
    </n-spin>
    
    <br/><br/><br/>
    <div>
      <n-button color="#ffffff" size="large" class="zw-hci2-main-search-btn" v-on:click="submit">
        <template #icon>
          <n-icon>
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32"><path d="M29 27.586l-7.552-7.552a11.018 11.018 0 1 0-1.414 1.414L27.586 29zM4 13a9 9 0 1 1 9 9a9.01 9.01 0 0 1-9-9z" fill="currentColor"></path></svg>
          </n-icon>
        </template>
        &nbsp;
        Search Now
      </n-button>
      <span class="zw-hci2-spacer">


      </span>
      <n-button color="#ffffff" ghost size="large" class="zw-hci2-main-search-btn-c" @click="showModal=true;">
        <template #icon>
          <n-icon>
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512"><path d="M440.9 136.3a4 4 0 0 0 0-6.91L288.16 40.65a64.14 64.14 0 0 0-64.33 0L71.12 129.39a4 4 0 0 0 0 6.91L254 243.88a4 4 0 0 0 4.06 0z" fill="currentColor"></path><path d="M54 163.51a4 4 0 0 0-6 3.49v173.89a48 48 0 0 0 23.84 41.39L234 479.51a4 4 0 0 0 6-3.46V274.3a4 4 0 0 0-2-3.46z" fill="currentColor"></path><path d="M272 275v201a4 4 0 0 0 6 3.46l162.15-97.23A48 48 0 0 0 464 340.89V167a4 4 0 0 0-6-3.45l-184 108a4 4 0 0 0-2 3.45z" fill="currentColor"></path></svg>
          </n-icon>
        </template>
        &nbsp;
        View Image
      </n-button>
      
    </div>
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

  </div>
</template>

<style scoped lang="scss">
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
</style>
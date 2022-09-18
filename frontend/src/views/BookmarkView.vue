<script setup lang="ts">
import { defineComponent,ref,reactive } from 'vue'
import { useRoute } from 'vue-router'
import Router from '../router/index'
import Backend from '../apis/backend'
import { useMessage } from 'naive-ui'
interface ResultList{
  image:string,
  labels:string,
  title:string,
  description:string,
  coef:number,
  fav:number
}
const message = useMessage()
let save_path = ref("");
let intern_path = ref("");
let search_label = ref("");
let showModal = ref(false);
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

Backend.apiGetFavorite({}).then((response:any)=>{
    resultList.value = <ResultList[]><unknown>JSON.parse(<string>response.data)
})

function submitRefine(){
  let x = {
    'label':search_label.value
  }
  Backend.apiGetFavorite(x).then((response:any)=>{
    resultList.value = <ResultList[]><unknown>JSON.parse(<string>response.data)
  })
}
function clearBookmark(){
  let x={}
  Backend.apiClearFavorite(x).then((response:any)=>{
    Backend.apiGetFavorite(x).then((response:any)=>{
      resultList.value = <ResultList[]><unknown>JSON.parse(<string>response.data)
      message.success(
        "Bookmark removed.",
        { duration: 5000 }
      )
    })
  })
}
function backHome(){
  Router.push({name:'home',params:{}})
}
function showDetail(i:number){
  detailedItem.value = resultList.value[i-1]
  showModal.value = true
}
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
</script>

<template>
  <div class="zw-hci2-main-title">
      <div class="zw-hci2-fvkgrid">
          <div class="zw-hci2-fvkgrid-left zw-hci2-fvkgrid-left-media">
              <div class="zw-hci2-user-panel zw-hci2-panel">
                <!--Title-->
                <div>
                  <n-icon size="25" class="zw-hci2-icon-modifier">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" style=""><path d="M487.4 315.7l-42.6-24.6c4.3-23.2 4.3-47 0-70.2l42.6-24.6c4.9-2.8 7.1-8.6 5.5-14c-11.1-35.6-30-67.8-54.7-94.6c-3.8-4.1-10-5.1-14.8-2.3L380.8 110c-17.9-15.4-38.5-27.3-60.8-35.1V25.8c0-5.6-3.9-10.5-9.4-11.7c-36.7-8.2-74.3-7.8-109.2 0c-5.5 1.2-9.4 6.1-9.4 11.7V75c-22.2 7.9-42.8 19.8-60.8 35.1L88.7 85.5c-4.9-2.8-11-1.9-14.8 2.3c-24.7 26.7-43.6 58.9-54.7 94.6c-1.7 5.4.6 11.2 5.5 14L67.3 221c-4.3 23.2-4.3 47 0 70.2l-42.6 24.6c-4.9 2.8-7.1 8.6-5.5 14c11.1 35.6 30 67.8 54.7 94.6c3.8 4.1 10 5.1 14.8 2.3l42.6-24.6c17.9 15.4 38.5 27.3 60.8 35.1v49.2c0 5.6 3.9 10.5 9.4 11.7c36.7 8.2 74.3 7.8 109.2 0c5.5-1.2 9.4-6.1 9.4-11.7v-49.2c22.2-7.9 42.8-19.8 60.8-35.1l42.6 24.6c4.9 2.8 11 1.9 14.8-2.3c24.7-26.7 43.6-58.9 54.7-94.6c1.5-5.5-.7-11.3-5.6-14.1zM256 336c-44.1 0-80-35.9-80-80s35.9-80 80-80s80 35.9 80 80s-35.9 80-80 80z" fill="currentColor"></path></svg>
                </n-icon>
                  <b class="zw-hci2-user-panel-title">Manage Bookmark</b>
                </div>
                <!--Image-->
                <p>No longer like these favorited pictures? You can</p>
                <n-tooltip trigger="hover" placement="bottom">
                  <template #trigger>
                    <n-button color="#ffffff" type="info" size="large" class="zw-hci2-main-search-btn" style="width:100%" @click="clearBookmark">
                      <template #icon >
                        <n-icon size="20">
                          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 448 512"><path d="M432 32H312l-9.4-18.7A24 24 0 0 0 281.1 0H166.8a23.72 23.72 0 0 0-21.4 13.3L136 32H16A16 16 0 0 0 0 48v32a16 16 0 0 0 16 16h416a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16zM53.2 467a48 48 0 0 0 47.9 45h245.8a48 48 0 0 0 47.9-45L416 128H32z" fill="currentColor"></path></svg>
                        </n-icon>
                      </template>
                      Reset Bookmarks
                    </n-button>
                  </template>
                  Remove all of your bookmarks. This operation cannot be undone.
                </n-tooltip>
                <br/><br/>
                <!--Refinement-->
                <br/>
                <div>
                  <n-icon size="25" class="zw-hci2-icon-modifier">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 20 20"><g fill="none"><path d="M9.104 2.9a1 1 0 0 1 1.794 0l1.93 3.91l4.317.628a1 1 0 0 1 .554 1.706l-3.124 3.044l.738 4.3a1 1 0 0 1-1.451 1.054l-3.86-2.03l-3.862 2.03a1 1 0 0 1-1.45-1.055l.737-4.299l-3.124-3.044a1 1 0 0 1 .554-1.706l4.317-.627l1.93-3.912zM4.39 12.687a.5.5 0 0 1-.078.703l-2.5 2a.5.5 0 1 1-.624-.781l2.5-2a.5.5 0 0 1 .702.078zM4.312 5.11a.5.5 0 1 1-.624.78l-2.5-2a.5.5 0 1 1 .624-.78l2.5 2zm11.297 7.578a.5.5 0 0 0 .079.703l2.5 2a.5.5 0 1 0 .624-.781l-2.5-2a.5.5 0 0 0-.703.078zm.079-7.578a.5.5 0 0 0 .624.78l2.5-2a.5.5 0 1 0-.624-.78l-2.5 2z" fill="currentColor"></path></g></svg>
                  </n-icon>
                  <b class="zw-hci2-user-panel-title">Result Refinement</b>
                </div>
                <p>Not satisfied with the result? You can try these options below!</p>
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
                      Initiate Image Query
                    </n-button>
                  </template>
                  Go back to Home and initiate a new visual query
                </n-tooltip>
              </div>
          </div>
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
                          There's currently no customized bookmarks. You can explore and bookmark your favorite pictures by 'Initiate Image Query'
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
      </div>
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
  </div>
</template>



<style lang="scss" scoped>
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
</style>
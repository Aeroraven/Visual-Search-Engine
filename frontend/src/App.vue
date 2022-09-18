<script setup lang="ts">
import {ref} from 'vue'
import Router from './router/index'
const active = ref(false);
const placement = ref("right");
const active2 = ref(false);
const placement2 = ref("right");
const activate = (place:any) => {
  active.value = true;
  placement.value = place;
};
const activate2 = (place:any) => {
  active2.value = true;
  placement2.value = place;
};
function goHome(){
  Router.push({name:'home'})
}
function goBookmark(){
  Router.push({name:'bookmark'})
}
</script>

<template>
  <div class="zw-hci2-main-wrapper">
    <n-message-provider>
      <div class="zw-hci2-top-bar">
        <span class="zw-hci2-top-bar-title">
          <span class="zw-hci2-naive-icon-modifier">
            <n-icon size="28">
              <svg style="color:#0099FF" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512">
                <path d="M335.45 256a214.83 214.83 0 0 1 29.08-108l7.62-13.26a280.69 280.69 0 0 0-48.64-7.15c-21.94-16.9-54.64-36.95-92.34-43.33L208 80l13.37 61.86c-41.67 14.14-78.43 42.86-102.76 62.62q-7.06-5.91-14.78-11.55c-39.71-29-82.6-31.8-84.4-31.9L0 160l2.67 19.31c.29 2 6.79 44.73 31.65 76.52C9.46 287.63 3 330.33 2.67 332.36L0 352l19.43-1.36c1.8-.1 44.69-2.89 84.4-31.9q7.58-5.53 14.56-11.37c24.37 19.83 61.14 48.6 102.86 62.74L208 432l23.17-4.22c37.49-6.34 70.08-26.4 92-43.32a284.27 284.27 0 0 0 49.32-7.23l-7.91-13.18A214.92 214.92 0 0 1 335.45 256z" fill="currentColor"></path><path d="M499.59 221.75c-5.85-9.88-16.54-24.9-34.19-40.28a209.82 209.82 0 0 0-62-37L392.23 164a183.22 183.22 0 0 0-.09 183.87l11.75 19.57a209.26 209.26 0 0 0 61.42-36.49C497.05 303.47 512 269 512 256c0-12.31-8-26.74-12.41-34.25zM416 256a16 16 0 1 1 16-16a16 16 0 0 1-16 16z" fill="currentColor"></path>
              </svg>
            </n-icon>
          </span>
          <n-gradient-text type="info">
            <span class="zw-hci2-top-bar-title-override">
              HCI Lab 2
            </span>
          </n-gradient-text>
        </span>
        <n-divider vertical class="zw-hci2-vdivider"/> Visual Search
        
        <div class="zw-hci2-right-topbar">
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button quaternary circle type="info" size="large" @click="goHome">
                <template #icon >
                  <n-icon size="20">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" style="color:#444;"><path d="M946.5 505L534.6 93.4a31.93 31.93 0 0 0-45.2 0L77.5 505c-12 12-18.8 28.3-18.8 45.3c0 35.3 28.7 64 64 64h43.4V908c0 17.7 14.3 32 32 32H448V716h112v224h265.9c17.7 0 32-14.3 32-32V614.3h43.4c17 0 33.3-6.7 45.3-18.8c24.9-25 24.9-65.5-.1-90.5z" fill="currentColor"></path></svg>
                  </n-icon>
                </template>
              </n-button>
            </template>
            Home
          </n-tooltip>
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button quaternary circle type="info" size="large" @click="goBookmark">
                <template #icon >
                  <n-icon size="20">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 576 512" style="color:#444;"><path d="M259.3 17.8L194 150.2L47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103l-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5l105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2L316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z" fill="currentColor"></path></svg>
                  </n-icon>
                </template>
              </n-button>
            </template>
            Bookmark
          </n-tooltip>
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button quaternary circle type="info" size="large" @click="activate('bottom')">
                <template #icon >
                  <n-icon size="20">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" style="color:#444;"><path d="M504 256c0 136.997-111.043 248-248 248S8 392.997 8 256C8 119.083 119.043 8 256 8s248 111.083 248 248zM262.655 90c-54.497 0-89.255 22.957-116.549 63.758c-3.536 5.286-2.353 12.415 2.715 16.258l34.699 26.31c5.205 3.947 12.621 3.008 16.665-2.122c17.864-22.658 30.113-35.797 57.303-35.797c20.429 0 45.698 13.148 45.698 32.958c0 14.976-12.363 22.667-32.534 33.976C247.128 238.528 216 254.941 216 296v4c0 6.627 5.373 12 12 12h56c6.627 0 12-5.373 12-12v-1.333c0-28.462 83.186-29.647 83.186-106.667c0-58.002-60.165-102-116.531-102zM256 338c-25.365 0-46 20.635-46 46c0 25.364 20.635 46 46 46s46-20.636 46-46c0-25.365-20.635-46-46-46z" fill="currentColor"></path></svg>
                  </n-icon>
                </template>
              </n-button>
            </template>
            Help
          </n-tooltip>
          
        </div>
      </div>
      <router-view v-slot="{ Component }">
        <transition name="slide-fade">
          <component :is="Component" />
        </transition>
      </router-view>

      <n-drawer v-model:show="active" :width="502" :placement="placement">
        <n-drawer-content title="Help for Visual Search">
          <b>About the Model</b>: The image retrieval system uses deep learning model as its evaluation method. The model we used is ResNet-34 pretrained on ImageNet. The output of convoluton layers are used as the image feature.
          <br/>
          <b>About the Results</b>: Results are sorted in the order of relevance. The image more similar to your uploaded picture will be shown in higher priority. Search results only contain image form the preset dataset. Image tags are automatically generated by ResNet-34 model, and not guaranteed to be completely correct.
          <br/>
          <b>Acknowledgements:</b> This project is intended for the course HCI,Spring 2022. It's based on many open-source projects. For detailed references and acknowledgements, please <a href="javascript:void(0)" @click="activate2('bottom')">Click Here</a>
        </n-drawer-content>
        <n-drawer v-model:show="active2" :width="251" :placement="placement2">
          <n-drawer-content title="Acknowledgements">
            <b>Author</b>: 1950641 <br/>
            <b>Language:</b> Backend:Python, Frontend:TypeScript(Vue3)+CSS(Sass).<br/>
            <b>Development Environments</b>:<br/>
            <li>Vue 3 (Vuejs.org,MIT License,https://github.com/vuejs/core)</li>
            <li>Vite (Vuejs.org,MIT License,https://github.com/vitejs/vite)</li>
            <li>Flask (Pallets,BSD-3 License,https://github.com/pallets/flask)</li>
            <li>PyTorch (https://github.com/pytorch/pytorch)</li>
            <b>Other Dependencies</b>:<br/>
            <li>NaiveUI (TuSimple,MIT License,https://github.com/TuSimple/naive-ui)</li>
            <li>XIcon (07akioni,https://github.com/07akioni/xicons)</li>
            <li>Axios (Axios,MIT License,https://github.com/axios/axios)</li>
            <li>ResNet34 (https://arxiv.org/abs/1512.03385,Implemented by PyTorch Vision)</li>
            <b>Archived Images</b>:<br/>
            <li>All images are downloaded form Bing Image.</li>
          </n-drawer-content>
        </n-drawer>
      </n-drawer>
      
    </n-message-provider>
    
  </div>  
</template>

<style lang="scss" scoped>
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
</style>

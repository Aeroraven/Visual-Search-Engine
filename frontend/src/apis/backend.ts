import request from "../utils/request";

export default class {
  static apiFindSimilarImages(data:FormData) {
    return request({
      url: "/api/findSimilarImages",
      method: "post",
      data:data,
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
  }
  static apiFindSimilarImagesRefined(data:any) {
    return request({
      url: "/api/findSimilarImagesRefined",
      method: "post",
      data:data,
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
  }
  static apiAddFavorite(data:any){
    return request({
      url: "/api/addBookmark",
      method: "post",
      data:data,
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
  }
  static apiRemoveFavorite(data:any){
    return request({
      url: "/api/removeBookmark",
      method: "post",
      data:data,
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
  }
  static apiGetFavorite(data:any){
    return request({
      url: "/api/getBookmarkList",
      method: "post",
      data:data,
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
  }
  static apiClearFavorite(data:any){
    return request({
      url: "/api/clearBookmark",
      method: "post",
      data:data,
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
  }
}
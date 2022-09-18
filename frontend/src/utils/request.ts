import axios, { type AxiosRequestConfig } from "axios";
// create an axios instance
const service = axios.create({
  baseURL: "http://localhost:5000/",
  withCredentials:true,
  timeout: 20000,
});
// request interceptor
service.interceptors.request.use(
  (config:AxiosRequestConfig<any>)  => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
// response interceptor
service.interceptors.response.use(
  (response) => {
    const res = response.data;
    return res
  },
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.setItem("token", "");
        window.location.href = "/";
      }
      if (error.response.status === 500) {
        return Promise.reject(
          new Error("输入的数据存在非法部分，请重新检查输入后再进行重试。")
        );
      }
      if (error.response.status === 400) {
        return Promise.reject(
          new Error("输入的数据存在非法部分，请重新检查输入后再进行重试。")
        );
      }
      if (error.response.status === 403) {
        return Promise.reject(new Error("您暂无权限查看当前页面。"));
      }
      if (error.response.status === 404) {
        return Promise.reject(
          new Error("您所访问的服务当前正在维护，或已经迁移。")
        );
      }
    }

    return Promise.reject(error);
  }
);
export default service;
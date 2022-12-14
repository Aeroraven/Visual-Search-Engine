import BookmarkViewVue from "@/views/BookmarkView.vue";
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SearchPage from "../views/SearchPage.vue"
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/search",
      name: "search",
      component: SearchPage,
    },
    {
      path: "/bookmark",
      name: "bookmark",
      component: BookmarkViewVue,
    },
  ],
});

export default router;

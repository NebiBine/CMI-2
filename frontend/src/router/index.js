import { createRouter, createWebHistory } from 'vue-router'
//LAYOUTS
import WelcomeLayout from '../layouts/WelcomeLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'
import MainLayout from '../layouts/MainLayout.vue'
//VIEWS
import WelcomePage from '../views/WelcomePageView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotYourPasswordView from '../views/ForgotYourPasswordView.vue'
//import HomeView from '../views/HomeView.vue'
//import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path:'/',
    component: WelcomeLayout,
    children: [
      {path:'',component: WelcomePage}
    ]
  },
  {
    path:'/auth',
    component: AuthLayout,
    children: [
      {path:'login',component: LoginView},
      {path:'register',component: RegisterView},
      {path:'ForgotPassword',component: ForgotYourPasswordView},
    ]
  }


    //USTVARJANJE NOVIH ROUTOU PRINCIP - zacasno
  //{ path: '/', name: 'Home', component: HomeView },
  //{ path: '/about', name: 'About', component: AboutView },
]




//router create
const router = createRouter({
  history: createWebHistory(),
  routes,
})
//export
export default router
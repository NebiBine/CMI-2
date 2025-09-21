import { createRouter, createWebHistory } from 'vue-router'
//LAYOUTS
import WelcomeLayout from '../layouts/WelcomeLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'
import MainLayout from '../layouts/MainLayout.vue'
//VIEWS
  //welcome page
import WelcomePage from '../views/WelcomePageView.vue'
  //login and register and profile creation and forgot your password
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotYourPasswordView from '../views/ForgotYourPasswordView.vue'
import ChangePasswordView from '../views/ChangePasswordView.vue'
import ProfileCreationView from '../views/ProfileCreationView.vue'
  //main page dashboard etc.
import DashboardView from '../views/DashboardView.vue'
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
      {path:'ProfileCreation',component: ProfileCreationView},
      {path:'ForgotPassword',component: ForgotYourPasswordView},
      {
        path: "/auth/PasswordReset/:token",
        name: "ResetPassword",// ne rabim za zacetek bo samo olajsava ce bom kaj uporabljal se ta subpage
        component: (ChangePasswordView),
        props: true
      },
      ]
  },
  {
    path:'/app',
    component: MainLayout,
    children: [
      {path:'Dashboard',component: DashboardView}
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
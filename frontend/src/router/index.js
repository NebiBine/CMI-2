import { createRouter, createWebHistory } from 'vue-router';
import axios from "axios";
//LAYOUTS
import WelcomeLayout from '../layouts/WelcomeLayout.vue';
import AuthLayout from '../layouts/AuthLayout.vue';
import MainLayout from '../layouts/MainLayout.vue';
//VIEWS
  //welcome page
import WelcomePage from '../views/WelcomePageView.vue';
  //login and register and profile creation and forgot your password
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ForgotYourPasswordView from '../views/ForgotYourPasswordView.vue';
import ChangePasswordView from '../views/ChangePasswordView.vue';
import ProfileCreationView from '../views/ProfileCreationView.vue';
  //main page dashboard etc.
import DashboardView from '../views/DashboardView.vue';
import PollsAndInsightsView from '../views/PollsAndInsightsView.vue';

//admin
import AdminPanelView from '../views/AdminPanelView.vue';
import AdminDashboard from '../views/AdminDashboardView.vue';
import AdminUserManagementView from '../views/AdminUserManagementView.vue';
import PollManagementView from '../views/PollManagementView.vue';
//import HomeView from '../views/HomeView.vue'
//import AboutView from '../views/AboutView.vue'


import AccountView from '../views/AccountView.vue';
import SettingsView from '../views/SettingsView.vue';
import OurMissionView from '../views/OurMissionView.vue';
import AboutUsView from '../views/AboutUsView.vue';
import FAQView from '../views/FAQView.vue';
import OurStoryView from '../views/OurStoryView.vue';

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
      {path:'ProfileCreation',component: ProfileCreationView, meta: { requiresAuth: false }},
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
      {path:'Dashboard',name:'dashboard',component: DashboardView, meta: { requiresAuth: true }},
      {path:'PollsAndInsights',name:'polls',component: PollsAndInsightsView, meta: { requiresAuth: true }},
    ]
  },
  {
    path:'/admin',
    component: MainLayout,
    children: [
      {path:'AdminPanel',component: AdminPanelView, name:'adminPanel', meta: { requiresAuth: true }},
      {path:'AdminDashboard',component: AdminDashboard, name:'adminDashboard', meta: { requiresAuth: true }},
      {path:'UserManagement',component: AdminUserManagementView, name:'userManagement', meta: { requiresAuth: true }},
      {path:'PollManagement',component: PollManagementView, name:'pollManagement', meta: { requiresAuth: true }}
    ]
  },
  {
    path:'/other',
    component: MainLayout,
    children: [
      {path:'account',component: AccountView, name:'account', meta: { requiresAuth: true }},
      {path:'settings',component: SettingsView, name:'settings', meta: { requiresAuth: true }},
      {path:'ourMission',component: OurMissionView, name:'aboutMission', meta: { requiresAuth: true }},
      {path:'aboutUs',component: AboutUsView, name:'aboutUs', meta: { requiresAuth: true }},
      {path:'ourStory',component: OurStoryView, name:'aboutStory', meta: { requiresAuth: true }},
      {path:'faq',component: FAQView, name:'faq', meta: { requiresAuth: true }}
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
//requires auth

//to - kam hocem it recimo /app/dashboard
//from - iz kje prihajam recimo /auth/login
//next - funkcija ki jo moram klicat da vue routerju povem kaj naj naredi (continue,redirect, cancel)
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) { //ce to ima meta requiresauth potem preveri ce ne samo dovoli da gre dalje 
    try {
      const res = await axios.get("http://localhost:8000/auth/check", { //getam iz backenda
        withCredentials: true, // pove da zahtevam cookije
      });
      //DODAJ DA CE SI ZE LOGINAN GRES DIREKTNO IZ LOGINA NA DASHBOARD -- REDIRECT--------------------------------------------------------------------
      if (res.data.loggedIn) {
        next(); // ce je logged in true dovolim userju da gre naprej na /app/dashboard recimo
        console.log(res.data.loggedIn)
      } else {
        next("/auth/login"); 
      }
    } catch (err) {
      next("/auth/login"); //ce je error sklepam da user ni loggan in in ga pustim na loginu
    }
  } else {
    next();
  }
});


//export
export default router
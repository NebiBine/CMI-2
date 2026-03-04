<script setup>
import { onMounted, ref,h } from "vue"
import "../assets/styles/mainStyle.css"
import { useRouter } from "vue-router"
import axios from "axios";
import logoutIcon from '../assets/icons/logout_icon.png';

const router = useRouter();
const activeKey = ref("dashboard")
const admin = ref(false)
const username = ref("");
const userProfilePicture = ref("");
const profileOptions = ref([
  {
    label:'Profile',
    key:'profile',
  },
  {
    label:'Logout',
    key:'logout',
    icon: () => h('img', { 
      src: logoutIcon, 
      style: 'width: 16px; height: 16px;'
    })
  }
])

function handleUserOptions(key){
  if(key === "profile"){
    router.push('/other/account')
  }
}
const menuOptions = ref([
  {
    label: "Dashboard",
    key: "dashboard",
//    children: [
//      {
//        label: 'Test'
//      }
//    ]
  },
  {
    label: "Social",
    key: "social",
  },
  {
    label: "Traffic Updates",
    key: "trafficUpdates",
    children: [
      {
        label:'General',
        key:'trafficGeneral',
        disabled:true,
      },
      {
        label:'Jams',
        key:'trafficJams',
        disabled:true,
      },
      {
        label:'Accidents',
        key:'trafficAccidents',
        disabled:true,
      },
      {
        label:'Works',
        key:'trafficWorks',
        disabled:true,
      },
      {
        label:'Blocks',
        key:'trafficBlocks',
        disabled:true,
      }

    ]
  },
  {
    label: "Polls & Insights",
    key: "polls",
  },
  {
    label: "Weather",
    key: "weather",
  },
  {
    label: "Public Transit",
    key: "publicTransit",
    disabled:true,
  },
  {
    label: "City Guides",
    key: "cityGuides",
    children:[
      {
        label:'Reviews',
        key:'cityReviews',
        disabled:true
      },
      {
        label:'Points of Interest',
        key:'cityPointsOfInterest',
        disabled:true
      },
      {
        label:'Local Goods',
        key:'cityLocalGoods'
      }
    ]
  },
  {
    label: "Energy Info",
    key: "energyInfo",
    disabled:true
  },
  {
    label:"Rewards",
    key:"rewards"
  },
  {
    type: "divider",
    key: "divider-1",
  },
  {
    label: "Settings",
    disabled:true,
    key: "settings",
  },
  {
    label:'About Us',
    key:'aboutUs',
    children: [
      {
        label:'Our Mission',
        key:'aboutMission'
      },
      {
        label:'Our Story',
        key:'aboutStory'
      },
      {
        label:'FAQ',
        key:'faq'
      }
    ]
  },
  {
    label:'Account',
    key:'account'
  }

])
async function admincheck() {
  try{
    const response = await axios.get(
      "http://localhost:8000/auth/checkAdmin",
      {withCredentials:true}
    )
    admin.value = response.data.admin
    console.log("IS CURRENT USER ADMIN",admin.value)
    if(admin.value === true){
      menuOptions.value.push(
        {
          label:'Admin Panel',
          key:'adminPanel',
          children: [
            {
              label:'Admin Dashboard',
              key:'adminDashboard'
            },
            {
              label:'User Management',
              key:'userManagement'
            },
            {
              label:'Poll Management',
              key:'pollManagement'
            },
            {
              label:'Reward Management',
              key:'rewardManagement'
            }
      //      {
        //      label:'Data Management',
          //    key:'dataManagement'
            //}

          ]
        }
      )
    }
  }
  catch(error){
    console.log("Admin check error: " + error)
  }
}

async function getProfileData(){
  try{
    const response = await axios.post(
      'http://localhost:8000/profile/getProfile',
      {
        userId: "null",
        type: 1
      },
      { withCredentials: true }
    );
    if(response.data.statusCode == 200){
      userProfilePicture.value = response.data.pfp;
      username.value = response.data.username;
    }
    else{
      userProfilePicture.value = "database/data/pfp/default_profile_pic.png";
    }


  }
  catch (error) {
    console.log('Error while fetching profile data');
    console.log(error);
  }
}
onMounted(()=>{
  admincheck()
  getProfileData()
})
</script>

<template>
  <n-message-provider class="app-message-provider">
  <n-layout class="app-layout">
    <!-- HEADER -->
    <n-layout-header class="header" bordered>
      <div class ="logo">
        <img src="../assets/images/logotip_cmi.png" width="140px" height="140px">
    </div>
    <div class = "userInfo">
      <!--tukaj pride username itd.-->
      <img :src="userProfilePicture" alt="Profile Picture">
      <n-dropdown :options="profileOptions" @select="handleUserOptions" class="profile_dropdown">
        <n-button>{{username}}</n-button>
      </n-dropdown>
    </div>
    </n-layout-header>

    <!-- MAIN (SIDEBAR + CONTENT) -->
    <n-layout has-sider class="main-layout">
      <!-- SIDEBAR -->
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="220"
        show-trigger="bar"
        class="sidebar"
      >
        <n-menu v-model:value="activeKey" :options="menuOptions" @update:value="key => router.push({ name: key })"/>
      </n-layout-sider>

      <!-- CONTENT -->
      <n-layout-content class="content">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
  </n-message-provider>
</template>

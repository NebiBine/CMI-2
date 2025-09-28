<script setup>
import { ref } from "vue"
import "../assets/styles/mainStyle.css"
import { useRouter } from "vue-router"


const router = useRouter();
const activeKey = ref("dashboard")

const menuOptions = [
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
        key:'trafficGeneral'
      },
      {
        label:'Jams',
        key:'trafficJams'
      },
      {
        label:'Accidents',
        key:'trafficAccidents'
      },
      {
        label:'Works',
        key:'trafficWorks'
      },
      {
        label:'Blocks',
        key:'trafficBlocks'
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
  },
  {
    label: "City Guides",
    key: "cityGuides",
    children:[
      {
        label:'Reviews',
        key:'cityReviews'
      },
      {
        label:'Points of Interest',
        key:'cityPointsOfInterest'
      }
    ]
  },
  {
    label: "Energy Info",
    key: "energyInfo",
  },
  {
    type: "divider",
    key: "divider-1",
  },
  {
    label: "Settings",
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
      }
    ]
  },
  {
    label:'Account',
    key:'account'
  }

]
</script>

<template>
  <n-layout class="app-layout">
    <!-- HEADER -->
    <n-layout-header class="header" bordered>
      <div class ="logo">
        <b>CMI - City Management Interface</b>
    </div>
    <div class = "test">
      <!--tukaj pride username itd.-->
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
        <n-menu v-model:value="activeKey" :options="menuOptions" />
      </n-layout-sider>

      <!-- CONTENT -->
      <n-layout-content class="content">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

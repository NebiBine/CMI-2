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
  },
  {
    label: "Blank",
    key: "blank",
  },
  {
    type: "divider",
    key: "divider-1"
  },
  {
    label: "Settings",
    key: "settings",
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

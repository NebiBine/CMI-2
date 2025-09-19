
<script setup>
import '../assets/styles/AUTHStyle.css'
</script>
<template>
    <div class="welcome-layout">
      <main>
        <n-message-provider>
            <router-view />
        </n-message-provider>
      </main>
    </div>
  </template>
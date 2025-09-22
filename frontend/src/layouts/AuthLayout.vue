<script setup>
import '../assets/styles/AUTHStyle.css'


</script>

<template>
  <n-config-provider :theme="null">
  <n-message-provider>
  <div class="auth-layout">
    <!-- Leva stran (formi) -->
    <div class="auth-left">
      <main>
        <router-view />
      </main>
    </div>

    <!-- Desna Stran (slika) -->
    <div class="auth-right">
      <img src="../assets/images/login_photo.jpg" alt="City illustration" />
    </div>
  </div>
</n-message-provider>
</n-config-provider>
</template>

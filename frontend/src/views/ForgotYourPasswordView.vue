<script setup>
import '../assets/styles/AUTHStyle.css'
import { ref } from "vue"

const formValue = ref({
  ResetEmail: "",
})
</script>

<template>
  <div class="forgot-page">
    <!-- Left side (form) -->
    <div class="forgot-left">
      <div class="forgot-container">
        <h1>Forgot Password</h1>
        <p class="subtitle">
          Enter your email and we’ll send you a link to reset your password.
        </p>

        <n-input v-model:value="formValue.ResetEmail" placeholder="Email" />
        <n-button>Send Reset Link</n-button>

        <div class="forgot-footer">
          <router-link to="/auth/login">← Back to Login</router-link>
        </div>
      </div>
    </div>

    <!-- Right side (illustration) -->
    <div class="forgot-right">
      <img src="../assets/images/login_photo.jpg" alt="Forgot password illustration" />
    </div>
  </div>
</template>

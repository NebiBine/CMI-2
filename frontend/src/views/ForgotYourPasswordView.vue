<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import '../assets/styles/AUTHStyle.css'

const formValue = ref({
  email: "",
})

const router = useRouter()

const sendResetLink = () => {
  console.log("📩 Reset link sent to:", formValue.value.email)
  // axios call here if needed
}
</script>

<template>
  <div class="auth-container">
    <h1>Forgot Password</h1>
    <p class="subtitle">Enter your email and we’ll send you a reset link.</p>

    <n-input v-model:value="formValue.email" placeholder="Email" />
    <n-button @click="sendResetLink">Send Reset Link</n-button>

    <div class="auth-footer">
      <router-link to="/auth/login">← Back to Login</router-link>
    </div>
  </div>
</template>

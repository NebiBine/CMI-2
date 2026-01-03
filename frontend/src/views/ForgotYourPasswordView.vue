<script setup>
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import { v4 as uuidv4 } from "uuid"
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { message } from "ant-design-vue";

const router = useRouter();
const formRef = ref(null);
const size = ref("medium");


const formValue = ref({
  user: {
    email: "",
  },
});

const rules = {
  user: {
    email: {
      required: true,
      message: "Please input your email",
      trigger: "blur"
    }
  },
};

// axios 
const forgotPassword = async () => {
  try {
    const response = await axios.post("http://localhost:8000/auth/forgotPassword", {
      email: formValue.value.user.email
    },{
      withCredentials: true
    })
    console.log("✅ Success:", response.data);
    if(response.data.statusCode === 200){
      message.success(response.data.message);
    }
    else{
      message.error(response.data.message);
    }
  } catch (error) {
    console.error("❌ Error:", error);
    message.error(error.response.data.message);
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-left">
      <div class="login-container">
        <h1>Forgot your password</h1>
        <p class="subtitle">Enter your email and we’ll send you a reset link.</p>
        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.email">
            <n-input v-model:value="formValue.user.email" placeholder="Email" />
          </n-form-item>

          <n-button type="primary" @click="forgotPassword">Send reset link</n-button>
        </n-form>

        <div class="login-footer">
          <p><i>Make sure to check <b>spam inbox</b> aswell!</i></p>
          <p><RouterLink to="/auth/login" class="povezave">← Back to Login</RouterLink></p>
        </div>
      </div>
    </div>

  </div>
</template>
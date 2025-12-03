<script setup>
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css';
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { message } from 'ant-design-vue';

const router = useRouter();
const formRef = ref(null);
const size = ref("medium");

const rememberState = ref(false);

const formValue = ref({
  user: {
    username: "",
    password: ""
  },
});

const rules = {
  user: {
    username: {
      required: true,
      message: "Please input your username",
      trigger: "blur"
    },
    password: {
      required: true,
      message: "Please input your password",
      trigger: "blur"
    }
  },
};

// axios login
const login = async () => {
  try {
    const response = await axios.post("http://localhost:8080/auth/login", {
      identifier: formValue.value.user.username,
      password: formValue.value.user.password,
      remember: rememberState.value
    },
    {withCredentials: true})
    console.log("✅ CMI Login success:", response.data)

    if (response.data.success === true) {
      router.push("/app/Dashboard");
      
      message.success(response.data.message);
    } else {
      message.error(response.data.message);
    }
  } catch (error) {
    console.error("❌ CMI Login error:", error);
    message.error(error.response.data.message);
  }
};
function remember(checked){
  rememberState.value = checked;
  console.log("Remember me stanje:", rememberState.value);
}
//dodaj da ce user ze ima cookije da direktno pusham na dashboard router.push("/app/Dashboard");

const [messageApi, contextHolder] = message.useMessage();
const wrongUsername = () => {
  messageApi.info('Username does not exist!');
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-left">
      <h1>Welcome Back to CMI!</h1>
      <div class="login-container">
        
        <p class="subtitle">Log in to manage your city services and stay updated.</p>

        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.username">
            <n-input v-model:value="formValue.user.username" placeholder="Username" />
          </n-form-item>

          <n-form-item path="user.password">
            <n-input type="password" v-model:value="formValue.user.password" placeholder="Password" />
          </n-form-item>

          <n-space item-style="display: flex;" align="center">
            <n-checkbox color="#4cc9f0" @update:checked="remember" >Remember me</n-checkbox>
          </n-space>

          <n-button type="primary" class="log-reg_btn" @click="login">Log In</n-button>
        </n-form>

        <div class="login-footer">
          <p>
            Don’t have an account?
            <RouterLink to="/auth/register" class = "povezave">Register here</RouterLink>
          </p>
          <p><RouterLink to="/auth/ForgotPassword" class = "povezave">Forgot your password?</RouterLink></p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
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
      message: "Please input your username or email!",
      trigger: "blur"
    },
    password: {
      required: true,
      message: "Please input your password!",
      trigger: "blur"
    }
  },
};

//FUNKCIJA DA PREVERIM CE JE LOGGED IN TRUE IN CE JE POTEM GA DAM NA DASHBOARD, CE NE JE PA NA LOGIN
async function checkSession() {
  try {
    const response = await axios.get("http://localhost:8000/auth/check", {
      withCredentials: true
    });
    if (response.data.loggedIn==true) {
      router.push("/app/Dashboard");
      message.success("Welcome back!",3);
    }
  } catch (error) {
    console.error("❌ CMI Session check error:", error);
  }
};



function remember(checked){
  rememberState.value = checked;
  console.log("Remember me stanje:", rememberState.value);
}

// axios login
async function login() {
  try {
    const response = await axios.post("http://localhost:8000/auth/login", {
      identifier: formValue.value.user.username,
      password: formValue.value.user.password,
      remember: rememberState.value
    },
    {withCredentials: true})
    console.log("✅ CMI Login success:", response.data)

    if (response.data.statusCode === 200) {
      router.push("/app/Dashboard");
      message.success(response.data.message,3);
    }
  } catch (error) {
    console.error("❌ CMI Login error:", error);
    if (error.response.data.detail) {
        message.error(error.response.data.detail,3);
    } else if (error.response.data.message) {
        message.error(error.response.data.message,3);
    } else {
        message.error('Login failed. Please try again.',3);
    }
}
};

onMounted(() => {
  checkSession();
});
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
            <n-input v-model:value="formValue.user.username" placeholder="Email/Username" />
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

<script setup>
    import '../assets/styles/mainStyle.css'
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';
</script>
<template>
    <h1>Weather</h1>
    <p>Look through the weather forecast and keep an eye on the weather alerts if there are any!</p>
</template>
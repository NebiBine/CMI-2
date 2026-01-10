<script setup>
    import '../assets/styles/mainStyle.css'
    import { ref, onMounted } from 'vue';
    import axios from 'axios';

</script>
<template>
    <h1>Rewards</h1>
    <p>Look through the available rewards here and redeem them!</p>

    <div v-for="reward in rewards">
        <!--TODO: PRIKAZI REWARDE TUKAJ V TEM DIVU--> 
    </div>
</template>

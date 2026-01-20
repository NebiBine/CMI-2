<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userPoints = ref(0);
const rewardDrawer = ref(false);

async function getUserPoints(){
    try{
        const response = await axios.get("http://localhost:8000/poll-reward/getUserPoints",
        { withCredentials: true });
        userPoints.value = response.data;
    }
    catch(error){
        console.log(error)
    }
}

function claimedRewardsDrawerOpen(){
    rewardDrawer.value = true;
}


onMounted(() => {
    getUserPoints()
});
</script>
<template>
    <h1>Rewards</h1>
    <p>Look through the available rewards here and redeem them!</p>
    <p>Your current points: {{ userPoints }}</p>
    <n-button @click="claimedRewardsDrawerOpen">View your claimed rewards</n-button>
    <n-drawer v-model:show="rewardDrawer" placement="right" :width="400" closable>
        <n-drawer-content closable title="Your claimed rewards" id = "rwTest">
            <div v-if="rewards">
                <div v-for="reward in rewards">
                    <!--TODO: PRIKAZI REWARDE TUKAJ V TEM DIVU--> 
                </div>
            </div>
            <div v-else class = "empty-rewards">
                <img src = "../assets/icons/no-rewards.png">
                <p>You haven't claimed any rewards yet</p>
            </div>

        </n-drawer-content>
    </n-drawer>

</template>

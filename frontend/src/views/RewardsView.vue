<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { message } from 'ant-design-vue';

const userPoints = ref(0);
const rewardDrawer = ref(false);
const rewards = ref([]);
const claimedRewards = ref([]);

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
async function getAllAvailableRewards(){
    try{
        const response  = await axios.get('http://localhost:8000/poll-reward/getAllAvailableRewards',
        { withCredentials: true });
        rewards.value = response.data.avaliableRewards;
        claimedRewards.value = response.data.claimedRewards;
        console.log("Available rewards:", rewards.value);
    }
    catch(error){
        console.log(error)
    }
}

async function claimReward(reward){
    try{
        const response = await axios.post(`http://localhost:8000/poll-reward/claimReward`,
        {id: reward.id},
        { withCredentials: true });
        if(response.data.statusCode === 200){
            message.success(response.data.message);
        }
        else{
            message.error(response.data.message);
        }
        getUserPoints();
        getAllAvailableRewards();
    }
    catch(error){
        console.log(error)
    }
}

function claimedRewardsDrawerOpen(){
    rewardDrawer.value = true;
}


onMounted(() => {
    getUserPoints();
    getAllAvailableRewards();
});
</script>
<template>
    <h1>Rewards</h1>
    <p>Look through the available rewards here and redeem them!</p>
    <p>Your current points: {{ userPoints }}</p>

    <n-button @click="claimedRewardsDrawerOpen">View your claimed rewards</n-button>
    <div class = "polls-container">
        <div v-for="reward in rewards" :key="reward.id" class = "EnPoll"> 
            <h2>Reward Title: {{ reward.rewardTitle }}</h2>
            <p>Description: {{ reward.rewardDescription }}</p>
            <p>Points Required: {{ reward.pointsRequired }}</p>
            <p>Expires At: {{ new Date(reward.expirationDate).toLocaleDateString() }}</p>
            <n-button @click="claimReward(reward)">Claim Reward</n-button>
            <!--TODO: SISTEM ZA CLAIM REWARD BUTTON JE NASTAVLJEN FUNCKIJO SE DOPISI-->
        </div>
    </div>

    <n-drawer v-model:show="rewardDrawer" placement="right" :width="400" closable>
        <n-drawer-content closable title="Your claimed rewards" id = "rwTest">
            <div v-if="claimedRewards.length != 0">
                <div v-for="claimedReward in claimedRewards" :key="claimedReward.id" class = "enReward"> 
                    <h2>Reward Title: {{ claimedReward.rewardTitle }}</h2>
                    <p>Description: {{ claimedReward.rewardDescription }}</p>
                </div>
            </div>
            <div v-else class = "empty-rewards">
                <img src = "../assets/icons/no-rewards.png">
                <p>You haven't claimed any rewards yet</p>
            </div>

        </n-drawer-content>
    </n-drawer>

</template>

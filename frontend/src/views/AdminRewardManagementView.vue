<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue';
import axios from 'axios';


const modalStatus = ref(false);
const rewards = ref([]);

const rewardName = ref("");
const rewardDescription = ref(""); 
const pointsRequired = ref(0);
const expiresAt = ref(null);


function openModal(){
    modalStatus.value = true;
}
function closeModal(){
    modalStatus.value = false;
}

async function submitReward(){
    const rewardData = {
        rewardTitle: rewardName.value,
        rewardDescription: rewardDescription.value,
        pointsRequired: pointsRequired.value,
        expirationDate: expiresAt.value
    }
    try{
        const response = await axios.post("http://localhost:8000/poll-reward/addReward",
        rewardData,
        { withCredentials: true });
        console.log("Reward added:", response.data);
        closeModal();
    }
    catch(error){
        console.log(error)
    }
}
//TODO: PRIKAZ VSEH REWARDOV IN UREJANJE IN BRISANJE REWARDOV 

</script>
<template>
    <h1>Reward Management</h1>
    <p>Here you can manage rewards for citizens.</p>
    <n-button @click="openModal">Add a reward</n-button>





    <n-modal v-model:show="modalStatus" preset="dialog" title="Add reward"
    positive-text="Add Reward"
    negative-text="Cancel"
    @positive-click="submitReward"
    @negative-click="closeModal">
    
    <template #icon>
        <img src="../assets/icons/reward_add_modal.svg" />
    </template>


    <label for="rewardName">Reward Name:
        <n-input id="rewardName" v-model:value="rewardName" placeholder="Enter reward name"></n-input>
    </label>

    <label for="rewardDescription">Reward description:
        <n-input id="rewardDescription" v-model:value="rewardDescription" placeholder="Enter reward description"></n-input>
    </label>

    <label for="pointsRequired">Points Required:
        <n-input-number id="pointsRequired" v-model:value="pointsRequired" placeholder="Enter points required" ></n-input-number>
    </label>
    
    <label for="expiresAt">Expires at:
        <n-date-picker v-model:value="expiresAt" type="date" placeholder="Select expiration date" />
    </label>
    
    </n-modal>
</template>
<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { message } from 'ant-design-vue';


const modalStatus = ref(false);
const modalEditStatus = ref(false);
const rewards = ref([]);

const rewardName = ref("");
const rewardDescription = ref(""); 
const pointsRequired = ref(0);
const expiresAt = ref(null);
const selectedReward = ref(null);
const editedRewardName = ref("");
const editedRewardDescription = ref("");
const editedPointsRequired = ref(0);
const editedExpiresAt = ref(null);


function openModal(){
    modalStatus.value = true;
}
function closeModal(){
    modalStatus.value = false;
}

function openModalEdit(reward){
    modalEditStatus.value = true;
    selectedReward.value = reward;
}

function closeModalEdit(){
    modalEditStatus.value = false;
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


async function getAdminRewards(){
    try{
        const response = await axios.get("http://localhost:8000/poll-reward/getAllRewardsAdmin",
        { withCredentials: true });
        rewards.value = response.data;
        console.log("Admin rewards:", rewards.value);
    }
    catch(error){
        console.log(error)
    }
}
//DELETE REWARD FUNKCIJA
async function deleteReward(rewardId){
    try{
        //SPREMENI ENDPOINT
        const response = await axios.post('http://localhost:8000/poll-reward/deleteReward',
        //POSLJEM REWARD ID V BACKEND DA VES KERGA IZBRISAT
        { rewardId: rewardId },
        { withCredentials: true }
    );
        message.success(response.data.message);
        getAdminRewards();
    }
    catch(error){
        console.log(error)
    }
}


async function editReward(){
    const editedReward = {
        id: selectedReward.value.id,
        rewardTitle: selectedReward.value.rewardTitle,
        rewardDescription: selectedReward.value.rewardDescription,
        pointsRequired: selectedReward.value.pointsRequired,
        expirationDate: selectedReward.value.expirationDate
    };
    try{
        //SPREMENI ENDPOINT
        const response = await axios.post('http://localhost:8000/poll-reward/editReward',
        //POSLJEM PODATKE NOVEGA REWARDA V BACKEND DA GA UPDATAS
        editedReward,
        {withCredentials: true}
    );
    if(response.data.statusCode === 200){
        message.success(response.data.message);
    }
    else{
        message.error(response.data.message);
    }
    console.log("EDITED REWARD",editedReward)
    closeModalEdit();
    getAdminRewards();
}

    catch(error){
        console.log(error)
        console.log("EDITED REWARD",editedReward)
    }
}

onMounted(() => {
    getAdminRewards();
});
//TODO: PRIKAZ VSEH REWARDOV IN UREJANJE IN BRISANJE REWARDOV 

</script>
<template>
    <h1>Reward Management</h1>
    <p>Here you can manage rewards for citizens.</p>
    <n-button @click="openModal">Add a reward</n-button>
    <div class = "polls-container">
        <div v-for="reward in rewards" :key="reward.id" class = "EnPoll"> 
            <h2>Reward Title: {{ reward.rewardTitle }}</h2>
            <p>Description: {{ reward.rewardDescription }}</p>
            <p>Points Required: {{ reward.pointsRequired }}</p>
            <div class="rewardEditDelete">
                <n-button class = "deleteReward" @click="deleteReward(reward.id)">Delete Reward</n-button>
                <n-button class = "editReward" @click="openModalEdit(reward)">Edit Reward</n-button>
            </div>
            <!--TODO: SISTEM ZA UREJANJE IN BRISANJE REWARDOV JE POTREBNO SE-->
        </div>
    </div>

    <!--ADD REWARD MODAL-->
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

    <!--EDIT REWARD MODAL-->
    <n-modal v-model:show="modalEditStatus" preset="dialog" title="Edit Reward"
    positive-text="Confirm Changes"
    negative-text="Cancel"
    @positive-click="editReward"
    @negative-click="closeModalEdit">
    
    <template #icon>
        <img src="../assets/icons/reward_add_modal.svg" />
    </template>

    
        <label for="rewardName">Reward Name:
            <n-input id="rewardName" v-model:value="selectedReward.rewardTitle" placeholder="Enter reward name"></n-input>
        </label>

        <label for="rewardDescription">Reward description:
            <n-input id="rewardDescription" v-model:value="selectedReward.rewardDescription" placeholder="Enter reward description"></n-input>
        </label>

        <label for="pointsRequired">Points Required:
            <n-input-number id="pointsRequired" v-model:value="selectedReward.pointsRequired" placeholder="Enter points required" ></n-input-number>
        </label>
        
        <label for="expiresAt">Expires at:
            <n-date-picker 
            v-model:value="selectedReward.expirationDate" 
            type="date" 
            placeholder="Select expiration date" 
            :is-date-disabled="(dateDanes) => dateDanes < Date.now()"
            />
            <!--DODAN VALIDATOR V DATETIME PICKER DA NEMORES IZBRAT PRETEKLIH DATUMOV-->
        </label>
        </n-modal>

</template>
<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import axios from 'axios'
import { NModal, NButton } from "naive-ui";


const admins = ref([]);
const uporabniki = ref([]);
const showModal = ref(false);
const selectedUser = ref(null);

const openUserModal = (uporabnik) => {
    selectedUser.value = uporabnik;
    console.log("TEST",selectedUser.value.userId)
    //razlaga za spodnjo vrstico
    selectedUser.value.isAdmin = admins.value.some(admin => admin.userId === uporabnik.userId)
    console.log("Is admin = ",selectedUser.value.isAdmin,uporabnik.userId)
    showModal.value = true;
};
function closeModal(){
    showModal.value = false;
}

const update = async() =>{
    try{
        const response = await axios.post("http://localhost:8080/auth/updateUser",
        selectedUser.value,
        {withCredentials:true});
        console.log("Successfuly updated user", response.data);
        showModal.value = false; //zaprem modal
        await getAllUsers(); //poklicem funkcijo da dobim nove osvežene podatke
        
    }
    catch(error){
        console.log(error);
    }
}

const getAllUsers = async () => {
    try {
        const response = await axios.get(
            'http://localhost:8080/data/getAllUsers', {
            withCredentials: true
        })
        //console.log(response.data)
        uporabniki.value = response.data.uporabniki
        admins.value = response.data.admins

        //console.log(admins.value)
    }
    catch (error) {
        console.log(error)
    }
}
//posljem userId ko admin klikne na more info da iz backenda prejmem podatke za dolocen userId
const userIdSend = async () => {
    try {
        const response = await axios.post("http://localhost:8080/auth/updateUser",
        selectedUser.value.userId,
        {withCredentials:true});
    }
    catch (error) {
        console.log(error)
    }
}
// getam podatke iz backenda za profil data ki so bili vneseni v profilecreationu
const profileData = async() => {
    try{
        const response = await axios.get(
        'http://localhost:8080/auth/POSODOBI_ENDPOINT',
        {withCredentials:true}
        )
        profil.value = response.data;
        console.log(profil.value);
    }
    catch(error){
        console.log(error);
    }

}



onMounted(() => {
    getAllUsers()
});
</script>
<template>
    <h1>User Management</h1>

    <!--LISTAM USE USERJE-->
    <div class="users_list">
        <n-table :bordered="true" :single-line="false">
  <thead>
    <tr>
      <th>Username</th>
      <th>Email</th>
      <th>UserId</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="uporabnik in uporabniki" :key="uporabnik.userId">
      <td>{{ uporabnik.username }}</td>
      <td>{{ uporabnik.email }}</td>
      <td>{{ uporabnik.userId }}</td>
      <td>
        <n-button text @click="() => { openUserModal(uporabnik); userIdSend(); }" >More Info</n-button>
      </td>
    </tr>
  </tbody>
</n-table>
    </div>
    <n-modal v-model:show="showModal" preset="dialog" title="Edit or View User">
        <template #default>
            <!--Narejeno tako da ce podatek ni najden ne vrze errora ampak je preprosto null-->
            <label for id="username"> Username:
                <n-input id="username" placeholder="" v-model:value="selectedUser.username"></n-input>
            </label>
            <label for id="password"> Password (Encrypted):
                <n-input id="password" placeholder="" v-model:value="selectedUser.email"></n-input>
            </label>
            <label for id="username"> User ID:
                <n-input id="username" placeholder=""v-model:value="selectedUser.userId"></n-input>
            </label>

            <label for id="admin_state"> Add admin?
                <n-checkbox id="admin_state" v-model:checked="selectedUser.isAdmin"></n-checkbox>
            </label>


            <n-button @click="update">Update</n-button>
            <n-button @click="closeModal()">Close</n-button>
        </template>
    </n-modal>

</template>
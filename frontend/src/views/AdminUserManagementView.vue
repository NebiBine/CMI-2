<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import axios from 'axios'
import { NModal, NButton } from "naive-ui";


const admins = ref([]);
const uporabniki = ref([]);
const profil = ref([]);
const showModal = ref(false);
const selectedUser = ref(null);

const openUserModal = (uporabnik) => {
    selectedUser.value = uporabnik;
    console.log("TEST",selectedUser.value.userId)
    //razlaga za spodnjo vrstico
    selectedUser.value.isAdmin = admins.value.some(admin => admin.userId === uporabnik.userId)
    console.log("Is admin = ",selectedUser.value.isAdmin,uporabnik.userId);
    userIdSend();
    showModal.value = true;
};
function closeModal(){
    showModal.value = false;
}

const update = async() =>{
    try{
        const response = await axios.post("http://localhost:8080/data/updateUser",
        profil.value,
        {withCredentials:true});
        console.log("Successfuly updated user", response.data);
        showModal.value = false; //zaprem modal
        await getAllUsers(); //poklicem funkcijo da dobim nove osvežene podatke
        
    }
    catch(error){
        console.log(error);
    }
}

/*
1.---------------------------------------------------------------------

GET ALL USERS TI POSLE ZDEJ TO:
[
   {
      "userId":"3cb33496-96dc-493d-8842-78ff8ff0b96c",
      "username":"bine",
      "hashPass":"scrypt:32768:8:1$D7x098jYSoywOz7I$efc7849879a54a02fc619e0fb2ee5226b8d0080bcaf725d7148806314aa164f7208692db79102672b9bd1e6be14f286896c83042c742d490f7669e6c2be59265",
      "email":"bine.tavcar@gmail.com"
   },
   {
      "userId":"89f644c0-336f-4cc5-92d7-02dc83df3f2a",
      "username":"nace",
      "hashPass":"scrypt:32768:8:1$nnuzbDrZGZi6Guaq$268306560e7d925e15bead2710f00b13358607264555c458cf350b2e4f0c571c27ba982e3a772a9ae39e4d7497aadb72e072438e3aa9134059d644874d6460da",
      "email":"nacerozman3@gmail.com"
   }...
]
BREZ ADMINA,!!!!


2.--------------------------------------------------
ADMIN BO ZDEJ V TVOJI FUNKCIJI userIdSend V /DATA/GETPROFILE IN SICER: pocakat rabm tebe za test dase lahko prkaze da vids kasn json drgac vrjetn bo tko

{
   "userId":"3cb33496-96dc-493d-8842-78ff8ff0b96c",
   "username":"bine",
   "hashPass":"scrypt:32768:8:1$D7x098jYSoywOz7I$efc7849879a54a02fc619e0fb2ee5226b8d0080bcaf725d7148806314aa164f7208692db79102672b9bd1e6be14f286896c83042c742d490f7669e6c2be59265",
   "email":"bine.tavcar@gmail.com",
   "isAdmin":true/false --> za checkbox k bos odpru view more
}

3.--------------------------------------------------
ideja: 
    pr actions lahko dava se delete user, da ga zbriseva, ni velka zadeva sam da vec funkcionalnosti

4.---------------------------------------------------
K BOS UPDEJTU USER NA /data/updateUser PRCAKUJE TA DATA, LAHKO DAVA KEJ STRAN TO NI PROBLEM, DODT PA TESKO, PLUS ADMIN
updateUser prcakuje:
    data = {
    "userId":123,
    "Fullname":fullName,
    "username":username,
    "birth":birth,
    "phone":phone,
    "street":street,
    "city":city,
    "country":country,
    "zip":zip,
    "isAdmin":isAdmin --> true/false, ali je checked al ni tojto
    }

VRNE TI PA ISTI JSON KSI MI GA POSLOU, IDENTITIČEN, POD POGOJEM DA NI BLO ERRORJA, SEPRAV PO ŽE NARJENE UPDEJTU V DB

*/
const getAllUsers = async () => {
    try {
        const response = await axios.get(
            'http://localhost:8080/data/getAllUsers', {
            withCredentials: true
        })
        //console.log(response.data)
        uporabniki.value = response.data
        //debug print
        console.log(uporabniki.value)
    }
    catch (error) {
        console.log(error)
    }
}
//posljem userId ko admin klikne na more info da iz backenda prejmem podatke za dolocen userId
const userIdSend = async () => {
    try {
        const response = await axios.post("http://localhost:8080/data/getProfile", //||BACK POSLE ISTO ZADEVO K U DASHBOARD VIEW + ISADMIN, SAM PRKAZ PODATKE, poglej gor||    
        {userId : selectedUser.value.userId},
        {withCredentials:true});

        profil.value = response.data;
        console.log(profil)
    }
    catch (error) {
        console.log(error)
    }
}
// getam podatke iz backenda za profil data ki so bili vneseni v profilecreationu
//||TEGA POMOJE NE RABS, DODT RABS ZA UPDATE GUMB FUNKCIJO, K POSLE CELO FORMO, LAHKO JE ISTO ALPA NI, VRNIL TI BO NOVE REFRESHANE UPDTEJTANE PODATKE||




onMounted(() => {
    getAllUsers();
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
            <label for id="fullName"> Full Name:
                <n-input id="fullName" placeholder="" v-model:value="profil.fullName"></n-input>
            </label>
            <label for id="username"> Username:
                <n-input id="username" placeholder="" v-model:value="profil.username"></n-input>
            </label>
            <label for id="birth"> Date of Birth:
                <n-input id="birth" placeholder="" v-model:value="profil.birth"></n-input>
            </label>
            <label for id="phone"> Mobile Number:
                <n-input id="phone" placeholder=""v-model:value="profil.phone"></n-input>
            </label>
            <label for id="street"> Street:
                <n-input id="street" placeholder=""v-model:value="profil.street"></n-input>
            </label>
            <label for id="city"> City:
                <n-input id="city" placeholder=""v-model:value="profil.city"></n-input>
            </label>
            <label for id="country"> Country:
                <n-input id="country" placeholder=""v-model:value="profil.country"></n-input>
            </label>
            <label for id="zip"> Zip Code:
                <n-input id="zip" placeholder=""v-model:value="profil.zip"></n-input>
            </label>
            

            <label for id="admin_state"> Add admin?
                <n-checkbox id="admin_state" v-model:checked="profil.isAdmin"></n-checkbox>
            </label>


            <n-button @click="update">Update</n-button>
            <n-button @click="closeModal()">Close</n-button>
        </template>
    </n-modal>

</template>
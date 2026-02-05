<script setup>
    import '../assets/styles/mainStyle.css'
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';

    const weatherData = ref([]);

    async function getWeatherData(){
      try{
        const response = await axios.get('http://localhost:8000/weather/getWeather',
        {withCredentials: true});
        weatherData.value = response.data;
        console.log("Weather data:", weatherData.value);
      }
      catch(error){
        console.error('Error fetching weather data:', error);
      }
    }
  onMounted(() => {
      getWeatherData();
  });
</script>
<template>
    <h1>Weather</h1>
    <p>Look through the weather forecast and keep an eye on the weather alerts if there are any!</p>
    <n-tabs type="line" animated class="zavihki_weather">
      <n-tab-pane name="currentWeather" tab="🌤️ Current Weather">
        <p>Weather details for today will be displayed here.</p>
        <!--TRENUTNO VREME PRIDE TUKAJ-->
      </n-tab-pane>
      <n-tab-pane name="forecast" tab="📅 Weather Forecast">
        <p>Weather details for 3 days in advance will be displayed here.</p>
        <!--NAPOVED VREMENA PRIDE TUKAJ-->
      </n-tab-pane>
      <n-tab-pane name="alerts" tab="⚠️ Weather Alerts">
        <p>Weather alerts will be displayed here.</p>
        <!--VREMENSKI ALERTI PRIDEJO TUKAJ-->
      </n-tab-pane>
    </n-tabs>

</template>
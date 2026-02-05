<script setup>
    import '../assets/styles/mainStyle.css'
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';

    const weatherData = ref(null);

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
        <div v-if="weatherData">
          <img :src="weatherData.weather.current.icon" alt="Weather Icon" />
          <p>Condition: {{ weatherData.weather.current.condition }}</p>
          <p>Temperature: {{ weatherData.weather.current.temp_c }}°C</p>
          <p>Feels like: {{ weatherData.weather.current.feelslike_c }}°C</p>
          <p>Humidity: {{ weatherData.weather.current.humidity }}%</p>
          <p>Dew Point: {{ weatherData.weather.current.dewpoint_c }}°C</p>
          <p>Wind speed: {{ weatherData.weather.current.wind_kph }} kph</p>
        </div>
        
        <!--TRENUTNO VREME PRIDE TUKAJ-->
      </n-tab-pane>
      <n-tab-pane name="forecast" tab="📅 Weather Forecast">
        <!-- <p>Weather details for 3 days in advance will be displayed here.</p> -->
      <div v-if="weatherData.weather.forecast">
        <div v-for="day in Object.values(weatherData.weather.forecast)" :key="day" class="forecast-day">
          <h3>Date: {{ new Date(day.date).toLocaleDateString() }}</h3>
          <img :src="day.icon" alt="Weather Icon" />
          <p>Condition: {{ day.condition }}</p>
          <p>Max Temp: {{ day.max_temp_c }}°C</p>
          <p>Min Temp: {{ day.min_temp_c }}°C</p>
          <p>Humidity: {{ day.avg_humidity }}%</p>
        </div>
      </div>
      </n-tab-pane>
      <n-tab-pane name="alerts" tab="⚠️ Weather Alerts">
        <p>Weather alerts will be displayed here.</p>
        <div v-if="weatherData.weather.alerts">
          <div v-for="alert in Object.values(weatherData.weather.alerts)" :key="alert" class="alert">
            <h3>{{ alert.headline }}</h3>
            <p>{{ alert.desc }}</p>
            <p>Severity: {{ alert.severity }}</p>
            <p>Areas: {{ alert.areas }}</p>
            <p>Urgency: {{ alert.urgency }}</p>
            <p>Event: {{ alert.event }}</p>
            <p v-if="alert.instruction != ''">
              Instructions: {{ alert.instruction }}
            </p>
            <p v-else>
              Instructions: No specific instructions provided.
            </p>
          </div>
        </div>
      </n-tab-pane>
    </n-tabs>

</template>
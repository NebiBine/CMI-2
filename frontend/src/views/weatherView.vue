<script setup>
    import '../assets/styles/mainStyle.css'
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';
    import { ThermometerSun,ThermometerSnowflake,Droplets } from 'lucide-vue-next';

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

    function toSeverityClass(severity) {
      const key = String(severity || "").toLowerCase();
      if (key === "severe") return "alert-severe";
      if (key === "moderate") return "alert-moderate";
      if (key === "minor") return "alert-minor";
      return "alert-unknown";
    };
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
          <img :src="weatherData.weather.current.icon" alt="Weather Icon" width="70" height="70"/>
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
      <div v-if="weatherData.weather.forecast" class ="forecast-container">
        <div v-for="day in Object.values(weatherData.weather.forecast)" :key="day" class="forecast-day">
          <h3 style="font-weight: bolder; font-size: 18px;">{{ new Date(day.date).toLocaleDateString(undefined, { weekday: "long" }) }}</h3>
          <h3 style="margin-top: -25px;margin-bottom: 30px;">Date: {{ new Date(day.date).toLocaleDateString() }}</h3>
          <img :src="day.icon" alt="Weather Icon" width="70" height="70" style="display: block; margin: 0 auto;"/>
          <p id="forecast-condition">Condition: {{ day.condition }}</p>
          <div class="temp-range">
            <p style = "display: flex; flex-direction: row; gap:5px; top: 15px;"><ThermometerSun :size="15" /> Temp: {{ day.max_temp_c }}°C</p>
            <p style = "display: flex; flex-direction: row; gap:5px; top: 15px;"><ThermometerSnowflake :size="15" /> Min Temp: {{ day.min_temp_c }}°C</p>
          </div>
          <div class="humidity-precipitation">
            <p style = "display: flex; flex-direction: row; gap:5px; top: 15px;"><Droplets :size="15" /> Humidity: {{ day.avg_humidity }}%</p>
            <p style = "display: flex; flex-direction: row; gap:5px; top: 15px;">Precipitation: {{ day.total_precip_mm }} mm</p>
          </div>
        </div>
      </div>
      </n-tab-pane>
      <n-tab-pane name="alerts" tab="⚠️ Weather Alerts">
        <p>Weather alerts will be displayed here.</p>
        <div v-if="weatherData.weather.alerts" class="alerts-container">
          <div v-for="alert in Object.values(weatherData.weather.alerts)" :key="alert" :class="['alert-card', toSeverityClass(alert.severity)]">
            <n-collapse class="alert-collapse">
              <n-collapse-item :name="alert.headline">
                <template #header>
                  <div class="alert-header">
                    <span class="alert-title">{{ alert.headline }}</span>
                    <span class="alert-badge">{{ alert.severity }}</span>
                  </div>
                </template>
                <p class="alert-desc">{{ alert.desc }}</p>
                <div class="alert-meta">
                  <div class="meta-item">
                    <span class="meta-label">Areas</span>
                    <span class="meta-value">{{ alert.areas }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">Urgency</span>
                    <span class="meta-value">{{ alert.urgency }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">Event</span>
                    <span class="meta-value">{{ alert.event }}</span>
                  </div>
                </div>
                <p v-if="alert.instruction != ''" class="alert-instruction">
                  {{ alert.instruction }}
                </p>
                <p v-else class="alert-muted">
                  No specific instructions provided.
                </p>
              </n-collapse-item>
            </n-collapse>
          </div>
        </div>
      </n-tab-pane>
    </n-tabs>

</template>
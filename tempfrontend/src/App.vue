<template>
  <div id="app">
        <line-chart v-if="loaded" :chartdata="chartdata" :options="options" :height="100"/>
        <line-chart v-if="loaded" :chartdata="humidityData" :options="options" :height="100"/>
  </div>
</template>

<script>
import LineChart from './components/Chart'
import axios from 'axios'
export default {
  name: 'App',
  components: { LineChart },
  data(){
    return{
      loaded: false,
      chartdata: Object,
      humidityData: Object,
      options: {
            title:{
              display: true,
              text: 'Temperature °C'
            },
            scales: {
            xAxes: [{
                type: 'time',
                distribution: 'linear'
            }],
            yAxes: [{
              ticks: {
                suggestedMin: 0,
                suggestedMax: 30
            },
          }]
        }
      }
    }
  },
    methods:{
    getRandomInt () {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      },
      processData(cObj,dtype){
        var deviceNames = cObj.map(c=>c.device);
        var uniqueDeviceNames = Array.from(new Set(deviceNames));
        var timestampLabels = cObj.map(c=>c.timestamp);

        var processedDatasets = [];
        var processedChartData = {};

        uniqueDeviceNames.forEach(d=>{
          var singleObj = {};
          var dataset;
          if (dtype == 0){
              dataset = cObj.filter(c=>c.device==d).map(c=>c.temp);
          } else if (dtype==1){
              dataset = cObj.filter(c=>c.device==d).map(c=>c.humidity);
          } else {
            dataset = cObj.filter(c=>c.device==d).map(c=>c.light);
          }
          
          var backgroundColour =  cObj.filter(c=>c.device==d).map(c=>c.colour)[0];
          //var timeset = cObj.filter(c=>c.device==d).map(c=>c.timestamp);
          singleObj['label'] = d.split(' ')
                                .map(w => w[0].toUpperCase() + w.substr(1).toLowerCase())
                                .join(' ');
          singleObj['data'] = dataset;
          singleObj['backgroundColor'] = backgroundColour;
          singleObj['borderColor'] = backgroundColour;
          singleObj['fill'] = false;
          //singleObj['t'] = timeset;
          processedDatasets.push(singleObj);
        });

        processedChartData['labels'] = timestampLabels
        processedChartData['datasets'] = processedDatasets

        return processedChartData
      },
      getHumidityData(){
        this.humidityData = this.processData(this.chartdata,1)
      }
  },
  async mounted () {
    this.loaded = false
    try {
      axios.get("http://localhost:3000/api/temperature")
          .then(res => {
            this.chartdata = this.processData(res.data,0);
            this.humidityData = this.processData(res.data,1);
            this.loaded = true}
            )
          .catch(err => console.log(err));
     
    } catch (e) {
      console.error(e)
    }
  }
}

</script>

<style>
</style>
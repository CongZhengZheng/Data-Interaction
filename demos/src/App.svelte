<script>
  import * as d3 from 'd3';
	import {onMount} from 'svelte';
  import Map from './Map.svelte';
  import Histogram from './Histogram.svelte';

	let data = [];
  let fullData = [];
  let filter1 = [];
  let filter2 = [];
  let filter3 = [];
  let selectedTract = null;

  let var1 = 'aggravate';
  let var2 = 'burglary';
  let var3 = 'drug abuse';
  

	onMount(async function() {
    // load data from csv (source: https://chicagohealthatlas.org/download)
    let table = d3.csv('chi-crime-data.csv', (d) => ({
          ...d,
          'Name': d['Name'].substring(6),
          'Population': d['Population'],
          'CZA_2023': +d['CZA_2023'],
          'CZB_2023': +d['CZB_2023'],
          'CZD_2023': +d['CZD_2023'],
          'CZH_2023': +d['CZH_2023']
        }));

    let geocoord = d3.json('census-tracts.geojson')
      .then((d) => d.features);
    
    await Promise.all([table, geocoord]).then((values) => {
      // console.log(values);
      let table = values[0];
      let geocoord = values[1];
      // join the variables we want to show on the map
      for (let i = 0; i < geocoord.length; i++) {
        let tract = geocoord[i].properties.name10;
        let found = false;
        let j = 0;
        while (!found && table.length > j) {
          if (table[j].Name == tract) {
            found = true;
            data.push(geocoord[i]);
            data[data.length - 1].properties['population'] = table[j]['Population']
            // data[data.length - 1].properties['popChange'] = table[j]['CIP_2010-2020']
            // data[data.length - 1].properties['rentRatio'] = table[j]['RBU_2018-2022'] / table[j]['RBS_2018-2022']
            data[data.length - 1].properties['aggravate'] = table[j]['CZA_2023']
            data[data.length - 1].properties['burglary'] = table[j]['CZB_2023']
            data[data.length - 1].properties['drug abuse'] = table[j]['CZD_2023']
            data[data.length - 1].properties['homicide'] = table[j]['CZH_2023']
            // grab other variables as needed
          } else {
            j++;
          }
        }
      }
      // console.log(data);
      fullData = [...data];
    });
	});

  function updateData() {
    data = fullData.filter(d => 
        (!filter1.length || (d.properties['aggravate'] >= filter1[0] && d.properties['aggravate'] <= filter1[1])) &&
        (!filter2.length || (d.properties['burglary'] >= filter2[0] && d.properties['burglary'] <= filter2[1])) &&
        (!filter3.length || (d.properties['drug abuse'] >= filter3[0] && d.properties['drug abuse'] <= filter3[1]))
    );
    }

  function handleSelectTract(event) {
    selectedTract = event.detail.tract; 
  }

  function resetSelection() {
    selectedTract = null;
    filter1 = [];
    filter2 = [];
    filter3 = [];
    updateData();
    document.dispatchEvent(new CustomEvent('reset-brush'));

  }


</script>

<main>
  <h1>Chicago Crime Data in 2023</h1>
  <div style="text-align: left; max-width: 700px; margin: 10px 0 20px 0; color: lightgray;">
    <p style="margin-left: 10px;">Interact with the data in two ways:</p>
    <ol style="margin: 10px 0 20px 30px; padding-left: 0; list-style-position: outside;">
      <li style="margin-bottom: 15px;">Use brush filtering on the histograms to see the distribution of crime data and select census tracts that fall within this range.</li>
      <li style="margin-bottom: 15px;">Click on each tract on the map to view the specific crime data of that selected tract.</li>
    </ol>
    <p style="margin-left: 10px;">Use the <strong>'Reset Selection'</strong> button to clear the current selection.</p>
  </div>
  <button on:click={resetSelection}>Reset Selection</button>
  <div class="flex-container row">
    <Map data={data} fullData={fullData} on:selectTract={handleSelectTract}/>
    <div class="flex-container col">
      <figure class="hist">
        <Histogram data={data} fullData={fullData} selectedTract={selectedTract} variable={var1} bind:filter={filter1} update={updateData} />
        <figcaption>Aggravated Assault/Battery Incidents in 2023</figcaption>
      </figure>
      <figure class="hist">
        <Histogram data={data} fullData={fullData} selectedTract={selectedTract} variable={var2} bind:filter={filter2} update={updateData} />
        <figcaption>Burglary Incidents in 2023</figcaption>
      </figure>
      <figure class="hist">
        <Histogram data={data} fullData={fullData} selectedTract={selectedTract} variable={var3} bind:filter={filter3} update={updateData} />
        <figcaption>Drug Abuse Incidents in 2023</figcaption>
      </figure>
    </div>
  </div>
</main>

<style>
  .flex-container {

    display: flex;
    
    justify-content: center;  
    /* flex-flow: row; */ 
    

    height: 100%;
    padding: 15px;
    gap: 5px;

  }

  .flex-container > div{
    padding: 8px;
  }

  .flex-container .row {
    flex-direction: row;  
  }

  .flex-container .col {
    flex-direction: column;  
  }

  .map { 
    /* flex:1 1 auto; */
    flex-grow:1;
  }
			
  .hist { 
    /* flex:0 1 auto; */
    flex-grow:0;
  }
			

</style>
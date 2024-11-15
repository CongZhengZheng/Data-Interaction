<script>
  import Histogram from './Histogram.svelte';
  import { onMount } from 'svelte';
  import LineChart from './LineChart.svelte';
  import * as d3 from 'd3';

  let allData = [];
  let filteredData = [];
  let selectedAgeGroup = '';
  let selectedGenre = '';

  onMount(async () => {
    allData = await d3.csv('video_game_reviews.csv', d => ({
      Title: d['Game Title'],
      UserRating: +d['User Rating'],
      AgeGroupTargeted: d['Age Group Targeted'],
      Price: d['Price'],
      Platform: d['Platform'],
      RequiresSpecialDevice: d['Requires Special Device'],
      Developer: d['Developer'],
      Publisher: d['Publisher'],
      ReleaseYear: d['Release Year'],
      Genre: d['Genre'],
      Multiplayer: d['Multiplayer'],
      GameLength: d['Game Length (Hours)'],
      GraphicsQuality: d['Graphics Quality'],
      SoundtrackQuality: d['Soundtrack Quality'],
      StoryQuality: d['Story Quality'],
      UserReviewText: d['User Review Text'],
      GameMode: d['Game Mode'],
      MinNumberofPlayers: d['Min Number of Players']
    }));
    filteredData = allData;
    console.log("Loaded Data:",allData)
  });

  $: {filteredData = allData.filter(d =>
    (selectedAgeGroup === '' || d.AgeGroupTargeted === selectedAgeGroup) &&
    (selectedGenre === '' || d.Genre === selectedGenre)
  );
  console.log("Filtered data:", filteredData);}
</script>

<main>
  <h1>All about Video Games!</h1>
  <p id="intro-text">
    With the birth of the first massive-scale computer machine and "Hello World" as the first computer programme, video games,
    now considered as the ninth art, have grown and peaked in 21st century for its unparallel qualities of narratives, soundtracks, graphics, etc. alongside
     with the development of hardware and Internet. 
    It is simply an enjoyment to play games. Whether you’re the competitive type, a team player, someone who enjoys a good story, or just likes to explore, you can always find
    your belongings and communities in this era, where many high-quality video games are coming out from all over the world.
    This website is all about catching you up on the latest in video games from the last decade or so (2010-2023). Wondering which games are worth your time or how the world of gaming has evolved? You're in the right place! <br><br>
    The dataset is from: <a href="https://www.kaggle.com/datasets/jahnavipaliwal/video-game-reviews-and-ratings/data" target="_blank">Kaggle Dataset</a>.
  </p>
  <h2>1. The 50 Best Games Worth Buying</h2>
  <p id="section1-text"> 
    Overwhelmed by too many great games and not enough time to try them all? No worries! Here is a list of the top 50 games based on user ratings — definitely worth your time and money. Use the filters to tailor the list to your preferences, and click on any bar in the chart to dive deeper into the details. It's a blast to pick the best of the best and add them to your cart!
  </p>
  <div class="controls">
    <label for="ageGroup">Age Group:</label>
    <select id="ageGroup" bind:value={selectedAgeGroup}>
      <option value="">All Ages</option>
      {#each Array.from(new Set(allData.map(d => d.AgeGroupTargeted))) as ageGroup}
        <option value={ageGroup}>{ageGroup}</option>
      {/each}
    </select>

    <label for="genre">Genre:</label>
    <select id="genre" bind:value={selectedGenre}>
      <option value="">All Genres</option>
      {#each Array.from(new Set(allData.map(d => d.Genre))) as genre}
        <option value={genre}>{genre}</option>
      {/each}
    </select>
  </div>
 
  <div class="chart-container">
    <Histogram filteredData={filteredData}/>
  </div>
  <div class="chart-container">
    <LineChart/>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    max-width: 960px; 
    margin: auto;
  }

  h1, h2, p {
    text-align: left;
    width: 100%; 
  }
  .chart-container {
    width: 100%; 
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
  }
  .controls {
    width: 100%;
    display: flex;
    justify-content: flex-start;
    gap: 10px; 
    margin-bottom: 20px;
  }

</style>






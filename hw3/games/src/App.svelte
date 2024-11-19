<script>
  import Histogram from './Histogram.svelte';
  import { onMount } from 'svelte';
  import LineChart from './LineChart.svelte';
  import * as d3 from 'd3';
  import { writable } from 'svelte/store';
  import PieChart from './PieChart.svelte';

  let allData = [];
  let filteredData1 = [];
  let filteredData2 = [];
  let filteredData3 = [];
  let selectedAgeGroup = '';
  let selectedGenre = '';
  let selectedPlatform = '';
  let selectedGameMode = '';
  let selectedGameDetails = writable('');
  let selectedAttribute = writable('Price');
  let selectedYear = writable('');
  

  onMount(async () => {
    allData = await d3.csv('video_game_reviews.csv', d => ({
      Title: d['Game Title'],
      UserRating: (((+d['User Rating']-10.5)/40) * 10),
      AgeGroupTargeted: d['Age Group Targeted'],
      Price: +d['Price'],
      Platform: d['Platform'],
      RequiresSpecialDevice: d['Requires Special Device'],
      Developer: d['Developer'],
      Publisher: d['Publisher'],
      ReleaseYear: +d['Release Year'],
      Genre: d['Genre'],
      Multiplayer: d['Multiplayer'],
      GameLength: +d['Game Length (Hours)'],
      GraphicsQuality: d['Graphics Quality'],
      SoundtrackQuality: d['Soundtrack Quality'],
      StoryQuality: d['Story Quality'],
      UserReviewText: d['User Review Text'],
      GameMode: d['Game Mode'],
      MinNumberofPlayers: +d['Min Number of Players']
    }));
    filteredData1 = allData;
    filteredData2 = allData;
    filteredData3 = allData;
    console.log("Loaded Data:",allData)
  });

  $: {filteredData1 = allData.filter(d =>
    (selectedAgeGroup === '' || d.AgeGroupTargeted === selectedAgeGroup) &&
    (selectedGenre === '' || d.Genre === selectedGenre) &&
    (selectedPlatform == '' || d.Platform === selectedPlatform) &&
    (selectedGameMode == '' || d.GameMode === selectedGameMode)
  );
  console.log("Filtered data:", filteredData1);}
</script>

<main>
  <h1>All about Video Games!</h1>
  <p id="intro-text">
    With the birth of the first massive-scale computer machine and "Hello World" as the first computer programme, video games,
    now considered as the ninth art, have grown and peaked in 21st century for its unparallel qualities of narratives, soundtracks, graphics, etc. alongside
     with the development of hardware and Internet. <br><br>
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

    <label for="platform">Platform:</label>
    <select id="platform" bind:value={selectedPlatform}>
      <option value="">All Platforms</option>
      {#each Array.from(new Set(allData.map(d => d.Platform))) as platform}
        <option value={platform}>{platform}</option>
      {/each}
    </select>

    <label for="gameMode">Game Mode:</label>
    <select id="gameMode" bind:value={selectedGameMode}>
      <option value="">All Games</option>
      {#each Array.from(new Set(allData.map(d => d.GameMode))) as gameMode}
        <option value={gameMode}>{gameMode}</option>
      {/each}
    </select>

  </div>
  <div class="info-box">
    {@html $selectedGameDetails || 'Click on a bar to see details...'}
  </div>
 
  <div class="scroll-container">
    <Histogram filteredData={filteredData1} {selectedGameDetails}/>
  </div>

  <h2>2. See the Gaming Industry Trends</h2>
  <p id="section2-text"> 
    Life moves quickly, and so does the gaming industry. Check out this summary to catch up with the trends in user ratings, prices, story quality, and more, covering the years 2010 to 2023. See how games have evolved over time!
  </p>

  <label for="attribute">Variable:</label>
  <select id="attribute" bind:value={$selectedAttribute}>
    <option value="UserRating">User Rating</option>
    <option value="Price">Price</option>
    <option value="GameLength">Game Length</option>
  </select>

  <div class="chart-container">
    <LineChart filteredData={filteredData2} attribute={$selectedAttribute} />
  </div>

  <p>On average, games in each year receive a score of around 4.8, the price is set at around 40 dollars, and the game length is around 32 hours.</p>

  <h2>3. Top 10 Game Developers of each year</h2>
  <p id="section3-text">
    As an avid gamer, big-name companies like Nintendo, Capcom, and Blizzard immediately spring to mind, along with indie studios like those behind <i>Disco Elysium</i> and the <i>Sherlock Holmes</i> Series. There are a thousand Hamlets in a thousand people's eyes. Nonetheless, here I would like to show you by statistics the top 10 game developers delivering on average the highest-rated games each year. While the quality of games from a developer can vary, this analysis seeks to identify those companies which consistently producing high-quality games. And a personal note — as a dedicated fan of Keiichiro Toyama, any game from them is an instant buy for me!
  </p>

  <div class="controls">
    <label for="yearSelect">Select Year:</label>
    <select id="yearSelect" bind:value={$selectedYear}>
      <!-- Dynamically generate year options based on data -->
      {#each Array.from(new Set(allData.map(d => d.ReleaseYear))).sort((a, b) => a - b) as year}
        <option value={year}>{year}</option>
      {/each}
    </select>

  </div>

  <PieChart data={filteredData3} year={$selectedYear}/>


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

  .scroll-container {
  width: 100%; 
  overflow-x: auto; 
  white-space: nowrap;
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

  .info-box {
    width: 300px;
    min-height: 100px;
    padding: 10px;
    margin-left: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 8px;
    color: #333;
    font-size: 0.9em;
    line-height: 1.4;
  }

</style>






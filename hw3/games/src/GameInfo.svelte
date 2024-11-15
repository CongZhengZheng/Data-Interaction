<script>
    export let game;
  </script>
  
  {#if game}
    <div class="info-container">
      <div class="info-row"><strong>Title:</strong> {game.Title}</div>
      <div class="info-row"><strong>Rating:</strong> {game.UserRating}</div>
      <div class="info-row"><strong>Price:</strong> ${game.Price.toFixed(2)}</div>
      <!-- Add more rows as needed -->
    </div>
  {:else}
    <div class="info-container">Click on a bar to see details...</div>
  {/if}
  
  <style>
    .info-container {
      display: flex;
      flex-direction: column;
      background: #f9f9f9;
      border: 1px solid #ccc;
      padding: 10px;
      margin-top: 10px;
    }
    .info-row {
      margin: 5px 0;
    }
  </style>
  
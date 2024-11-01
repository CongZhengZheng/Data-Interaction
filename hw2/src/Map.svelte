<script>
  import * as d3 from 'd3';
  import { legendColor } from 'd3-svg-legend';
  import { createEventDispatcher } from 'svelte';

  export let data;
  export let fullData;

  const dispatch = createEventDispatcher();

  let width = 500;
  let height = 500;

  let proj = d3.geoMercator()
      .scale(40000)
      .center([-87.39, 41.52])
      .translate([width, height]);
  let path = d3.geoPath().projection(proj);

  $: scale = d3.scaleSequential(d3.interpolatePiYG)
      .domain([
          d3.min(data.map(d => +d.properties.population)),
          d3.median(data.map(d => +d.properties.population)),
          d3.max(data.map(d => +d.properties.population))
      ]);

  let legend;
  $: {
      const colorLegend = legendColor()
          .shape('rect')
          .cells(9)
          .scale(scale);
      
      d3.select(legend)
          .call(colorLegend);
  }

  function handleTractClick(tract) {
      dispatch('selectTract', { tract });
  }

  function handleKeyDown(event, tract) {
      if (event.key === 'Enter' || event.key === ' ') {
          handleTractClick(tract);
      }
  }
</script>

<main>
  <svg {width} {height}>
      {#each data as d}
          <g tabindex="0"
             role="button"
             aria-label="Select tract"
             on:click={() => handleTractClick(d)}
             on:keydown={(event) => handleKeyDown(event, d)}
             style="cursor: pointer;">
              <path
                  style="fill: {scale(+d.properties.population)}"
                  d={path(d)} />
          </g>
      {/each}
      
      {#each fullData as d}
          <path class="geooverlay" d={path(d)} />
      {/each}

      <g transform="translate({width - 100}, 50)" bind:this={legend} />
  </svg>
</main>

<style>
  .geooverlay {
      stroke: grey;
      stroke-width: 1px;
      fill: none;
  }
</style>

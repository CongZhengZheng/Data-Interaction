<script>
  import * as d3 from 'd3';
  export let filteredData;
  let svg;
  let tooltip;

  let margin = { top: 50, right: 30, bottom: 200, left: 60 };
  let width = 1000 - margin.left - margin.right;
  let height = 600 - margin.top - margin.bottom;


  $: {
    if (filteredData && filteredData.length > 0) {
      console.log("Data received in Histogram:", filteredData);
      updateHistogram();
    } else {
      console.log("No data found");
    }
  }

  function updateHistogram() {

    let sortedData = [...filteredData]
      .sort((a, b) => b.UserRating - a.UserRating) 
      .slice(0, 100); 

    console.log("Number of items to plot:", sortedData.length);

    const svgElement = d3.select(svg)
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .html(''); 

    let x = d3.scaleBand()
      .domain(sortedData.map(d => d.Title))
      .range([0, width])
      .padding(0.1);

    let y = d3.scaleLinear()
      .domain([d3.min(sortedData, d => d.UserRating) -5, d3.max(sortedData, d => d.UserRating) + 0.5])
      .range([height, 0]);

    let bars = svgElement.selectAll("rect")
      .data(sortedData);

    bars.enter()
      .append("rect")
      .merge(bars)
      .attr("x", d => x(d.Title))
      .attr("width", x.bandwidth())
      .attr("y", d => y(d.UserRating))
      .attr("height", d => height - y(d.UserRating))
      .style("fill", "#6a5acd");

    bars.exit().remove();

    svgElement.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "rotate(-45) translate(-10, 0)")
      .style("text-anchor", "end");

    svgElement.append("g")
      .call(d3.axisLeft(y));
  }

  function handleMouseOver(event, d) {
    d3.select(event.currentTarget).style("fill", "yellow");
    tooltip.style("visibility", "visible")
           .html(`Title: ${d.Title}<br>Rating: ${d.UserRating}<br>Age Group: ${d.AgeGroupTargeted}<br>Price: ${d.Price}<br>Platform: ${d.Platform}`)
           .style("left", `${event.pageX + 10}px`)
           .style("top", `${event.pageY + 10}px`);
  }

  function handleMouseOut(event, d) {
    d3.select(event.currentTarget).style("fill", "#6a5acd");
    tooltip.style("visibility", "hidden");
  }
</script>

<svg bind:this={svg} width={width + margin.left + margin.right} height={height + margin.top + margin.bottom}></svg>
<div bind:this={tooltip} class="tooltip" style="position: absolute; visibility: hidden; background-color: white; padding: 10px; border: 1px solid #d3d3d3;"></div>

<style>
  .tooltip {
    position: absolute;
    text-align: center;
    padding: 8px;
    font: 12px sans-serif;
    background: white;
    border: solid 1px #aaa;
    border-radius: 8px;
    pointer-events: none;
    opacity: 0.9;
  }
</style>

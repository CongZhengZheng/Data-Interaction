<script>
  import * as d3 from 'd3';
  export let filteredData;
  export let selectedGameDetails;

  let svg;
  let tooltip;

  let margin = { top: 100, right: 30, bottom: 100, left: 30 };
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
      .domain([0, d3.max(sortedData, d => d.UserRating)])
      .range([height, 0]);

    // Update the x-axis
    svgElement.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "rotate(-45) translate(-10, 0)")
      .style("text-anchor", "end");

    // Update the y-axis
    svgElement.append("g")
      .call(d3.axisLeft(y));

    // Update bars
    svgElement.selectAll("rect")
      .data(sortedData, d => d.Title)
      .join(
        enter => enter.append("rect")
          .attr("x", d => x(d.Title))
          .attr("width", x.bandwidth())
          .attr("y", height)
          .attr("height", 0)
          .style("fill", "#6a5acd")
          .style("cursor", "pointer")
          .call(enter => enter.transition().duration(750)
            .attr("y", d => y(d.UserRating))
            .attr("height", d => height - y(d.UserRating))
          ),
        update => update
          .call(update => update.transition().duration(750)
            .attr("x", d => x(d.Title))
            .attr("width", x.bandwidth())
            .attr("y", d => y(d.UserRating))
            .attr("height", d => height - y(d.UserRating))
          ),
        exit => exit
          .call(exit => exit.transition().duration(750)
            .attr("y", height)
            .attr("height", 0)
            .remove()
          )
      )
      .on("click", (event, d) => {
        selectedGameDetails.set(`Title: ${d.Title}, 
                                Rating: ${d.UserRating},
                                Age Group Targeted: ${d.AgeGroupTargeted},
                                Price:${d.Price}, 
                                Platform:${d.Platform},
                                Required Special Device:${d.RequiresSpecialDevice},
                                Developer:${d.Developer},
                                Publisher:${d.Publisher},
                                Release Year:${d.ReleaseYear},
                                Genre:${d.Genre},
                                Multiplayer:${d.Multiplayer}, 
                                Game Length (Hours):${d.GameLength}, 
                                Graphics Quality: ${d.GraphicsQuality},
                                Soundtrack Quality: ${d.SoundtrackQuality},
                                Story Quality: ${d.StoryQuality}, 
                                Game Mode: ${d.GameMode},
                                Minimum Number of Players: ${d.MinNumberofPlayers}, 
                                User Review: ${d.UserReviewText}`);
      });
  }
</script>

<svg bind:this={svg} width={width + margin.left + margin.right} height={height + margin.top + margin.bottom}></svg>
<div bind:this={tooltip} class="tooltip" style="position: absolute; visibility: hidden; background-color: white; padding: 10px; border: 1px solid #d3d3d3;"></div>

<style>
  .tooltip {
    position: absolute;
    text-align: center;
    padding: 10px;
    font: 12px sans-serif;
    background: white;
    border: solid 2px #aaa;
    border-radius: 8px;
    pointer-events: none;
    opacity: 0.9;
  }
</style>

<script>
    import * as d3 from 'd3';
    export let filteredData = [];
    export let attribute;
  
    let svg;
    let margin = { top: 20, right: 20, bottom: 30, left: 50 };
    let width = 500 - margin.left - margin.right;
    let height = 300 - margin.top - margin.bottom;
  
    $: if (filteredData.length > 0 && attribute) {
        console.log("Updating chart with attribute:", attribute);
        console.log("Filtered Data:", filteredData);
        updateChart();
    }
  
    function updateChart() {
      let sums = {};
      filteredData.forEach(d => {
        let year = d.ReleaseYear;
        if (!sums[year]) sums[year] = { sum: 0, count: 0 };
        sums[year].sum += d[attribute];
        sums[year].count++;
      });
  
      let averages = Object.keys(sums).map(year => ({
        year: +year,
        average: sums[year].sum / sums[year].count
      }));
  
      d3.select(svg).selectAll('*').remove();
  
      let xScale = d3.scaleLinear()
        .domain(d3.extent(averages, d => d.year))
        .range([0, width]);
  
      let yScale = d3.scaleLinear()
        .domain([0, Math.ceil(d3.max(filteredData, d => d[attribute]))])
        .range([height, 0]);
  
      // Define the line
      let line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.average));
  
      let chart = d3.select(svg)
        .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);
  
      chart.append('path')
        .datum(averages)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 1)
        .attr('d', line);

        let dots = chart.selectAll(".dot")
    .data(averages)
    .enter()
    .append("g")
    .attr("class", "dot-group");

  dots.append("circle")
    .attr("class", "dot")
    .attr("cx", d => xScale(d.year))
    .attr("cy", d => yScale(d.average))
    .attr("r", 3)
    .style("fill", "#69b3a2")
    .style("cursor", "pointer");

  dots.append("text")
    .attr("x", d => xScale(d.year))
    .attr("y", d => yScale(d.average) - 10)
    .attr("text-anchor", "middle")
    .style("font-size", "8px")
    .style("visibility", "hidden")
    .style("fill", "white")
    .text(d => `${d.average.toFixed(2)}`);

  dots.on("click", function(event, d) {
    let isVisible = d3.select(this).select("text").style("visibility") === "visible";
    d3.selectAll(".dot-group text").style("visibility", "hidden"); // Hide all first
    d3.select(this).select("text").style("visibility", isVisible ? "hidden" : "visible");
  });

      chart.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.format("d")));
  
      chart.append('g')
        .call(d3.axisLeft(yScale));
    }
  </script>
  
  <svg bind:this={svg}></svg>
  
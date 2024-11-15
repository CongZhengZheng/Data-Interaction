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
      // Calculate averages for the selected attribute per year
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
  
      // Clear the previous chart content
      d3.select(svg).selectAll('*').remove();
  
      // Setup scales
      let xScale = d3.scaleLinear()
        .domain(d3.extent(averages, d => d.year))
        .range([0, width]);
  
      let yScale = d3.scaleLinear()
        .domain([0, d3.max(averages, d => d.average)])
        .range([height, 0]);
  
      // Define the line
      let line = d3.line()
        .x(d => xScale(d.year))
        .y(d => yScale(d.average));
  
      // Create the SVG container
      let chart = d3.select(svg)
        .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);
  
      // Draw the line
      chart.append('path')
        .datum(averages)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2)
        .attr('d', line);
  
      // Add the X and Y axes
      chart.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.format("d")));
  
      chart.append('g')
        .call(d3.axisLeft(yScale));
    }
  </script>
  
  <svg bind:this={svg}></svg>
  
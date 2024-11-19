<script>
    import * as d3 from 'd3';
  
    export let data = [];
    export let year;
  
    let svg;
    let margin = 40;
    let width = 700;
    let height = 600;
    let radius = Math.min(width, height) / 2 - margin;
  
    $: {

      if(data && data.length>0){
        console.log("Data Found")
      }else{
        console.log("No Data found")
      }
      
      let filteredData = data.filter(d => d.ReleaseYear === year);
  
      let developers = filteredData.reduce((acc, game) => {
        acc[game.Developer] = acc[game.Developer] || { sum: 0, count: 0 };
        acc[game.Developer].sum += game.UserRating;
        acc[game.Developer].count++;
        return acc;
      }, {});
  
      let averages = Object.entries(developers)
        .map(([key, value]) => ({
          developer: key,
          averageRating: value.sum / value.count
        }))
        .sort((a, b) => b.averageRating - a.averageRating)
        .slice(0, 10);
  
      renderPieChart(averages);
    }
  
    function renderPieChart(data) {
      const svgElement = d3.select(svg)
        .html('') 
        .attr('viewBox', `0 0 ${width} ${height}`)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);
  
      let color = d3.scaleOrdinal(d3.schemeCategory10);
      let pie = d3.pie().value(d => d.averageRating).sort((a, b) => b.averageRating - a.averageRating);
      let data_ready = pie(data);
      let arcGenerator = d3.arc().innerRadius(0).outerRadius(radius);
  
      svgElement
        .selectAll('path')
        .data(data_ready)
        .join('path')
        .attr('d', arcGenerator)
        .attr('fill', d => color(d.data.developer))
        .attr('stroke', 'white')
        .style('stroke-width', '2px')
        .style('opacity', 0.7);
  
      svgElement
        .selectAll('text')
        .data(data_ready)
        .join('text')
        .text(d => `${d.data.developer}: ${d.data.averageRating.toFixed(2)}`)
        .attr("transform", d => `translate(${arcGenerator.centroid(d)})`)
        .style("text-anchor", "middle")
        .style("fill", "white")
        .style("font-size", 8);

      let legend = d3.select(svg)
        .append("g")
        .attr("transform", `translate(${width - 120}, 30)`)
        .selectAll(".legend")
        .data(data_ready)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(0, ${i * 20})`);

      legend.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", d => color(d.data.developer));

      legend.append("text")
        .attr("x", 20)
        .attr("y", 10)
        .text(d => `${d.data.developer} (${d.data.averageRating.toFixed(2)})`)
        .style("font-size", "8px")
        .style("fill", "white")
        .style("text-anchor", "start");
}
    
  </script>
  
  <svg bind:this={svg}></svg>
  
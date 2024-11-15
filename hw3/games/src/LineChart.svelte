<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    export let data = [];

    function aggregateData(data) {
        const sumByYear = d3.rollup(data, v => d3.mean(v, d => d.Price), d => d.ReleaseYear);
        return Array.from(sumByYear, ([key, value]) => ({ ReleaseYear: key, AvgPrice: value }));
    }

    onMount(() => {
        const processedData = aggregateData(data);

        const svg = d3.select("#linechart");
        let margin = { top: 50, right: 30, bottom: 50, left: 60 };
        const width = 960 - margin.left - margin.right;
        const height = 500 - margin.top - margin.bottom;

        const x = d3.scaleLinear()
            .domain(d3.extent(processedData, d => d.ReleaseYear))
            .range([0, width]);
        const y = d3.scaleLinear()
            .domain([0, d3.max(processedData, d => d.AvgPrice)]).nice()
            .range([height, 0]);

        const g = svg.append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);

        // X axis
        g.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(d3.axisBottom(x).ticks(processedData.length).tickFormat(d3.format("d")));

        // Y axis
        g.append("g")
            .call(d3.axisLeft(y));

        // Define the line
        const line = d3.line()
            .x(d => x(d.ReleaseYear))
            .y(d => y(d.AvgPrice))
            .curve(d3.curveMonotoneX); 

 
        g.append("path")
            .datum(processedData) 
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("d", line);
    });
</script>

<svg id="linechart" width="960" height="500"></svg>


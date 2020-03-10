$(document).ready(function(){
	tail();
	bar();
});


function tail(){
	$("#tail").css("position","static");
}

function bar(){
	const margin = 60;
	const TW=992;
	const TH=400;
    const width = TW - 2 * margin;
    const height = TH - 2 * margin;
	//
    const svg = d3.select('svg#bar');
	svg.attr("width", TW)
	   .attr("height", TH);
	const chart = svg.append('g').attr('transform', 'translate('+margin+','+margin+')');
	//以定價為最高點
	const price_list=parseInt($("#price_list").text());
	const xScale = d3.scaleBand()
					 .range([0,width])
					 .domain(stores);	
	const yScale = d3.scaleLinear()
					 .range([height, 0])
					 .domain([0, price_list]);	
	chart.append('g').attr('transform', 'translate(0, '+height+')')
	                 .call(d3.axisBottom(xScale))
					 ; 
	chart.append('g').call(d3.axisLeft(yScale));					 
	//alert(2);
}
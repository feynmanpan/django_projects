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
    const width = TW;
    const height = TH - margin*2;
	//SVG
    const svg = d3.select('svg#bar');
	svg.attr("width", TW)
	   .attr("height", TH);
	//繪圖區   
	const chart = svg.append('g').attr('transform', 'translate('+margin/2+','+margin/2+')');
	//以定價為最高點
	//const price_list=parseInt($("#price_list").text());
	const xScale = d3.scaleBand()
					 .range([0,width])
					 .domain(stores_name)
					 .padding(0.95)
					 ;	
	const yScale = d3.scaleLinear()
					 .range([height, 0])
					 .domain([0, price_list])
					 ;	
	chart.append('g').attr('transform', 'translate(0, '+height+')')
	                 .call(d3.axisBottom(xScale))
					 ; 
	chart.append('g').call(d3.axisLeft(yScale));					 
	//紙本售價bar
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('rect')
		.attr('x', (b) => xScale(b.store_name)-5)
		.attr('y', (b) => yScale(b.price_sale))
		.attr('height', (b) => height-yScale(b.price_sale))
		.attr('width', xScale.bandwidth())	
		.attr('style', 'fill:rgb(210, 105, 30)')	
		;
	//電子書bar
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('rect')
		.attr('x', (b) => xScale(b.store_name)+5)
		.attr('y', (b) => yScale(b.price_sale_ebook))
		.attr('height', (b) => height-yScale(b.price_sale_ebook))
		.attr('width', xScale.bandwidth()*0.7)	
		.attr('style', 'fill:rgb(100, 149, 237)')	
		;				
	//紙本price
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('text')
		.text((b) => b.price_sale)
	    .attr("text-anchor", "middle")		
		.attr('x', (b) => xScale(b.store_name)+0)
		.attr('y', (b) => yScale(b.price_sale)-5)	
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "15px")
	    .attr("fill", "rgb(210, 105, 30)");		
		;	
	//ebook price
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('text')
		.text((b) => b.price_sale_ebook)
	    .attr("text-anchor", "start")		
		.attr('x', (b) => xScale(b.store_name)+13)
		.attr('y', (b) => yScale(b.price_sale_ebook)+10)	
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "13px")
	    .attr("fill", "rgb(100, 149, 237)");		
		;	
	
}
















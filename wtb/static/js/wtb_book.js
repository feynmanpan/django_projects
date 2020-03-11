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
					 .padding(0.9)
					 ;	
	const yScale = d3.scaleLinear()
					 .range([height, 0])
					 .domain([0, price_list])
					 ;	
	chart.append('g').attr('transform', 'translate(0, '+height+')')
	                 .call(d3.axisBottom(xScale))
					 ; 
	chart.append('g').call(d3.axisLeft(yScale));					 
	//BAR紙本售價
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('rect')
		.attr('x', (b) => xScale(b.store_name))
		.attr('y', (b) => yScale(b.price_sale))
		.attr('height', (b) => height-yScale(b.price_sale))
		.attr('width', xScale.bandwidth())	
		.attr('style', 'fill:rgb(210, 105, 30);cursor:pointer')
		.on("click", function(b,i){
			if(b.url_book!=""){	
				window.open(b.url_book, '_blank');     
			}
		})
		//.on("mouseover", function(b,i){
			//
		//})		
		.append('title')
		.text((b)=>Math.round(parseInt(b.price_sale)*100/price_list)+"折 : 前往"+b.store_name+"紙本商品頁")
		;
	function handleMouseOver(d,i){
		
	}
	//BAR電子書
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('rect')
		.attr('x', (b) => xScale(b.store_name)+5)
		.attr('y', (b) => yScale(b.price_sale_ebook))
		.attr('height', (b) => height-yScale(b.price_sale_ebook))
		.attr('width', xScale.bandwidth()*0.7)	
		.attr('style', 'fill:rgb(100, 149, 237);cursor:pointer')	
		.on("click", function(b,i){
			if(b.url_ebook!=""){
				window.open(b.url_ebook, '_blank');     
			}
		})
		.append('title')
		.text((b)=>Math.round(parseInt(b.price_sale_ebook)*100/price_list)+"折 : 前往"+b.store_name+"電子書商品頁")		
		;	
	//
	$('rect').hover(
		function(){
			var that=$(this);
			$('rect').css("opacity","0.5");
			that.css("opacity","1");
		},
		function(){
			var that=$(this);
			$('rect').css("opacity","1");
			//that.css("opacity","1");
		}		
	);
		
	//紙本price
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('text')
		.text((b) => b.price_sale)
	    .attr("text-anchor", "start")		
		.attr('x', (b) => xScale(b.store_name)-5)
		.attr('y', (b) => yScale(b.price_sale)-5)	
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "15px")
	    .attr("fill", "rgb(210, 105, 30)")	
		.attr('style', 'cursor:pointer')
		.on("click", function(b,i){
			if(b.url_book!=""){	
				window.open(b.url_book, '_blank')  
			}
		})	
		.append('title')
		.text((b)=>Math.round(parseInt(b.price_sale)*100/price_list)+"折 : 前往"+b.store_name+"紙本商品頁")
		;	
	//ebook price
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('text')
		.text((b) => b.price_sale_ebook)
	    .attr("text-anchor", "start")		
		.attr('x', (b) => xScale(b.store_name)+0)
		.attr('y', (b) => yScale(b.price_sale_ebook)+13)	
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "13px")
	    .attr("fill", "black")
		.attr('style', 'cursor:pointer')
		.on("click", function(b,i){
			if(b.url_ebook!=""){
				window.open(b.url_ebook, '_blank')    
			}
		})		
		.append('title')
		.text((b)=>Math.round(parseInt(b.price_sale_ebook)*100/price_list)+"折 : 前往"+b.store_name+"電子書商品頁")		
		;	
	//79折	
	chart.append('line')
        .attr('x1', 0)
        .attr('y1', height*(1-0.79))
        .attr('x2', width)
        .attr('y2', height*(1-0.79))
        .attr('stroke', 'red')
		.attr('stroke-width', '0.5px')
		//.attr('stroke-dasharray', '15,5')
		;
	//7折	
	chart.append('line')
        .attr('x1', 0)
        .attr('y1', height*(1-0.7))
        .attr('x2', width)
        .attr('y2', height*(1-0.7))
        .attr('stroke', 'red')
		.attr('stroke-width', '0.5px')
		.attr('stroke-dasharray', '5,5')
		;		
	//5折	
	chart.append('line')
        .attr('x1', 0)
        .attr('y1', height*(1-0.5))
        .attr('x2', width)
        .attr('y2', height*(1-0.5))
        .attr('stroke', 'green')
		.attr('stroke-width', '0.5px')
		;		
	//3折	
	chart.append('line')
        .attr('x1', 0)
        .attr('y1', height*(1-0.3))
        .attr('x2', width)
        .attr('y2', height*(1-0.3))
        .attr('stroke', 'blue')
		.attr('stroke-width', '0.5px')	
		;
}
















$(document).ready(function(){
	tail();
	bar();
});


function tail(){
	$("#tail").css("position","static");
}

function bar(){
	const margin = 60; 
	const TW=982;
	const TH=350;
    const width = TW;
    const height = TH - margin*2;
	//SVG
    const svg = d3.select('svg#bar');
	svg.attr("width", TW)
	   .attr("height", TH);
	//繪圖區   
	const chart = svg.append('g').attr('transform', 'translate('+(margin/2+5)+','+margin/2+')');
	//以定價為最高點
	//const price_list=parseInt($("#price_list").text());
	const xScale = d3.scaleBand()
					 .range([0,width])
					 .domain(store_names)
					 .padding(0.9)
					 ;	
	const yScale = d3.scaleLinear()
					 .range([height, 0])
					 .domain([0, price_list])
					 ;	
	chart.append('g').attr('transform', 'translate(0, '+height+')')
	                 .attr("id","x-axis") 
	                 .call(d3.axisBottom(xScale))
					 ; 
	chart.append('g').attr("id","y-axis")
	                 .call(d3.axisLeft(yScale))
					 ;		

	//x軸跳官網
	/*
	$("#x-axis text").click(function(){
		var that=$(this);
		var sname=that.text();
		var idx=store_names.indexOf(sname);
		//
		window.open(store_urls[idx], '_blank');  
	});
	*/	
	chart.selectAll('#x-axis .tick') 
		.data(store_names)
		.on("click", function(sn,i){
			var link=store_urls[i]
			window.open(link, '_blank');     			
		})		
		.append('title') 
		.text((sn)=>"前往"+sn+"官網")
		;	

	//BAR紙本售價
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('rect')
		.attr('class',(b) => b.store+" price")
		.attr('x', (b) => xScale(b.store_name)-4) 
		.attr('y', (b) => yScale(b.price_sale))
		.attr('height', (b) => height-yScale(b.price_sale))
		.attr('width', xScale.bandwidth())	
		.attr('style', 'fill:rgb(210, 105, 30);cursor:pointer')
		.on("click", function(b,i){
			if(b.url_book!=""){	
				window.open(b.url_book, '_blank');     
			}
		})	
		.append('title')
		.text((b)=>Math.round(parseInt(b.price_sale)*100/price_list)+"折 : 前往"+b.store_name+"紙本商品頁")
		;
	//BAR電子書
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('rect')
		.attr('class',(b) => b.store+" price")
		.attr('x', (b) => xScale(b.store_name)+10)
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

		
	//紙本price
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('text')
		.text((b) => b.price_sale)
		.attr('class',(b) => b.store+" price")
	    .attr("text-anchor", "start")		
		.attr('x', (b) => xScale(b.store_name)-8)
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
		.attr('class',(b) => b.store+" price")
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
		

	//
	$('.price').hover(
		function(){
			var that=$(this);
			var store=that.attr("class").replace(" price","");
			$('.price:not(.'+store+')').css("opacity","0.3");
		},
		function(){
			var that=$(this);
			$('.price').css("opacity","1");
		}		
	);
	//水平線=================================
	//100折	
	chart.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', width)
        .attr('y2', 0)
        .attr('stroke', 'black')
		.attr('stroke-width', '0.5px')
		//.attr('stroke-dasharray', '15,5')
		;
	chart.append('text')
		.text('定價'+price_list)
	    .attr("text-anchor", "start")		
		.attr('x', 2)
		.attr('y', -2)		
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "10px")
	    .attr("fill", "black")
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
	chart.append('text')
		.text('79折')
	    .attr("text-anchor", "start")		
		.attr('x', 2)
		.attr('y', height*(1-0.79)-2)		
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "10px")
	    .attr("fill", "red")
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
	chart.append('text')
		.text('7折')
	    .attr("text-anchor", "start")		
		.attr('x', 2)
		.attr('y', height*(1-0.7)-2)		
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "10px")
	    .attr("fill", "red")
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
	chart.append('text')
		.text('5折')
	    .attr("text-anchor", "start")		
		.attr('x', 2)
		.attr('y', height*(1-0.5)-2)		
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "10px")
	    .attr("fill", "green")
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
	chart.append('text')
		.text('3折')
	    .attr("text-anchor", "start")		
		.attr('x', 2)
		.attr('y', height*(1-0.3)-2)		
	    .attr("font-family", "sans-serif")
	    .attr("font-size", "10px")
	    .attr("fill", "blue")
		;		
}















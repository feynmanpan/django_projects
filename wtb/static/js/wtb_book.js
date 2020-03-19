$(document).ready(function(){
	taaze_vdo_handle();
	tail();
	bar();
});

function taaze_vdo_handle(){
		
	if(taaze_vdo!=""){

		
		var vdo=$("#info_listp").find('video#vdo');
		var vdo_btn=$('#vdo_btn');
		var vdo_close=$('#vdo_close');
		//
		var m=window.matchMedia('(max-width: 992px)').matches;		
		if(m==true){

		}		
		//
		vdo.attr('src',taaze_vdo);
		vdo_btn.show();		
		//顯示影片
		vdo_btn.find('img,span:first').click(function(){
			vdo.show().get(0).play();	
			vdo_close.show();
		});
		//隱藏影片
		vdo_close.click(function(){
			vdo.hide().get(0).pause();	
			vdo_close.hide();
		});
		$(document).on('keyup',function(evt) {
			//ESC
			if (evt.keyCode == 27) {
				vdo_close.trigger('click');
			}
		});		
		
	};//if
}


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
	//
	var m=window.matchMedia('(max-width: 992px)').matches;		
	if(m==true){		
		svg.attr("width", "100%")
		   .attr("height", "auto");
	}else{
		svg.attr("width", TW)
		   .attr("height", TH);			
	}	  
	//
	$(window).resize(function() {
		var m=window.matchMedia('(max-width: 992px)').matches;		
		if(m==true){		
			svg.attr("width", "100%")
			   .attr("height", "auto");
		}else{
			svg.attr("width", TW)
			   .attr("height", TH);			
		}
	});	
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
	//加強讀冊顏色
	$(".tick text:Contains('讀冊')").attr('fill','#e3007f').css('font-weight','bold');
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
	//針對茉莉處理
	//提示
	function title_handle(b){
		if(b.store!='mollie'){
			return Math.round(parseInt(b.price_sale)*100/price_list)+"折 : 前往"+b.store_name+"紙本商品頁"
		}else{
			return b.stock+'有庫存，點我聯絡'
		}//if
	}	
	//價錢文字
	function text_handle(b){
		if(b.store!='mollie'){
			return b.price_sale
		}else{
			if(b.price_sale==price_list){
				//顯示庫存分店
				//alert(b.stock);
				return b.stock.replace(/店/g,'')
			}else{
				return ''
			}
		}//if		
	}
	
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
			};
			/*
			if(b.store=='mollie'){
				if(b.price_sale==price_list){
					window.open(b.url_book, '_blank'); //前往分店
				}
			};
			*/
		})	
		.append('title')
		//.text((b)=>Math.round(parseInt(b.price_sale)*100/price_list)+"折 : 前往"+b.store_name+"紙本商品頁")
		.text(title_handle)
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

		
	//文字:紙本price
	chart.selectAll()
		.data(bookprices)
		.enter()
		.append('text')
		//.text((b) => b.price_sale)
		.text(text_handle)
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
		//.text((b)=>Math.round(parseInt(b.price_sale)*100/price_list)+"折 : 前往"+b.store_name+"紙本商品頁")
		.text(title_handle)
		;	
	//茉莉店名位置處理
	$("text.mollie.price")
		.attr('text-anchor','middle')
		.attr("font-size", "12px")
		.css('font-weight','bolder')
		.css('font-family','微軟正黑體')
		;
		
	//文字:ebook price
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
















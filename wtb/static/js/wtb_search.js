
$(document).ready(function(){ 
	//autocomplete
	$("#kw_input").autocomplete({
		source: function( request, response ) {
			$.ajax({   
				type: "get",
				url: "/autocom/",
				timeout:1000*30,
				data:{kw:request.term},
				dataType: "json", 
				async:true,
			})
			.done(function(data){
				response(
					$.map(
						//data.suggestions,//biggo 
						data,//taaze_elite 
						function (item){   
							return item.substr(0,33) 
							//return item['value'].substr(0,33) //elite
						}
					)//map
				);
			});//ajax
		}//source
	});		
	//關閉搜尋結果
	$('#close').click(function(){
		$("#result").slideUp("slow");
		$("body").css('overflow','visible');
	});
	
	$(document).on('keyup',function(evt) {
		//ESC
		if (evt.keyCode == 27) {
			$('#close').trigger('click');
		}
	});
	


	$("#kw_input").keyup(function(event) {
		// Number 13 is the "Enter" key on the keyboard
		if (event.keyCode === 13 && $("#kw_submit").is(":visible")) {
			// Cancel the default action, if needed
			event.preventDefault();
			// Trigger the button element with a click
			$("#kw_submit").trigger('click');
		}
	});

	//開始搜尋
	$("#kw_submit").click(function(){
		var kw=$("#kw_input").val().trim();
		if(kw==''){
			alert('請輸入關鍵字');
			return false;
		}
		//放大鏡切換
		var that=$(this);
		var ing=$('#ing');
		that.hide();
		ing.show().data('show','Y');
		var stime=Date.now();
		//==============================================
		//若已搜過此kw	
		var item_kw=$(".item[data-kw='"+kw+"']");//要加單引號，有些kw有點 . 會出錯
		var item_notkw=$(".item").not(item_kw);
		
		if(item_kw.length>0){			
			item_notkw.hide();			
			item_kw.show();
			//
			$("#kw").text(kw);
			$("#resultn").text(item_kw.length);
			$("body").css('overflow','hidden');			
			//
			$("#result").slideDown("slow").scrollTop(0);	
			ing.hide().data('show','N');
			that.show();
			//
			var etime=Date.now();
			D=(etime-stime)/1000;
			$("#process_time span").text(D).attr('data-from','local');
			//
			return false;
		}
		//==============================================
		//此kw沒搜過，重打ajax
		$.ajax({   
			type: "get",
			url: "/search/",
			timeout:1000*30,
			data: {kw:kw},//"kw="+kw,
			dataType: "json", 
			async:true,
		})
		.fail(
			function(err){ 
				alert('爬蟲失敗，請重新按一次查詢，sorry');
				//
				//ing.hide().data('show','N');
				//that.show();					
			}//
		)//fail
		.done(
			function(data){

				var n=data.length;
				if(n==0){
					alert("無搜尋結果，請重新查詢");
					//
					//ing.hide().data('show','N');
					//that.show();										
					//alert(1);
					return false;
				}
				//alert(2);
				//______________________________________
				//$(".item").remove();
				item_notkw.hide();
				//
				$("#kw").text(kw);
				$("#resultn").text(n);					
				$("body").css('overflow','hidden');
				//$("#result").slideDown("slow");
				//
				var result=$("#result");
				var forcopy=result.find(".itemcopy");
				for (var i = 0; i < n; i++) {
					var item_data=data[i];
					var item=forcopy.clone();
					//
					item.removeClass("itemcopy").addClass("item");
					item.attr("title","前往本書比價頁面");
					item.find("a").attr("href","/book/"+item_data['bookid']);
					item.data('bookid',item_data['bookid'])
						.data('kw',kw)
						.attr('data-bookid',item_data['bookid'])
						.attr('data-kw',kw)
						;
					item.find('img').attr('src',item_data['src']);
					item.find('.title>strong').text(item_data['title']);
					item.find('.author').text(item_data['author']);
					item.find('.publisher').text(item_data['publisher']);
					item.find('.pub_dt').text(item_data['pub_dt']);
					item.find('.price_list>span').text(item_data['price_list']);
					item.find('.intro').text(item_data['intro']==""?"無簡介":item_data['intro']);
					//	
					item.appendTo(result);
				};//for
				$("#result").slideDown("slow").scrollTop(0); 

				//ing.hide().data('show','N');
				//that.show();

			}//success
		)//done
		.always(
			function(){
				ing.hide().data('show','N');
				that.show();	
				//alert(1);
				var etime=Date.now();
				D=(etime-stime)/1000;
				$("#process_time span").text(D).attr('data-from','server');				
			}
		)//always
	});//click
	
});//ready
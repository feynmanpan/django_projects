
$(document).ready(function(){ 
	//關閉搜尋結果
	$('#close').click(function(){
		$("#result").slideUp("slow");
		$("body").css('overflow','visible');
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
		//
		var that=$(this);
		var ing=$('#ing');
		that.hide();
		ing.show().data('show','Y');
		//		
		//
		$.ajax({   
			type: "get",
			url: "/search/",
			timeout:1000*30,
			data: "kw="+kw,
			dataType: "json", 
			async:true,
			error: function(err){ 
				alert('爬蟲失敗，請重新按一次查詢，sorry');
				//
				ing.hide().data('show','N');
				that.show();					
			},
			success: function(data){
				//alert(data.length);
				//alert(data[0]['title'])
				//$("#result").text(data); 					
				//
				var n=data.length;
				if(n==0){
					alert("無搜尋結果，請重新查詢");
					//
					ing.hide().data('show','N');
					that.show();										
					return false;
				}
				if($(".item").length>0){
					$(".item").remove();						
					//$("#result").slideUp("fast");						
				}else{
					//$("body").css('overflow','hidden');
				};
					
				$("body").css('overflow','hidden');
				$("#result").slideDown("slow");
				$("#kw").text(kw);
				$("#resultn").text(n);
				//
				var result=$("#result");
				var forcopy=result.find(".itemcopy");
				for (var i = 0; i < n; i++) {
					var item_data=data[i];
					var item=forcopy.clone();
					//
					item.removeClass("itemcopy").addClass("item");
					item.attr("title","前往本書比價頁面");
					item.find("a").attr("href","/book/"+item_data['bookid'])
					item.data('bookid',item_data['bookid']);
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
				//$("#result").slideDown("slow");
				ing.hide().data('show','N');
				that.show();

			}//success
		});//ajax
	});//click
	
});//ready
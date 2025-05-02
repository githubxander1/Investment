$(function(){

	$('.share_btn').click(function(){
		var scroll_top = $(document).scrollTop();
		var h = scroll_top+"px";
		$('#box_share').animate({'top':h},500);

		var dta_url = $(this).attr("data-url");
		var sub_name = $(this).attr("data-name");
		var img_url =  $(this).attr("data-img");
		jiathis_config = {
			 	title:sub_name,
			    url:dta_url,
			    pic:img_url
			};
	});
	
	$('.qrcode_btn').click(function(){
		var scroll_top = $(document).scrollTop();
		var h = scroll_top+"px";
		$('#box_share').animate({'top':h},500);

		var dta_url = $(this).attr("data-url");
		var sub_name = $(this).attr("data-name");
		var img_url =  $(this).attr("data-img");
		jiathis_config = {
			 	title:sub_name,
			    url:dta_url,
			    pic:img_url
			};
	});
	
	
	
	$('#boxclose_share').click(function(){
		$('#box_share').animate({'top':'-400px'},500);
	});

	$(window).scroll(function(){
		$('#box_share').animate({'top':'-400px'},500);
	});
	
	$(".my_mall").bind("click",function(){
		if($(this).attr("init")==1){
			$(this).attr("init",0);
			$(".my_mall_qrcode").animate({'right':'-247px'},500);
		}else{
			
			$(this).attr("init",1);
			$(".my_mall_qrcode").animate({'right':'120px'},500);
		}
		
		
	});
	
	
	
});

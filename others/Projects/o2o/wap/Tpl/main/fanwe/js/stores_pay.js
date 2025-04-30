$(document).ready(function(){
	init_dp_star();
});



/**
 * 点评星星初始化
 */
function init_dp_star(){
	$(".stars").each(function(i,stars){
		var avg_point = $(stars).attr("data"); //评分
		var start_cut = parseInt(avg_point);	//选中的星星数
		var start_half = '';	//小数点后的分数
		var half_width = 0;	//有小数的星星百分百宽度
		
	 
		if(avg_point.indexOf(".")>0){
			start_half = "0"+avg_point.substring(avg_point.indexOf("."),avg_point.length);
			half_width = (parseFloat(start_half)*100).toFixed(1);
		}
		 
		if(avg_point>=1)
			$(stars).find(".text-icon:lt("+start_cut+")").addClass("main_color");
		else
			$(stars).find(".text-icon").removeClass("icon-star").addClass("icon-star-gray");
		
		if(start_half.length>0){
			$(stars).find(".text-icon").eq(avg_point).html('<i style="width:'+half_width+'%;" class="text-icon icon-star icon-star-half">&#xe67f</i>&#xe67f');
			$(stars).find(".text-icon").eq(avg_point).css("position", "relative");
		}
	});
	
}


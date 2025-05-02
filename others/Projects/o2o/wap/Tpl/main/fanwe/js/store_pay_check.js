/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(function(){

    init_payment_input();
    init_pay_btn();

});

function init_payment_input(){
    $("input[name='payment'],input[name='all_account_money'] ").bind("click",function(){
        count_buy_total();
    });   
}



function count_buy_total()
{
	ajaxing = true;
	var query = new Object();
	
	//全额支付
	if($("input[name='all_account_money']").attr("checked"))
	{
		query.all_account_money = 1;
	}
	else
	{
		query.all_account_money = 0;
	}

	
	//支付方式
	var payment = $("input[name='payment']:checked").val();
	if(!payment)
	{
		payment = 0;
	}
	query.payment = payment;
        query.order_id = order_id;
	query.bank_id = $("input[name='payment']:checked").attr("rel");
	
	if(!isNaN(order_id)&&order_id>0)
		query.act = "count_store_pay_total";
	else
		query.act = "check";
	
	
	$.ajax({ 
		url: custom_ajax_url,
		data:query,
		type: "POST",
		dataType: "json",
		success: function(data){
	
			if(data.status == -1)
			{  //未登录，请先登录
				$.showErr("未登录，请先登录",function(){location.href=login_url;});
				
			}

			if(data.pay_price == 0)
			{
				$("input[name='payment']").attr("checked",false);
			}
	        if(data.pay_price>0){
	            $(".pay_btn").val("确认支付：￥"+data.pay_price);
	            
	        }else{
	            $(".pay_btn").val("确认支付");
	        }
            
	        $(".pay_info").html(data.html);
                        
			ajaxing = false;
		},
		error:function(ajaxobj)
		{
//			if(ajaxobj.responseText!='')
//			alert(LANG['REFRESH_TOO_FAST']);
		}
	});
        
}
function init_pay_btn(){
    $(".pay_btn").bind("click",function(){
        var payment = $("input[name='payment']:checked").val();
        var bank_id=0;
        if(payment>0 || $("input[name='all_account_money']").attr("checked")=="checked"){
            if(!ajaxing)
            {
            	var query = new Object();
            	if($("input[name='all_account_money']").attr("checked"))
            	{
            		query.all_account_money = 1;
            	}
            	else
            	{
            		query.all_account_money = 0;
            	}
                query.order_id = order_id;
                query.bank_id = bank_id;
                query.payment = payment;
                query.act = "done";
                
                $.ajax({
                        url:custom_ajax_url,
                        data:query,
                        type:"POST",
                        dataType:"json",
                        success:function(data){
                        	if(data.status==1){
                				location.href=data.jump;
                			}else{
                				$.showErr(data.info,0,data.jump);
                			}

                        }			
                });
            }
        }else{
             alert("请选择支付方式");
        }
    });
//    $(".pay-form").bind("submit",function(){
//        alert(".pay_btn").val();
//        return false;
//    });
}
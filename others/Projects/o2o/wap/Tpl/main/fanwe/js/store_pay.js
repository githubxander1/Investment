/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(function(){
    init_money_change();
    init_payment_input();
    init_pay_btn();
    count_discount();
    order_submit();
});

function order_submit(){
    $(".sub_btn").bind("click",function(){
        var query=$("#submit_dp").serialize();
        var url=$("#submit_dp").attr('action');
        
        $.ajax({ 
    		url: url,
    		data:query,
    		type: "POST",
    		dataType: "json",
    		success: function(data){
    			if(data.status==1){
    				location.href=data.jump;
    			}else{
    				$.showErr(data.info);
    			}
    		},

    	});
            
        

    });
}


function init_money_change(){
    $("input[name='money']").bind({"keyup":function(event){
        count_discount();
    },"blur":function(){
    	//count_discount();
    }});
}

function init_payment_input(){
    $("input[name='payment'],input[name='all_account_money'] ").bind("click",function(){
        count_buy_total();
    });   
}

/**
 * 计算促销优惠金额
 * @param {float} money
 */
function count_discount(){
	
    var money = parseFloat($("input[name='money']").val()); 
    if(isNaN(money)){
    	money=0;
    }
    //if(money > 0){
    	
  
          var query = new Object();
          query.act='promote';
          
          query.location_id=location_id;
          query.money=money;
        $.ajax({ 
    		url: custom_ajax_url,
    		data:query,
    		type: "POST",
    		dataType: "json",
    		success: function(data){

    			if(data.promote){
        			$.each(data.promote,function(index,obj){
        				
        				$(".promote_id_"+obj.id).find("span").html(obj.discount_price);
        			});
        	        //计算后的结果
    			}

    	        $(".pay_amount").find("span").html("&yen;"+(data.pay_price));
    	        
    		}
        });

    //} 

    
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
			if(data.pay_price == 0)
			{
				$("input[name='payment']").attr("checked",false);
			}
                        if(data.pay_price>0){
                            $(".pay_btn").val("确认支付：￥"+data.pay_price);
                            
                        }else{
                            $(".pay_btn").val("确认支付");
                        }
                        
                        
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
        if(payment>0 || $("input[name='all_account_money']").attr("checked")=="checked"){
            if(!ajaxing)
            {
                var query = new Object();
                query.order_id = order_id;
                query.act = "done";
                $.ajax({
                        url:custom_ajax_url,
                        data:query,
                        type:"POST",
                        dataType:"json",
                        success:function(obj){
                                if(obj.status)
                                {
                                        //有支付方式的情况下
                                        $(".pay-form").attr("action",data.payment_code.pay_action);
                                }
                                else
                                {

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
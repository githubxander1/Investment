var lesstime = 0;
$(document).ready(function () {
	init_bank();
	
	$(".bank").bind("click",function(){
		$(".bank span").removeClass("checked");
		$(this).find("span").addClass("checked");
		init_bank();		
	});
	
	init_sms_btn($("#uc_sms_btn"));
	$("#uc_sms_btn").bind("click",function(){
		do_send($("#uc_sms_btn"));
	});
	
	
	$("form[name='add_card']").bind("submit",function(){		
		var bank_name = $("form[name='add_card']").find("input[name='bank_name']").val();
		var bank_account = $("form[name='add_card']").find("input[name='bank_account']").val();
		var bank_user = $("form[name='add_card']").find("input[name='bank_user']").val();
		var sms_verify = $("form[name='add_card']").find("input[name='sms_verify']").val();		
		if($.trim(bank_name)=="")
		{
			$.showErr("请输入开户行名称");
			return false;
		}
		if($.trim(bank_account)=="")
		{
			$.showErr("请输入开户行账号");
			return false;
		}
		if($.trim(bank_user)=="")
		{
			$.showErr("请输入开户人真实姓名");
			return false;
		}
		if($.trim(sms_verify)=="")
		{
			$.showErr("请输入短信验证码");
			return false;
		}
		
		var ajax_url = $("form[name='add_card']").attr("action");
		var query = $("form[name='add_card']").serialize();
		$.ajax({
			url:ajax_url,
			data:query,
			dataType:"json",
			type:"POST",
			success:function(obj){
				if(obj.status==1){
					$.showSuccess("保存成功",function(){
						location.href = obj.url;
					});					
				}else if(obj.status==0){
					if(obj.info)
					{
						$.showErr(obj.info,function(){
							if(obj.url) location.href = obj.url;
						});
					}
					else
					{
						if(obj.url)location.href = obj.url;
					}
					
				}else{
					
				}
			}
		});		
		return false;
	});	

	
	$("form[name='withdraw']").bind("submit",function(){		
		var bank_id = $("form[name='withdraw']").find("input[name='bank_id']").val();
		var money = $("form[name='withdraw']").find("input[name='money']").val();
		var pwd = $("form[name='withdraw']").find("input[name='pwd']").val();
		if($.trim(pwd)=="")
		{
			$.showErr("请输入登录密码");
			return false;
		}

		if($.trim(bank_id)==""||isNaN(bank_id)||parseFloat(bank_id)<=0)
		{
			$.showErr("请选择提现账户");
			return false;
		}
		if($.trim(money)==""||isNaN(money)||parseFloat(money)<=0)
		{
			$.showErr("请输入正确的提现金额");
			return false;
		}
		
		var ajax_url = $("form[name='withdraw']").attr("action");
		var query = $("form[name='withdraw']").serialize();
		$.ajax({
			url:ajax_url,
			data:query,
			dataType:"json",
			type:"POST",
			success:function(obj){
				if(obj.status==1){
					$.showSuccess("提现申请成功，请等待管理员审核",function(){
						if(obj.url)location.href = obj.url;
					});					
				}else if(obj.status==0){
					if(obj.info)
					{
						$.showErr(obj.info,function(){
							if(obj.url) location.href = obj.url;
						});
					}
					else
					{
						if(obj.url)location.href = obj.url;
					}
					
				}else{
					
				}
			}
		});		
		return false;
	});		
	
 });

function init_bank(){
	var bank_name=$(".bank").find(".checked").attr("bank_name");
	var bank_id=$(".bank").find(".checked").attr("rel");
	$("input[name='bank_name']").val(bank_name);
	$("input[name='bank_id']").val(bank_id);
}



function do_send(btn)
{
   var account = $(btn).attr("account");
   
	if($.trim($("#mobile").val())=="" && account!=1)
	{
		$.showErr("请输入手机号码");
		return false;
	}
	
	if(lesstime>0)return;
	var query = new Object();
	query.mobile = $("#mobile").val();
	query.act = "send_sms_code";
	query.unique = $(btn).attr("unique");
    query.account = account;
	query.verify_code = (btn).attr("verify_code");
	$.ajax({
		url:AJAX_URL,
		data:query,
		type:"POST",
		dataType:"json",
		success:function(obj){
			if(obj.status==1)
			{
				$(btn).attr("lesstime",obj.lesstime);
				init_sms_btn(btn);
				$.showSuccess(obj.info);
				
			}
			else
			{
				if(obj.status==-1)
				{
							$("#verify_image_box .verify_form_box .verify_content").html("");
		                    var html_str = '<div class="v_input_box"><input type="text" class="v_txt" placeholder="图形码" id="verify_image"/><img src="'+obj.verify_image+"&r="+Math.random()+'"  /></div>'+
		                                    '<div class="blank"></div><div class="blank"></div>'+
		                                    '<div class="v_btn_box"><input type="button" class="v_btn" name="confirm_btn" value="确认"/></div>';
		                    $("#verify_image_box .verify_form_box .verify_content").html(html_str);
		                    $("#verify_image_box").show();
							
							$("#verify_image_box").find("img").bind("click",function(){
								$(this).attr("src",obj.verify_image+"&r="+Math.random());
							});
							$("#verify_image_box").find("input[name='confirm_btn']").bind("click",function(){
								var verify_code = $.trim($("#verify_image_box").find("#verify_image").val());
								if(verify_code=="")
								{
									$.showErr("请输入图形验证码");
								}
								else
								{
									$(btn).attr("verify_code",verify_code);
									$("#verify_image_box .verify_form_box .verify_content").html("");
							                                    $("#verify_image_box").hide();
							                                    do_send(btn);
							                                    
								}
							});
							if($(btn).attr("verify_code")&&$(btn).attr("verify_code")!="")
							{
								$.showErr(obj.info,function(){
									$(btn).attr("verify_code","")
								});
							}
				}
				else
				{
					$.showErr(obj.info);
				}
				
			}
		}
	});
}


//关于短信验证码倒计时
function init_sms_btn(btn)
{
	$(btn).stopTime();
	$(btn).everyTime(1000,function(){
		lesstime = parseInt($(btn).attr("lesstime"));
		lesstime--;
		$(btn).val("重新获取("+lesstime+")");
		$(btn).attr("lesstime",lesstime);
		 
		if(lesstime<=0 || $(btn).attr("lesstime") == 'NaN')
		{
			$(btn).stopTime();
			$(btn).val("获取验证码");
		}
	});
}
$(document).ready(function(){
	
	$("#sub_address").bind("click",function(){
		$("#withdraw form").submit();
	});
	
	
	$("#withdraw form").bind("submit",function(){
		
		var bank_name = $("#withdraw form").find("input[name='bank_name']").val();
		var bank_account = $("#withdraw form").find("input[name='bank_account']").val();
		var bank_user = $("#withdraw form").find("input[name='bank_user']").val();
		var money = $("#withdraw form").find("input[name='money']").val();
		var type = $("#withdraw form").find("select[name='type']").val();
		
		if($.trim(bank_name)==""&&type==1)
		{
			$.showErr("请输入开户行名称");
			return false;
		}
		if($.trim(bank_account)==""&&type==1)
		{
			$.showErr("请输入开户行账号");
			return false;
		}
		if($.trim(bank_user)==""&&type==1)
		{
			$.showErr("请输入开户人真实姓名");
			return false;
		}
		if($.trim(money)==""||isNaN(money)||parseFloat(money)<=0)
		{
			$.showErr("请输入正确的提现金额");
			return false;
		}
		
		var ajax_url = $("#withdraw form").attr("action");
		var query = $("#withdraw form").serialize();
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
							if(obj.url)
								location.href = obj.url;
						});
					}
					else
					{
						if(obj.url)
							location.href = obj.url;
					}
					
				}else{
					
				}
			}
		});
		
		
		return false;
	});
	
	
	$("select[name='type']").bind("change",function(){
		if($("select[name='type']").val()==1){
			$('.bank').show();
		}else{
			$('.bank').hide();
		}
	});
	
	
	
	//关于手机号的验证码绑定
	init_bind_sms_btn();
	//绑定按钮事件
	init_sms_btn();
	//初始化倒计时
	function init_sms_btn() {
		$("#withdraw").find("button.ph_verify_btn[init_sms!='init_sms']").each(function(i, o) {
			$(o).attr("init_sms", "init_sms");
			var lesstime = $(o).attr("lesstime");
			var divbtn = $(o).next();
			divbtn.attr("lesstime", lesstime);
			if(parseInt(lesstime) > 0)
				init_sms_code_btn($(divbtn), lesstime);
		});
	}
	function init_bind_sms_btn() {
		if(!$("#withdraw").find("div.ph_verify_btn").attr("bindclick")) {
			$("#withdraw").find("div.ph_verify_btn").attr("bindclick", true);
			$("#withdraw").find("div.ph_verify_btn").bind("click", function() {
				if($(this).attr("rel") == "disabled")
					return false;
				var btn = $(this);
				var query = new Object();
				query.act = "send_fxsms_code";
				query.account = 1;
				query.no_verify = 1;
				//发送手机验证登录的验证码
				$.ajax({
					url : AJAX_URL,
					dataType : "json",
					data : query,
					type : "POST",
					global : false,
					success : function(data) {
						if(data.status) {
							init_sms_code_btn(btn, data.lesstime);
							IS_RUN_CRON = true;							
						} else {
							$.showErr(data.info,function(){
								if(data.jump)
								{
									location.href = data.jump;
								}
							});
						}
					}
				});
			});
		}

	}
});
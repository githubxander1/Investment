function do_is_effect(deal_id,obj){
	var query = new	Object();
	query.deal_id = deal_id;
	query.act = 'do_is_effect';
	$.showConfirm("确定"+$(obj).html()+"吗？",function(){
		$.ajax({
			url:ajax_url,
			data:query,
			type:"POST",
			dataType:"json",
			success:function(obj){
				if(obj.status)
				{
					if(obj.user_login_status!=1)
					{
						location.href = obj.jump;
					}
					else
					{
						$.showSuccess(obj.info,function(){
							location.reload();
						});
					}
					
				}
				else
				{
					if(obj.info)
					{
						$.showErr(obj.info,function(){
							location.reload() ;
							});
					}
					else
					{
						location.reload() ;
					}
					
				}
			}			
		});
	});
	
	return false;
}

function del_user_deal(deal_id,obj){
	var query = new	Object();
	query.deal_id = deal_id;
	query.act = 'del_user_deal';
	$.showConfirm("确定删除你的这个分销吗？",function(){
		$.ajax({
			url:fx_ajax_url,
			data:query,
			type:"POST",
			dataType:"json",
			success:function(obj){
				if(obj.status)
				{
					if(obj.user_login_status!=1)
					{
						location.href = obj.jump;
					}
					else
					{
						$.showSuccess(obj.info,function(){
							location.reload();
						});
					}
					
				}
				else
				{
					if(obj.info)
					{
						$.showErr(obj.info,function(){
							location.reload();
							});
					}
					else
					{
						location.reload();
					}
					
				}
			}			
		});
	});
	
	return false;
}

function add_user_fx_deal(deal_id,obj){
	var query = new	Object();
	query.deal_id = deal_id;
	query.act = 'add_user_fx_deal';
	$.ajax({
		url:fx_ajax_url,
		data:query,
		type:"POST",
		dataType:"json",
		success:function(obj){
			if(obj.status)
			{
				if(obj.user_login_status!=1)
				{
					location.href = obj.jump;
				}
				else
				{
					$.showSuccess(obj.info,function(){
						location.reload();
					});
				}
				
			}
			else
			{
				if(obj.info)
				{
					$.showErr(obj.info,function(){
						location.reload();
						});
				}
				else
				{
					location.reload();
				}
				
			}
		}			
	});
	return false;
}
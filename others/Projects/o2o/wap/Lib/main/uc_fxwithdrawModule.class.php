<?php
// +----------------------------------------------------------------------
// | Fanwe 方维o2o商业系统
// +----------------------------------------------------------------------
// | Copyright (c) 2014 http://www.fanwe.com All rights reserved.
// +----------------------------------------------------------------------
// | Author: 云淡风轻(97139915@qq.com)
// +----------------------------------------------------------------------

class uc_fxwithdrawModule extends MainBaseModule
{

	public function index()
	{
		global_run();		
		init_app_page();
		

		
		$param=array();	
		$param['page'] = intval($_REQUEST['page']);	
		$data = request_api("uc_fxwithdraw","index",$param);
		
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
			app_redirect(wap_url("index","user#login"));
		}
		
		if(isset($data['page']) && is_array($data['page'])){			
			$page = new Page($data['page']['data_total'],$data['page']['page_size']);   //初始化分页对象			
			$p  =  $page->show();
			
			$GLOBALS['tmpl']->assign('pages',$p);
		}
		$GLOBALS['tmpl']->assign("sms_lesstime",load_sms_lesstime());
		
		//print_r($data);exit;
		$GLOBALS['tmpl']->assign("data",$data);	
		$GLOBALS['tmpl']->display("uc_fxwithdraw.html");
	}
	

	

	public function save()
	{
		global_run();
		$param=array();
		
		$param['sms_verify'] = intval($_REQUEST['sms_verify']);
		$param['money'] = floatval($_REQUEST['money']);
		$param['type'] = intval($_REQUEST['type']);

		$param['bank_name'] = strim($_REQUEST['bank_name']);
		$param['bank_account'] = strim($_REQUEST['bank_account']);
		$param['bank_user'] = strim($_REQUEST['bank_user']);

		$data = request_api("uc_fxwithdraw","save",$param);
 		//print_r($data);exit;
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
			$result['status'] = 0;
			$result['info'] = "";
			$result['url'] = wap_url("index","user#login");
			ajax_return($result);
		}else{
			if($data['status']==0){
					$result['status'] = 0;
					$result['info']=$data['info'];
					ajax_return($result);	
			}elseif($data['status']==1){
					$result['status'] = 1;

					$result['url'] = wap_url("index","uc_fxwithdraw");
					ajax_return($result);					
			}
		}
		
		

	}


}
?>
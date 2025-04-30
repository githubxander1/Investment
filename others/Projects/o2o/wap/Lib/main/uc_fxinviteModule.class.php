<?php
// +----------------------------------------------------------------------
// | Fanwe 方维o2o商业系统
// +----------------------------------------------------------------------
// | Copyright (c) 2014 http://www.fanwe.com All rights reserved.
// +----------------------------------------------------------------------
// | Author: 云淡风轻(97139915@qq.com)
// +----------------------------------------------------------------------

class uc_fxinviteModule extends MainBaseModule
{

	public function index()
	{
		global_run();		
		init_app_page();
		
		$param=array();	
		$param['page'] = intval($_REQUEST['page']);
		$param['user_id'] = intval($_REQUEST['user_id']);		
		$data = request_api("uc_fxinvite","index",$param);
		
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
			app_redirect(wap_url("index","user#login"));
		}
		
		if(isset($data['page']) && is_array($data['page'])){			
			$page = new Page($data['page']['data_total'],$data['page']['page_size']);   //初始化分页对象			
			$p  =  $page->show();
			
			$GLOBALS['tmpl']->assign('pages',$p);
		}
		
		$data['ptype']="invite";
		//print_r($data);exit;
		$GLOBALS['tmpl']->assign("data",$data);	
		$GLOBALS['tmpl']->display("uc_fxinvite.html");
	}
	

	

	public function money_log()
	{
		global_run();
		init_app_page();
		$param=array();
		$param['page'] = intval($_REQUEST['page']);

		$data = request_api("uc_fxinvite","money_log",$param);
		
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
			app_redirect(wap_url("index","user#login"));
		}
		
		if(isset($data['page']) && is_array($data['page'])){			
			$page = new Page($data['page']['data_total'],$data['page']['page_size']);   //初始化分页对象			
			$p  =  $page->show();
			
			$GLOBALS['tmpl']->assign('pages',$p);
		}
		
		$data['ptype']="moneylog";
		//print_r($data);exit;
		$GLOBALS['tmpl']->assign("data",$data);	
		$GLOBALS['tmpl']->display("uc_fxinvite.html");		
		

	}


}
?>
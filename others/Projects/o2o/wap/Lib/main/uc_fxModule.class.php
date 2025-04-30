<?php
// +----------------------------------------------------------------------
// | Fanwe 方维o2o商业系统
// +----------------------------------------------------------------------
// | Copyright (c) 2014 http://www.fanwe.com All rights reserved.
// +----------------------------------------------------------------------
// | Author: 云淡风轻(97139915@qq.com)
// +----------------------------------------------------------------------

class uc_fxModule extends MainBaseModule
{

	public function index()
	{
		global_run();		
		init_app_page();
		
		$param['page'] = intval($_REQUEST['page']);
		$data = request_api("uc_fx","my_fx",$param);
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
			app_redirect(wap_url("index","user#login"));
		}
		
		if(isset($data['page']) && is_array($data['page'])){
		    //感觉这个分页有问题,查询条件处理;分页数10,需要与sjmpai同步,是否要将分页处理移到sjmapi中?或换成下拉加载的方式,这样就不要用到分页了
		    $page = new Page($data['page']['data_total'],$data['page']['page_size']);   //初始化分页对象
		    $p  =  $page->show();
		    $GLOBALS['tmpl']->assign('pages',$p);
		}
        
		$GLOBALS['tmpl']->assign("r",base64_encode($data['ref_uid']));
		$GLOBALS['tmpl']->assign("ajax_url",wap_url("index","uc_fx"));
		$GLOBALS['tmpl']->assign("data",$data);
		$GLOBALS['tmpl']->display("uc_fx.html");
	}
	
	public function deal_fx()
	{
	    global_run();
	    init_app_page();

	    $param['page'] = intval($_REQUEST['page']);
	    $param['fx_seach_key'] = strim($_REQUEST['fx_seach_key']);
	    $data = request_api("uc_fx","deal_fx",$param);
	    if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
	        app_redirect(wap_url("index","user#login"));
	    }
	
	    if(isset($data['page']) && is_array($data['page'])){
	        //感觉这个分页有问题,查询条件处理;分页数10,需要与sjmpai同步,是否要将分页处理移到sjmapi中?或换成下拉加载的方式,这样就不要用到分页了
	        $page = new Page($data['page']['data_total'],$data['page']['page_size']);   //初始化分页对象
	        $p  =  $page->show();
	        $GLOBALS['tmpl']->assign('pages',$p);
	    }
	
	    $GLOBALS['tmpl']->assign("ajax_url",wap_url("index","uc_fx"));
	    $GLOBALS['tmpl']->assign("data",$data);
	    $GLOBALS['tmpl']->display("uc_fx_deal.html");
	}
	public function add_user_fx_deal(){
	    global_run();
	    init_app_page();
	    
	    $param['deal_id'] = intval($_REQUEST['deal_id']);
	    $data = request_api("uc_fx","add_user_fx_deal",$param);
	    if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
	        $data['jump'] = wap_url("index","user#login");
	    }
	    ajax_return($data);
	}
	
    public function do_is_effect(){
	    global_run();		
		init_app_page();
		
		$param['deal_id'] = intval($_REQUEST['deal_id']);
		$data = request_api("uc_fx","do_is_effect",$param);
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
		    $data['jump'] = wap_url("index","user#login");
		}
		ajax_return($data);
	}
	
	public function del_user_deal(){
	    global_run();		
		init_app_page();
		
		$param['deal_id'] = intval($_REQUEST['deal_id']);
		$data = request_api("uc_fx","del_user_deal",$param);
		if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
		    $data['jump'] = wap_url("index","user#login");
		}
		ajax_return($data);
	}
	
	public function mall(){
	    global_run();		
		init_app_page();

		$param['page'] = intval($_REQUEST['page']);
		$param['type'] = intval($_REQUEST['type']);

		$data = request_api("uc_fx","mall",$param);
	
		if(isset($data['page']) && is_array($data['page'])){
		    //感觉这个分页有问题,查询条件处理;分页数10,需要与sjmpai同步,是否要将分页处理移到sjmapi中?或换成下拉加载的方式,这样就不要用到分页了
		    $page = new Page($data['page']['data_total'],$data['page']['page_size']);   //初始化分页对象
		    $p  =  $page->show();
		    $GLOBALS['tmpl']->assign('pages',$p);
		}

		//商城模版填充
		if($data['type']==1 && count($data['deal_list'])%2 !=0){
		    array_push($data['deal_list'],array());
		}
		
		$GLOBALS['tmpl']->assign("r",base64_encode($GLOBALS['ref_uid']));
		$GLOBALS['tmpl']->assign("ajax_url",wap_url("index","uc_fx"));
		$GLOBALS['tmpl']->assign("data",$data);
		$GLOBALS['tmpl']->display("uc_fx_mall.html");
	    
	}
	
}
?>
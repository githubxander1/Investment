<?php
// +----------------------------------------------------------------------
// | Fanwe 方维o2o商业系统
// +----------------------------------------------------------------------
// | Copyright (c) 2014 http://www.fanwe.com All rights reserved.
// +----------------------------------------------------------------------
// | Author: 云淡风轻(97139915@qq.com)
// +----------------------------------------------------------------------

class store_payModule extends MainBaseModule
{

	public function index()
	{
		global_run();		
		init_app_page();
                $location_id = intval($_REQUEST['id']);

		//请求接口
                $data = request_api("store_pay","pay",array("location_id"=>$location_id));
        
             
                if($data['status']==-1){
                	showErr($data['info'],0,wap_url("index","stores"));
                }
		//折扣数据
                $promote_json_data = array();
                foreach ($data['promote'] as $k=>$v){
                    $promote_json_data[] = $v['id'];
                }
//              print_r($promote_json_data);exit;
                $GLOBALS['tmpl']->assign("promote_json",  implode(',',$promote_json_data));
                $GLOBALS['tmpl']->assign("data",$data);
                $GLOBALS['tmpl']->assign("location_id",$location_id);
		$GLOBALS['tmpl']->display("pages/store_pay/index.html");
	}

	
	public function make_order()
	{
		global_run();
		init_app_page();
	
		$param = array();
	

		$param['money'] = floatval($_REQUEST['money']);
		$param['location_id'] = intval($_REQUEST['location_id']);
	
		$data = request_api("store_pay","make_order",$param);
                
		if($data['user_login_status']==1){
			if($data['status']==1){
				$data['jump']=wap_url("index","store_pay#check",array("order_id"=>$data['order_id']));
			}
			
		}else{
			$data['jump']=wap_url("index","user#login");
			//showErr('未登录，请先登录',0,wap_url('index','user#login'));
		}

		ajax_return($data);
		
	}
	
	
        public function check()
	{ 
		global_run();		
		init_app_page();
		
                $param = array();
                
                $param['order_id'] = intval($_REQUEST['order_id']);
        
		$data = request_api("store_pay","check",$param);
                
                if($data['user_login_status']!=LOGIN_STATUS_LOGINED){
		    app_redirect(wap_url("index","user#login"));
		}
		if(!$GLOBALS['is_weixin'])
		{
			foreach($data['payment_list'] as $k=>$v)
			{
				if($v['code']=="Wwxjspay")
				{
					unset($data['payment_list'][$k]);
				}
			}
		}
		else
		{
			foreach($data['payment_list'] as $k=>$v)
			{
				if($v['code']=="Upacpwap")
				{
					unset($data['payment_list'][$k]);
				}
			}
		}


		
		$account_amount = round($GLOBALS['user_info']['money'],2);
		$GLOBALS['tmpl']->assign("account_amount",$account_amount);
		$GLOBALS['tmpl']->assign("data",$data);
        $GLOBALS['tmpl']->assign("ajax_url",  wap_url("index","store_pay"));
                    
		$GLOBALS['tmpl']->display("pages/store_pay/check.html");
	}
	
	public function count_store_pay_total(){
	    global_run();
            $payment_id = intval($_REQUEST['payment']);
            $bank_id = intval($_REQUEST['bank_id']);
            $order_id = intval($_REQUEST['order_id']);
            $all_account_money = intval($_REQUEST['all_account_money']);
            
            $param = array();
            $param['payment_id'] = $payment_id;
            $param['bank_id'] = $bank_id;
            $param['order_id'] = $order_id;
            $param['all_account_money'] = $all_account_money;
            
            $data = request_api("store_pay","count_store_pay_total",$param);
            $GLOBALS['tmpl']->assign("data",$data);
            $data['html']=$GLOBALS['tmpl']->fetch("inc/store_pay.html");
            
	    ajax_return($data);
	}
        
        public function done(){
            $payment_id = intval($_REQUEST['payment']);
            $bank_id = intval($_REQUEST['bank_id']);
            $order_id = intval($_REQUEST['order_id']);
            $all_account_money = intval($_REQUEST['all_account_money']);
            $param['payment_id']=$payment_id;
            $param['bank_id']=$bank_id;
            $param['order_id']=$order_id;
            $param['all_account_money']=$all_account_money;
            
            $data = request_api("store_pay","done",$param);
            
            if($data['user_login_status']==1)
            {
            	if($data['pay_status']==1){
            		
            		$data['jump']=wap_url('index','store_payment#done',array('order_id'=>$data['order_id']));
            	}else{
            		$data['jump']=wap_url('index','store_payment#done',array('order_id'=>$data['order_id']));
            	}

            	ajax_return($data);
            
            }else{

            	showErr('未登录，请先登录',0,wap_url('index','user#login'));
            }
            
      
        }
        
        public function promote()
        {
        	global_run();
        
        	$param = array();
        	$param['money'] = floatval($_REQUEST['money']);
        	$param['location_id'] = intval($_REQUEST['location_id']);
        	$param['id'] = explode(',',strim($_REQUEST['id']));
        
        	$data = request_api("store_pay","promote",$param);
        //	$data['promote']['id']=json_encode($data['promote']['id']);
        	ajax_return($data);
        
        }
}
?>
<?php
// +----------------------------------------------------------------------
// | Fanwe 方维o2o商业系统
// +----------------------------------------------------------------------
// | Copyright (c) 2014 http://www.fanwe.com All rights reserved.
// +----------------------------------------------------------------------
// | Author: 云淡风轻(97139915@qq.com)
// +----------------------------------------------------------------------

class store_paymentModule extends MainBaseModule
{
	
	

	/**
	 *  支付订单页面，点击“确认支付”的跳转地址
	 *
	 */
	public function done()
	{
		global_run();
		init_app_page();
		$param['pay_status'] = intval($_REQUEST['pay_status']);
		$param['order_id'] = intval($_REQUEST['order_id']);
		$param['payment_notice_id'] = intval($_REQUEST['payment_notice_id']);
		$param['form'] = 'wap';
		$data = request_api("store_payment","done",$param);
		
		$GLOBALS['tmpl']->assign("data",$data);
		$GLOBALS['tmpl']->display("pages/store_pay/payment_done.html");
	

	}
	

	
	/**
	 *  会员充值
	 *
	 */
	public function incharge()
	{
	
		$param['pay_status'] = intval($_REQUEST['pay_status']);
		$param['order_id'] = intval($_REQUEST['order_id']);
		$param['payment_notice_id'] = intval($_REQUEST['payment_notice_id']);
		$param['form'] = 'wap';
		$data = request_api("dc_payment","incharge",$param);
	
		$GLOBALS['tmpl']->assign("data",$data);
		$GLOBALS['tmpl']->display("dc/dc_payment_done.html");
	
	
	}
	
	
	

}
?>
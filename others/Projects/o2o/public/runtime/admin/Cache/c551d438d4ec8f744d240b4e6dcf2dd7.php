<?php if (!defined('THINK_PATH')) exit();?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html>
<head>
<title></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=7" />
<link rel="stylesheet" type="text/css" href="__TMPL__Common/style/style.css" />
<style type="text/css">
	
/**
 * 自定义的font-face
 */
@font-face {font-family: "diyfont";
  src: url('<?php echo APP_ROOT; ?>/public/iconfont/iconfont.eot?r=<?php echo time(); ?>'); /* IE9*/
  src: url('<?php echo APP_ROOT; ?>/public/iconfont/iconfont.eot?#iefix&r=<?php echo time(); ?>') format('embedded-opentype'), /* IE6-IE8 */
  url('<?php echo APP_ROOT; ?>/public/iconfont/iconfont.woff?r=<?php echo time(); ?>') format('woff'), /* chrome、firefox */
  url('<?php echo APP_ROOT; ?>/public/iconfont/iconfont.ttf?r=<?php echo time(); ?>') format('truetype'), /* chrome、firefox、opera、Safari, Android, iOS 4.2+*/
  url('<?php echo APP_ROOT; ?>/public/iconfont/iconfont.svg#iconfont&r=<?php echo time(); ?>') format('svg'); /* iOS 4.1- */}
.diyfont {
  font-family:"diyfont" !important;
  font-size:20px;
  font-style:normal;
  -webkit-font-smoothing: antialiased;
  -webkit-text-stroke-width: 0.2px;
  -moz-osx-font-smoothing: grayscale;
}

</style>
<script type="text/javascript">
 	var VAR_MODULE = "<?php echo conf("VAR_MODULE");?>";
	var VAR_ACTION = "<?php echo conf("VAR_ACTION");?>";
	var MODULE_NAME	=	'<?php echo MODULE_NAME; ?>';
	var ACTION_NAME	=	'<?php echo ACTION_NAME; ?>';
	var ROOT = '__APP__';
	var ROOT_PATH = '<?php echo APP_ROOT; ?>';
	var CURRENT_URL = '<?php echo btrim($_SERVER['REQUEST_URI']);?>';
	var INPUT_KEY_PLEASE = "<?php echo L("INPUT_KEY_PLEASE");?>";
	var TMPL = '__TMPL__';
	var APP_ROOT = '<?php echo APP_ROOT; ?>';
	
	//关于图片上传的定义
	var UPLOAD_SWF = '__TMPL__Common/js/Moxie.swf';
	var UPLOAD_XAP = '__TMPL__Common/js/Moxie.xap';
	var MAX_IMAGE_SIZE = '1000000';
	var ALLOW_IMAGE_EXT = 'zip';
	var UPLOAD_URL = '<?php echo u("File/do_upload_icon");?>';
	var ICON_FETCH_URL = '<?php echo u("File/fetch_icon");?>';
	var ofc_swf = '__TMPL__Common/js/open-flash-chart.swf';
</script>
<script type="text/javascript" src="__TMPL__Common/js/jquery.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/jquery.timer.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/plupload.full.min.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/ui_upload.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/jquery.bgiframe.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/jquery.weebox.js"></script>
<link rel="stylesheet" type="text/css" href="__TMPL__Common/style/weebox.css" />
<script type="text/javascript" src="__TMPL__Common/js/swfobject.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/script.js"></script>

<script type="text/javascript" src="__ROOT__/public/runtime/admin/lang.js"></script>
<script type='text/javascript'  src='__ROOT__/admin/public/kindeditor/kindeditor.js'></script>
</head>
<body>
<div id="info"></div>

<script type="text/javascript" src="__TMPL__Common/js/jquery.bgiframe.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/jquery.weebox.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/user.js"></script>
<link rel="stylesheet" type="text/css" href="__TMPL__Common/style/weebox.css" />
<script type="text/javascript" src="__TMPL__Common/js/deal_order.js"></script>
<?php function get_delivery_sn($deal_order_item_id)
{
	$delivery_notice = M("DeliveryNotice")->where("order_item_id=".$deal_order_item_id)->order("delivery_time desc")->find();
	$order_id = M("DealOrderItem")->where("id=".$delivery_notice['order_item_id'])->getField("order_id");
	$res = $delivery_notice['notice_sn'];
	if($delivery_notice['express_id']!=0)
	{
		$res.=" <br /><a href='".U("Express/eprint",array("order_id"=>$order_id,"express_sn"=>$delivery_notice['notice_sn'],"express_id"=>$delivery_notice['express_id']))."' target='_blank'>".l("PRINT_EXPRESS")."</a> <a href='javascript:void(0);' onclick='track_express(\"".$delivery_notice['notice_sn']."\",\"".$delivery_notice['express_id']."\");'>".l("TRACK_EXPRESS")."</a>";
	}
	return $res;
}
function get_delivery_arrival($deal_order_item_id)
{
	$delivery_notice =  M("DeliveryNotice")->where("order_item_id=".$deal_order_item_id)->order("delivery_time desc")->find();
	if($delivery_notice['is_arrival']==1)
	{
		return l("USER_CONFIRM_DELIVERY");
	}
	elseif($delivery_notice['is_arrival']==2)
	{
		return "<span style='color:#f30;'>用户未收到货，维权</span>";
	}
	else
	{
		return l("USER_NOT_CONFIRM_DELIVERY");
	}
}
function get_delivery_memo($deal_order_item_id)
{
	return M("DeliveryNotice")->where("order_item_id=".$deal_order_item_id)->getField("memo");
} ?>
<script type="text/javascript">
	function track_express(express_sn,express_id)
	{	
		var newTab=window.open('about:blank');
		$.ajax({ 
				url: "<?php echo u("DealOrder/check_delivery");?>&express_sn="+express_sn+"&express_id="+express_id, 
				data: "ajax=1",
				dataType: "json",
				success: function(obj){
					
					if(obj.status==1)
					{
						newTab.location.href=obj.msg;
					}
					if(obj.status==0)
					{
						alert(obj.msg);
					}				
				}
		});		
	}

</script>
<div class="main">
<div class="main_title"><?php if($order_info['order_status'] == 0): ?><?php echo L("DEAL_ORDER_HANDLE");?><?php else: ?><?php echo L("DEAL_ORDER_VIEW");?><?php endif; ?><?php echo ($order_info["order_sn"]); ?>

</div>
<div class="blank5"></div>

<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=4 class="topTd"></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ORDER_USER");?>:</td>
		<td class="item_input">
			<?php echo (get_user_name_js($order_info["user_id"])); ?>
		</td>
		<td class="item_title">订单状态:</td>
		<td class="item_input">
			<?php echo (get_order_status($order_info["order_status"],$order_info)); ?>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ORDER_SN");?>:</td>
		<td class="item_input"><?php echo ($order_info["order_sn"]); ?></td>
		<td class="item_title"><?php echo L("ORDER_CREATE_TIME");?>:</td>
		<td class="item_input"><?php echo (to_date($order_info["create_time"])); ?></td>
	</tr>	
	<tr>
		<td class="item_title"><?php echo L("ORDER_PAY_STATUS");?>:</td>
		<td class="item_input"><?php echo (get_pay_status($order_info["pay_status"])); ?>
			<?php if($order_info['pay_status'] != 2): ?><input type="button" class="button" value="<?php echo L("ADMIN_INCHARGE_ORDER");?>" onclick="location.href='__APP__?m=DealOrder&a=order_incharge&id=<?php echo ($order_info["id"]); ?>';"  /><?php endif; ?>
		</td>
		<td class="item_title"><?php echo L("ORDER_DELIVERY_STATUS");?>:</td>
		<td class="item_input"><?php echo (get_delivery_status($order_info["delivery_status"],$order_info)); ?></td>
	</tr>
	<tr>
		<th colspan=4><?php echo L("PAYMENT_INFORMATION");?></th>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ORDER_TOTAL_PRICE");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["total_price"])); ?></td>
		<td class="item_title"><?php echo L("INCHARGE_AMOUNT");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["pay_amount"])); ?></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ORDER_DEAL_TOTAL_PRICE");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["deal_total_price"])); ?></td>
		<td class="item_title"><?php echo L("ORDER_USER_DISCOUNT");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["discount_price"])); ?></td>		
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ACCOUNT_PAYMENT");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["account_money"])); ?></td>
		<td class="item_title"><?php echo L("ECV_PAYMENT");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["ecv_money"])); ?></td>
	</tr>
	<?php if($order_info['payment_id'] > 0): ?><tr>
		<td class="item_title"><?php echo L("PAYMENT_METHOD");?>:</td>
		<td class="item_input"><?php echo (get_payment_name($order_info["payment_id"])); ?></td>
		<td class="item_title"><?php echo L("FEE_AMOUNT");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["payment_fee"])); ?></td>
	</tr><?php endif; ?>
	<?php if($order_info['delivery_id'] > 0): ?><tr>
		<th colspan=4><?php echo L("ORDER_DELIVERY");?></th>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ORDER_DELIVERY_METHOD");?></td>
		<td class="item_input"><?php echo (get_delivery_name($order_info["delivery_id"])); ?></td>
		<td class="item_title"><?php echo L("DELIVERY_FEE");?>:</td>
		<td class="item_input"><?php echo (format_price($order_info["delivery_fee"])); ?></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("DELIVERY_REGION_INFO");?>:</td>
		<td colspan=3>
			<?php echo L("REGION_LV1");?>：<?php echo (get_region_name($order_info["region_lv1"])); ?>
			<?php echo L("REGION_LV2");?>：<?php echo (get_region_name($order_info["region_lv2"])); ?>
			<?php echo L("REGION_LV3");?>：<?php echo (get_region_name($order_info["region_lv3"])); ?>
			<?php echo L("REGION_LV4");?>：<?php echo (get_region_name($order_info["region_lv4"])); ?>		
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("DELIVERY_ADDRESS");?>:</td>
		<td class="item_input"><?php echo ($order_info["address"]); ?></td>
		<td class="item_title"><?php echo L("DELIVERY_ZIP");?>:</td>
		<td class="item_input"><?php echo ($order_info["zip"]); ?></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("DELIVERY_CONSIGNEE");?>:</td>
		<td class="item_input"><?php echo ($order_info["consignee"]); ?></td>
		<td class="item_title"><?php echo L("DELIVERY_MOBILE");?>:</td>
		<td class="item_input"><?php echo ($order_info["mobile"]); ?></td>
	</tr><?php endif; ?>
	<tr>
		<th colspan=4><?php echo L("EXT_INFO");?></th>
	</tr>
	<tr>
		<td class="item_title">消费返现:</td>
		<td class="item_input"><?php echo (format_price($order_info["return_total_money"])); ?></td>
		<td class="item_title">
			<?php if($order_deals[0]['buy_type'] == 1): ?>消耗的积分:
			<?php else: ?>
			消费返积分:<?php endif; ?>
		</td>
		<td class="item_input"><?php echo (abs($order_info["return_total_score"])); ?>积分</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("ORDER_MEMO");?>:</td>
		<td colspan=3>
			<?php echo ($order_info["memo"]); ?>
		</td>
	</tr>
	<tr>
		<td colspan=4 class="bottomTd"></td>
	</tr>
</table>
<div class="blank5"></div>

<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=6 class="topTd"></td>
	</tr>
	<tr>
		<th colspan=6><?php echo L("ORDER_DEAL_GOODS");?></th>
	</tr>
	<tr>
		<th><?php echo L("ORDER_DEAL_GOODS_NAME");?></th>
		<th width=50><?php echo L("NUMBER");?></th>
		<th width=80><?php echo L("DEAL_TOTAL_PRICE");?></th>
		<th width=200>商家</th>
		<th width=250><?php echo L("DELIVERY_OP");?></th>
		<th width=200><?php echo L("DELIVERY_MEMO");?></th>
	</tr>
	<?php if(is_array($order_deals)): foreach($order_deals as $key=>$deal_item_group): ?><tr><td colspan=6>
		<div style="float:left;"><?php echo ($deal_item_group['supplier']); ?></div>
		<div style="float:right;"><?php if($deal_item_group['delivery_fee'] != -1): ?>运费：<?php echo ($deal_item_group['delivery_fee']); ?><?php endif; ?></div>
	</td></tr>
	<?php if(is_array($deal_item_group['goods_list'])): foreach($deal_item_group['goods_list'] as $key=>$deal_item): ?><tr>
		<td><?php echo ($deal_item["name"]); ?></td>
		<td><?php echo ($deal_item["number"]); ?></td>
		<td><?php echo (format_price($deal_item["total_price"])); ?></td>
		<td>
			<a href='<?php echo u("Supplier/index",array("id"=>$deal_item['supplier_id']));?>'><?php echo (get_supplier_name($deal_item["supplier_id"])); ?></a>
		</td>
		<td>
		<?php if($deal_item['is_delivery'] == 0): ?>无需发货
		<?php else: ?>
			<?php if($deal_item['delivery_status'] == 0): ?><?php if($deal_item['refund_status'] == 1): ?><span style="color:#f30;">退款申请</span>					
				 	&nbsp;
				 	<a href="javascript:void(0);" class="do_refund" action="<?php echo u("DealOrder/refund",array("order_item_id"=>$deal_item['id']));?>">退款审核</a> 
					<?php else: ?>
					<?php if($deal_item['refund_status'] == 2): ?>已退款	
					<?php else: ?>
					<input type="button" class="button" value="<?php echo L("DELIVERY");?>" onclick="location.href='__APP__?m=DealOrder&a=delivery&id=<?php echo ($order_info["id"]); ?>';"  />
					<br />
					<a href="javascript:void(0);" class="do_refund" action="<?php echo u("DealOrder/refund",array("order_item_id"=>$deal_item['id']));?>">立即退款</a><?php endif; ?><?php endif; ?>
			<?php else: ?>				
				  已发货
				 <br />
				 <?php echo L("DELIVERY_SN");?>：<?php echo (get_delivery_sn($deal_item["id"])); ?>
				 <br /><br />
				 <?php echo (get_delivery_arrival($deal_item["id"])); ?>
				 <?php if($deal_item['is_arrival'] == 2): ?><br />
					<?php if($deal_item['buy_type'] == 0): ?><a href="javascript:void(0);" class="do_refund" action="<?php echo u("DealOrder/refund",array("order_item_id"=>$deal_item['id']));?>">退款审核</a> |<?php endif; ?>
					<a href="javascript:void(0);" class="do_verify"  action="<?php echo u("DealOrder/do_verify",array("order_item_id"=>$deal_item['id']));?>">虚假维权，强制收货</a>
					<br /><br />
					<input type="button" class="button" value="<?php echo L("REDELIVERY");?>" onclick="location.href='__APP__?m=DealOrder&a=delivery&id=<?php echo ($order_info["id"]); ?>';"  /><?php endif; ?>
				 <?php if($deal_item['is_arrival'] == 0): ?><br />
					<?php if($deal_item['refund_status'] == 2): ?>已退款
					<?php else: ?>					
						<a href="javascript:void(0);" class="do_verify" action="<?php echo u("DealOrder/do_verify",array("order_item_id"=>$deal_item['id']));?>">长期不收货，强制收货</a>
						<br />
						<a href="javascript:void(0);" class="do_refund" action="<?php echo u("DealOrder/refund",array("order_item_id"=>$deal_item['id']));?>">立即退款</a><?php endif; ?><?php endif; ?><?php endif; ?><?php endif; ?>
		</td>
		<td> <?php echo (get_delivery_memo($deal_item["id"])); ?></td>
	</tr><?php endforeach; endif; ?><?php endforeach; endif; ?>
	<tr>
		<td colspan=6 class="bottomTd"></td>
	</tr>
</table>

<?php if($coupon_list): ?><div class="blank5"></div>
	
<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=10 class="topTd"></td>
	</tr>
	<tr>
		<th colspan=10><?php echo L("ORDER_COUPON");?></th>
	</tr>
	<tr>
		<th width=100><?php echo L("COUPON_SN");?></th>
		<th><?php echo L("COUPON_DEAL");?></th>
		<th width=80><?php echo L("USER_NAME");?></th>
		<th width=100>状态</th>
		<th width=200><?php echo L("COUPON_SUPPLIER");?></th>
		<th width=120><?php echo L("COUPON_BEGIN_TIME");?></th>
		<th width=120><?php echo L("COUPON_END_TIME");?></th>
		<th width=120><?php echo L("COUPON_CONFIRM_TIME");?></th>
		<th width=150><?php echo L("TAG_LANG_OPERATE");?></th>
	</tr>
	<?php if(is_array($coupon_list)): foreach($coupon_list as $key=>$coupon_item): ?><tr>
		<td><?php echo ($coupon_item["password"]); ?></td>
		<td><a href='<?php echo u("Deal/index",array("id"=>$coupon_item['deal_id']));?>'><?php echo (get_order_item_name($coupon_item["order_deal_id"])); ?></a></td>
		<td><?php echo (get_user_name($coupon_item["user_id"])); ?></td>
		<td><?php echo l("COUPON_IS_VALID_".$coupon_item['is_valid']);?></td>
		<td><a href='<?php echo u("Supplier/index",array("id"=>$coupon_item['supplier_id']));?>'><?php echo (get_supplier_name($coupon_item["supplier_id"])); ?></a></td>
		<td><?php echo (to_date($coupon_item["begin_time"])); ?></td>
		<td><?php echo (to_date($coupon_item["end_time"])); ?></td>
		<td>
			<?php if($coupon_item['confirm_time'] == 0): ?><?php echo L("NOT_USED");?>
			<?php else: ?>
				<?php echo (to_date($coupon_item["confirm_time"])); ?><?php endif; ?>
			<?php if($coupon_item['refund_status'] == 1): ?><br />
			<span style="color:#f30;">退款申请</span><?php endif; ?>
			<?php if($coupon_item['refund_status'] == 2): ?><br />
			<span style="color:#f30;">已退款</span><?php endif; ?>
			<?php if($coupon_item['refund_status'] == 3): ?><br />
			<span style="color:#f30;">拒绝退款</span><?php endif; ?>
		</td>
		<td>
			<a href="<?php echo u("DealCoupon/sms",array("id"=>$coupon_item['id']));?>">短信补发</a>
			<a href="<?php echo u("DealCoupon/mail",array("id"=>$coupon_item['id']));?>">邮件补发</a>
			<?php if($coupon_item['refund_status'] == 1): ?><br />
			<span style="color:#f30;">退款申请 <br /><a href="javascript:void(0);" class="do_refund" action="<?php echo u("DealOrder/refund",array("coupon_id"=>$coupon_item['id']));?>">退款审核</a></span>
			<?php else: ?>
			<br />
			<a href="javascript:void(0);" class="do_refund" action="<?php echo u("DealOrder/refund",array("coupon_id"=>$coupon_item['id']));?>">立即退款</a></span><?php endif; ?>
			<?php if($coupon_item['refund_status'] == 0 or $coupon_item['refund_status'] == 3): ?><?php if($coupon_item['confirm_time'] == 0): ?><br />			
				<a href="javascript:void(0);" class="do_verify"  action="<?php echo u("DealOrder/do_verify",array("coupon_id"=>$coupon_item['id']));?>">管理员验证消费</a><?php endif; ?><?php endif; ?>
		</td>
		
	</tr><?php endforeach; endif; ?>
	<tr>
		<td colspan=10 class="bottomTd"></td>
	</tr>
</table><?php endif; ?>

<div class="blank5"></div>

<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=6 class="topTd"></td>
	</tr>
	<tr>
		<th colspan=6><?php echo L("PAYMENT_NOTICE");?></th>
	</tr>
	<tr>
		<th><?php echo L("PAYMENT_NOTICE_SN");?></th>
		<th><?php echo L("OUTER_NOTICE_SN");?></th>
		<th><?php echo L("PAY_TIME");?></th>
		<th><?php echo L("PAYMENT_AMOUNT");?></th>
		<th><?php echo L("PAYMENT_METHOD");?></th>
		<th><?php echo L("PAYMENT_MEMO");?></th>
	</tr>
	<?php if(is_array($payment_notice)): foreach($payment_notice as $key=>$notice_item): ?><tr>
		<td><?php echo ($notice_item["notice_sn"]); ?></td>
		<td><?php echo ($notice_item["outer_notice_sn"]); ?></td>
		<td><?php echo (to_date($notice_item["pay_time"])); ?></td>
		<td><?php echo (format_price($notice_item["money"])); ?></td>
		<td><?php echo (get_payment_name($notice_item["payment_id"])); ?></td>
		<td><?php echo ($notice_item["memo"]); ?></td>
		
	</tr><?php endforeach; endif; ?>
	<tr>
		<td colspan=6 class="bottomTd"></td>
	</tr>
</table>



<div class="blank5"></div>
<?php if($list): ?><!-- Think 系统列表组件开始 -->
<table id="dataTable" class="dataTable" cellpadding=0 cellspacing=0 ><tr><td colspan="4" class="topTd" >&nbsp; </td></tr><tr class="row" ><th width="50px  "><a href="javascript:sortBy('id','<?php echo ($sort); ?>','DealOrder','view_order')" title="按照<?php echo L("ID");?><?php echo ($sortType); ?> "><?php echo L("ID");?><?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('content','<?php echo ($sort); ?>','DealOrder','view_order')" title="按照<?php echo L("MESSAGE_CONTENT");?>  <?php echo ($sortType); ?> "><?php echo L("MESSAGE_CONTENT");?>  <?php if(($order)  ==  "content"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('create_time','<?php echo ($sort); ?>','DealOrder','view_order')" title="按照<?php echo L("MESSAGE_CREATE_TIME");?>  <?php echo ($sortType); ?> "><?php echo L("MESSAGE_CREATE_TIME");?>  <?php if(($order)  ==  "create_time"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('user_id','<?php echo ($sort); ?>','DealOrder','view_order')" title="按照<?php echo L("USER_NAME");?><?php echo ($sortType); ?> "><?php echo L("USER_NAME");?><?php if(($order)  ==  "user_id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th></tr><?php if(is_array($list)): $i = 0; $__LIST__ = $list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$message): ++$i;$mod = ($i % 2 )?><tr class="row" ><td>&nbsp;<?php echo ($message["id"]); ?></td><td>&nbsp;<?php echo ($message["content"]); ?></td><td>&nbsp;<?php echo (to_date($message["create_time"])); ?></td><td>&nbsp;<?php echo (get_user_name($message["user_id"])); ?></td></tr><?php endforeach; endif; else: echo "" ;endif; ?><tr><td colspan="4" class="bottomTd"> &nbsp;</td></tr></table>
<!-- Think 系统列表组件结束 -->
 
<div class="blank5"></div>
<div class="page"><?php echo ($page); ?></div>

<div class="blank5"></div><?php endif; ?>

<?php if($order_info['promote_description']): ?><table class="form" cellpadding=0 cellspacing=0>
		<tr>
		<td  class="topTd"></td>
		</tr>
		<tr><th >享受的促销</th></tr>
			
			<tr>
				<td><?php echo ($order_info["promote_description"]); ?></td>
			</tr>

		<tr>
		<td colspan=2 class="bottomTd"></td>
		</tr>
	</table>
	<div class="blank5"></div><?php endif; ?>
<?php if($log_list): ?><table class="form" cellpadding=0 cellspacing=0>
		<tr>
		<td colspan=2 class="topTd"></td>
		</tr>
		<tr><th colspan=2><?php echo L("ORDER_LOG");?></th></tr>
			<?php if(is_array($log_list)): foreach($log_list as $key=>$log_item): ?><tr>
				<td><?php echo ($log_item["log_info"]); ?></td>
				<td><?php echo (to_date($log_item["log_time"])); ?></td>
			</tr><?php endforeach; endif; ?>
		<tr>
		<td colspan=2 class="bottomTd"></td>
		</tr>
	</table>
	<div class="blank5"></div><?php endif; ?>

</div>
</body>
</html>
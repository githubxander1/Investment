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

<script type="text/javascript" src="__TMPL__Common/js/dc.js"></script>
<?php function get_handle($id,$order_info)
	{	
		
		if($order_info['is_cancel']>0 || $order_info['refund_status'] > 1)
		{		
			$str = l("DEAL_ORDER_VIEW");
			
			$str = "<a href='".u("DcOrder/view_order",array("id"=>$id))."'>".$str."</a>";
			$str.="&nbsp;&nbsp;<a href='javascript:del(".$id.");'>".l("删除订单")."</a>";
		}
		else
		{
			if($order_info['order_status']==0)
			{
				$str = l("DEAL_ORDER_HANDLE");
				$str = "<a href='".u("DcOrder/view_order",array("id"=>$id))."'>".$str."</a>";
				if($order_info['confirm_status'] < 2 && $order_info['refund_status']==0 && $order_info['is_cancel']==0){
					
					$str.="&nbsp;&nbsp;<a href='javascript:close_order(".$id.");'>".l("关闭交易")."</a>";
				}
			}
			else
			{
				$str = l("DEAL_ORDER_VIEW");
				$str = "<a href='".u("DcOrder/view_order",array("id"=>$id))."'>".$str."</a>";
				$str.="&nbsp;&nbsp;<a href='javascript:del(".$id.");'>".l("删除订单")."</a>";
			}
		}	
		
			return $str;
	}

	
	function get_order_item($order_sn,$order_info)
	{
		$str = "<span><b>".$order_sn."</b></span>";
	
		$str.= "<span>".$order_info['location_name']."</span>";
		
		if($order_info['dc_comment']){
		
		$str.= "<span style='width: 260px; word-wrap: break-word;'>订单备注：".$order_info['dc_comment']."</span>";
		}
		
		if($order_info['order_delivery_time']>1){
		
		$str.= "<span>期望时间：".to_date($order_info['order_delivery_time'])."</span>";
		}
		else{
		
		$str.= "<span>期望时间：立即送餐</span>";
		}
		
		return $str;
		
	}
	
	
	function dc_get_pay_status($status)
	{
	
		return L("DC_PAY_STATUS_".$status);
	}
	
	function get_dc_order_status($id,$order_info)
	{
	
		if($order_info['is_cancel']>0)
		{
			$str="订单已关闭";
		}
		else
		{
			if($order_info['pay_status']==0){
				$str="支付中";
			}elseif($order_info['pay_status']==1){
			
				if($order_info['order_status']==0){
					if($order_info['confirm_status']==0){
						$str="待接单";
						if($order_info['refund_status']==1){
							$str.="<span style='color:#f30;'>申请退款</span>";
						}elseif($order_info['refund_status']==2){
							$str.="<span style='color:#f30;'>已退款</span>";
						}elseif($order_info['refund_status']==3){
							$str.="<span style='color:#f30;'>退款驳回</span>";
						}
					
					}elseif($order_info['confirm_status']==1){
					$str="已接单";
					
						if($order_info['refund_status']==1){
							$str.="<span style='color:#f30;'>申请退款</span>";
						}elseif($order_info['refund_status']==2){
							$str.="<span style='color:#f30;'>已退款</span>";
						}elseif($order_info['refund_status']==3){
							$str.="<span style='color:#f30;'>退款驳回</span>";
						}
					}elseif($order_info['confirm_status']==2){
					$str="已完成";
					}
				}else{
					$str="已结单";
				}
			}
		}
		
		return 	$str;
	} ?>
<script type="text/javascript" src="__TMPL__Common/js/jquery.bgiframe.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/jquery.weebox.js"></script>
<link rel="stylesheet" type="text/css" href="__TMPL__Common/style/weebox.css" />
<style>
#close_formx label{
	display:block;
	clear:both;
	
}
#dataTable td span{
	clear: both;
    display: block;
    float: left;
}
.weedialog .dialog-button input{
	width:70px !important;
	*width:70px;
	_width:70px;
}
</style>
<div class="main">
<div class="main_title">外卖订单列表</div>
<div class="blank5"></div>
<form name="search" action="__APP__" method="get">	
<div class="button_row">
	<input type="button" class="button" value="<?php echo L("DEL");?>" onclick="del();" />
	<?php if(!$_REQUEST['referer']): ?><input type="button" class="button" value="<?php echo L("EXPORT");?>" onclick="export_csv();" /><?php endif; ?>

</div>
<div class="blank5"></div>
<div class="search_row">

		<?php echo L("ORDER_SN");?>：<input type="text" class="textbox" name="order_sn" value="<?php echo strim($_REQUEST['order_sn']);?>" style="width:100px;" />
		<?php echo L("USER_NAME_S");?>：<input type="text" class="textbox" name="user_name" value="<?php echo strim($_REQUEST['user_name']);?>" style="width:100px;" />
		<?php echo L("SUPPLIER_NAME");?>：<input type="text" class="textbox" name="location_name" value="<?php echo strim($_REQUEST['location_name']);?>" style="width:100px;" />

		
		订单状态: 
		<select name="order_status">
				<option value="-1" <?php if(intval($_REQUEST['order_status']) == -1): ?>selected="selected"<?php endif; ?>>全部</option>
				<option value="0" <?php if(intval($_REQUEST['order_status']) == 0): ?>selected="selected"<?php endif; ?>>支付中</option>
				<option value="1" <?php if(intval($_REQUEST['order_status']) == 1): ?>selected="selected"<?php endif; ?>>待接单</option>
				<option value="2" <?php if(intval($_REQUEST['order_status']) == 2): ?>selected="selected"<?php endif; ?>>已接单</option>
				<option value="3" <?php if(intval($_REQUEST['order_status']) == 3): ?>selected="selected"<?php endif; ?>>已完成</option>
				<option value="4" <?php if(intval($_REQUEST['order_status']) == 4): ?>selected="selected"<?php endif; ?>>已结单</option>
				<option value="5" <?php if(intval($_REQUEST['order_status']) == 5): ?>selected="selected"<?php endif; ?>>申请退款</option>
				<option value="6" <?php if(intval($_REQUEST['order_status']) == 8): ?>selected="selected"<?php endif; ?>>订单关闭</option>
		</select>

		<input type="hidden" value="DcOrder" name="m" />
		<input type="hidden" value="index" name="a" />
		
		<input type="submit" class="button" value="<?php echo L("SEARCH");?>" />

</div>
</form>
<div class="blank5"></div>
<!-- Think 系统列表组件开始 -->
<table id="dataTable" class="dataTable" cellpadding=0 cellspacing=0 ><tr><td colspan="10" class="topTd" >&nbsp; </td></tr><tr class="row" ><th width="8"><input type="checkbox" id="check" onclick="CheckAll('dataTable')"></th><th width="50px"><a href="javascript:sortBy('id','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("ID");?><?php echo ($sortType); ?> "><?php echo L("ID");?><?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th width="260;"><a href="javascript:sortBy('order_sn','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("DC_ORDER_INFO");?><?php echo ($sortType); ?> "><?php echo L("DC_ORDER_INFO");?><?php if(($order)  ==  "order_sn"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('menu','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("DC_MENU_INFO");?><?php echo ($sortType); ?> "><?php echo L("DC_MENU_INFO");?><?php if(($order)  ==  "menu"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('user_name','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("USER_NAME");?>    <?php echo ($sortType); ?> "><?php echo L("USER_NAME");?>    <?php if(($order)  ==  "user_name"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('create_time','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("ORDER_CREATE_TIME");?>   <?php echo ($sortType); ?> "><?php echo L("ORDER_CREATE_TIME");?>   <?php if(($order)  ==  "create_time"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('total_price','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("PAY_AMOUNT");?>   <?php echo ($sortType); ?> "><?php echo L("PAY_AMOUNT");?>   <?php if(($order)  ==  "total_price"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('pay_amount','<?php echo ($sort); ?>','DcOrder','index')" title="按照<?php echo L("PAID_AMOUNT");?>      <?php echo ($sortType); ?> "><?php echo L("PAID_AMOUNT");?>      <?php if(($order)  ==  "pay_amount"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('id','<?php echo ($sort); ?>','DcOrder','index')" title="按照订单状态<?php echo ($sortType); ?> ">订单状态<?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th >操作</th></tr><?php if(is_array($list)): $i = 0; $__LIST__ = $list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$deal_order): ++$i;$mod = ($i % 2 )?><tr class="row" ><td><input type="checkbox" name="key" class="key" value="<?php echo ($deal_order["id"]); ?>"></td><td>&nbsp;<?php echo ($deal_order["id"]); ?></td><td>&nbsp;<?php echo (get_order_item($deal_order["order_sn"],$deal_order)); ?></td><td>&nbsp;<?php echo ($deal_order["menu"]); ?></td><td>&nbsp;<?php echo ($deal_order["user_name"]); ?></td><td>&nbsp;<?php echo (to_date($deal_order["create_time"])); ?></td><td>&nbsp;<?php echo (format_price($deal_order["total_price"])); ?></td><td>&nbsp;<?php echo (format_price($deal_order["pay_amount"])); ?></td><td>&nbsp;<?php echo (get_dc_order_status($deal_order["id"],$deal_order)); ?></td><td> <?php echo (get_handle($deal_order["id"],$deal_order)); ?>&nbsp;</td></tr><?php endforeach; endif; else: echo "" ;endif; ?><tr><td colspan="10" class="bottomTd"> &nbsp;</td></tr></table>
<!-- Think 系统列表组件结束 -->
 

<div class="blank5"></div>
<div class="page"><?php echo ($page); ?></div>
</div>
</body>
</html>
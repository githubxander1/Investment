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

<div class="main">
<div class="main_title"><?php if($order_info['order_status'] == 0): ?><?php echo L("DEAL_ORDER_HANDLE");?><?php else: ?><?php echo L("DEAL_ORDER_VIEW");?><?php endif; ?><?php echo ($order_info["order_sn"]); ?></div>
<div class="blank5"></div>
<form name="edit" action="__APP__" method="post" enctype="multipart/form-data">
<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=5 class="topTd"></td>
	</tr>
	<tr>
		<th colspan=5><?php echo L("DEAL_GOODS_LIST");?></th>
	</tr>
	<tr>
		<th><?php echo L("CHOICE");?></th>
		<th><?php echo L("DEAL_NAME");?></th>
		<th><?php echo L("NUMBER");?></th>
		<th><?php echo L("DEAL_UNIT_PRICE");?></th>
		<th><?php echo L("DEAL_TOTAL_PRICE");?></th>
	</tr>
	<?php if(is_array($order_deals)): foreach($order_deals as $key=>$deal_item): ?><tr>
		<td><input type="checkbox" name="order_deals[]" value="<?php echo ($deal_item["id"]); ?>" /> <?php if($deal_item['delivery_status'] == 1): ?><?php echo L("DELIVERYED");?><?php endif; ?></td>
		
		<td><?php echo ($deal_item["name"]); ?></td>
		<td><?php echo ($deal_item["number"]); ?></td>
		<td><?php echo (format_price($deal_item["unit_price"])); ?></td>
		<td><?php echo (format_price($deal_item["total_price"])); ?></td>

	</tr><?php endforeach; endif; ?>
	<tr>
		<td><?php echo L("DELIVERY_SN");?>:</td>
		<td colspan="4">
		<lable><?php echo L("SELECT_EXPRESS");?>
		<select name="express_id">
			<option value="0"><?php echo L("OTHER_EXPRESS");?></option>
			<?php if(is_array($express_list)): foreach($express_list as $key=>$express): ?><option value="<?php echo ($express["id"]); ?>"><?php echo ($express["name"]); ?></option><?php endforeach; endif; ?>
		</select>
		</lable>
			
		<input type="text" class="textbox" name="delivery_sn" /> 
		
		<span class="tip_span"><?php echo L("DELIVERY_SN_TIP");?></span>
		<br />
		<lable><input type="checkbox" value="1" name="send_goods_to_payment" /><?php echo L("SEND_GOODS_TO_PAYMENT");?></lable>
		
		
		</td>
	</tr>
	<tr>
		<td><?php echo L("DELIVERY_MEMO");?></td>
		<td colspan=4><textarea class="textarea" name="memo" ></textarea></td>
	</tr>
	<tr>
		<td colspan=5>
			<input type="hidden" name="order_id" value="<?php echo ($order_info["id"]); ?>" />
			<input type="hidden" name="<?php echo conf("VAR_MODULE");?>" value="DealOrder" />
			<input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="do_delivery" />
			<input type="submit" class="button" value="<?php echo L("CONFIRM_DELIVERY");?>" />
		</td>
	</tr>
	<tr>
		<td colspan=5 class="bottomTd"></td>
	</tr>
</table>
</form>

</div>
</body>
</html>
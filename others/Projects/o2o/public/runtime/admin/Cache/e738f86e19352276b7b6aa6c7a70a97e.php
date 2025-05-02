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

<?php function get_money_btn($money,$id)
{
	$str = format_price($money);
	return '<div style="float:left; width:100px;">'.$str.'</div> <input  style="float:left;" type="button" class="button" value="立即打款"  onclick="javascript:charge_edit('.$id.')" />';
}
function get_balance_link($name,$id)
{
	return '<a href="'.u("SupplierBalance/index",array("id"=>$id)).'">'.$name.'</a>';
} ?>
<script type="text/javascript">

function charge_edit(id)
{
	$.weeboxs.open(ROOT+'?m=Supplier&a=charge_edit&supplier_id='+id, {contentType:'ajax',showButton:false,title:"打款确认",width:600,height:195});
}
</script>
<div class="main">
<div class="main_title"> <?php echo ($balance_title); ?>结算报表</div>

<div class="blank5"></div>
<div class="search_row">
	<form name="search" action="__APP__" method="get">	
		商户名称：<input type="text" class="textbox" name="name" value="<?php echo strim($_REQUEST['name']);?>" />		
		<?php echo L("SEARCH_REFERER_TIME");?>：
		<select name="year">
			<?php if(is_array($year_list)): foreach($year_list as $key=>$year): ?><option value="<?php echo ($year["year"]); ?>" <?php if($year['current']): ?>selected="selected"<?php endif; ?>><?php echo ($year["year"]); ?>年</option><?php endforeach; endif; ?>
		</select>
		<select name="month">
			<?php if(is_array($month_list)): foreach($month_list as $key=>$month): ?><option value="<?php echo ($month["month"]); ?>" <?php if($month['current']): ?>selected="selected"<?php endif; ?>><?php echo ($month["month"]); ?>月</option><?php endforeach; endif; ?>
		</select>
		<input type="hidden" value="Balance" name="m" />
		<input type="hidden" value="bill" name="a" />
		<input type="submit" class="button" value="<?php echo L("SEARCH");?>" />
</form>
</div>
<div class="blank5"></div>

<!-- Think 系统列表组件开始 -->
<table id="dataTable" class="dataTable" cellpadding=0 cellspacing=0 ><tr><td colspan="10" class="topTd" >&nbsp; </td></tr><tr class="row" ><th width="50px"><a href="javascript:sortBy('id','<?php echo ($sort); ?>','Balance','bill')" title="按照<?php echo L("ID");?><?php echo ($sortType); ?> "><?php echo L("ID");?><?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('name','<?php echo ($sort); ?>','Balance','bill')" title="按照商户名称<?php echo ($sortType); ?> ">商户名称<?php if(($order)  ==  "name"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('month_sale_money','<?php echo ($sort); ?>','Balance','bill')" title="按照本月营业额<?php echo ($sortType); ?> ">本月营业额<?php if(($order)  ==  "month_sale_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('month_refund_money','<?php echo ($sort); ?>','Balance','bill')" title="按照本月退款<?php echo ($sortType); ?> ">本月退款<?php if(($order)  ==  "month_refund_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('month_money','<?php echo ($sort); ?>','Balance','bill')" title="按照本月消费<?php echo ($sortType); ?> ">本月消费<?php if(($order)  ==  "month_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('sale_money','<?php echo ($sort); ?>','Balance','bill')" title="按照总收入<?php echo ($sortType); ?> ">总收入<?php if(($order)  ==  "sale_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('refund_money','<?php echo ($sort); ?>','Balance','bill')" title="按照退款<?php echo ($sortType); ?> ">退款<?php if(($order)  ==  "refund_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('lock_money','<?php echo ($sort); ?>','Balance','bill')" title="按照未消费<?php echo ($sortType); ?> ">未消费<?php if(($order)  ==  "lock_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('wd_money','<?php echo ($sort); ?>','Balance','bill')" title="按照已付金额<?php echo ($sortType); ?> ">已付金额<?php if(($order)  ==  "wd_money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('money','<?php echo ($sort); ?>','Balance','bill')" title="按照应付余额<?php echo ($sortType); ?> ">应付余额<?php if(($order)  ==  "money"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th></tr><?php if(is_array($list)): $i = 0; $__LIST__ = $list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$sp): ++$i;$mod = ($i % 2 )?><tr class="row" ><td>&nbsp;<?php echo ($sp["id"]); ?></td><td>&nbsp;<?php echo (get_balance_link($sp["name"],$sp['id'])); ?></td><td>&nbsp;<?php echo (format_price($sp["month_sale_money"])); ?></td><td>&nbsp;<?php echo (format_price($sp["month_refund_money"])); ?></td><td>&nbsp;<?php echo (format_price($sp["month_money"])); ?></td><td>&nbsp;<?php echo (format_price($sp["sale_money"])); ?></td><td>&nbsp;<?php echo (format_price($sp["refund_money"])); ?></td><td>&nbsp;<?php echo (format_price($sp["lock_money"])); ?></td><td>&nbsp;<?php echo (format_price($sp["wd_money"])); ?></td><td>&nbsp;<?php echo (get_money_btn($sp["money"],$sp['id'])); ?></td></tr><?php endforeach; endif; else: echo "" ;endif; ?><tr><td colspan="10" class="bottomTd"> &nbsp;</td></tr></table>
<!-- Think 系统列表组件结束 -->
 
<div class="blank5"></div>
<div class="page"><?php echo ($page); ?></div>
</div>
</body>
</html>
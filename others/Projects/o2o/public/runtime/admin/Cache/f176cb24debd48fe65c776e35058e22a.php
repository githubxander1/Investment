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

<?php function get_is_reply($c)
	{
		if($c)return "已回复";
		else
		return "<span style='color:#f30;'>未回复</span>";
	}
	function get_dp_item($id,$dp)
	{
		if($dp['deal_id'])
		{
			return $GLOBALS['db']->getOne("select sub_name from ".DB_PREFIX."deal where id = ".$dp['deal_id']);
		}
		elseif($dp['youhui_id'])
		{
			return $GLOBALS['db']->getOne("select name from ".DB_PREFIX."youhui where id = ".$dp['youhui_id']);
		}
		elseif($dp['event_id'])
		{
			return $GLOBALS['db']->getOne("select name from ".DB_PREFIX."event where id = ".$dp['event_id']);
		}
		else
		{
			return $GLOBALS['db']->getOne("select name from ".DB_PREFIX."supplier_location where id = ".$dp['supplier_location_id']);
		}
	} ?>
<div class="main">
<div class="main_title"><?php echo ($main_title); ?><a href="<?php echo u("SupplierLocation/index");?>" class="back_list"><?php echo L("BACK_LIST");?></a></div>
<div class="blank5"></div>
<div class="button_row">
	<input type="button" class="button" value="<?php echo L("FOREVERDEL");?>" onclick="foreverdel();" />
</div>
<div class="blank5"></div>
<div class="search_row">
	<form name="search" action="__APP__" method="get">	
		类型：<select name="type">
			<option value="all" <?php if($_REQUEST['type'] == 'all'): ?>selected="selected"<?php endif; ?>>全部点评</option>
			<option value="dealdp" <?php if($_REQUEST['type'] == 'dealdp'): ?>selected="selected"<?php endif; ?>>商品或团购点评</option>			
			<option value="youhuidp" <?php if($_REQUEST['type'] == 'youhuidp'): ?>selected="selected"<?php endif; ?>>优惠券点评</option>
			<option value="eventdp" <?php if($_REQUEST['type'] == 'eventdp'): ?>selected="selected"<?php endif; ?>>活动点评</option>		
		</select>
	关键词：<input type="text" class="textbox" name="keyword" value="<?php echo strim($_REQUEST['keyword']);?>" />	
		<input type="hidden" value="SupplierLocationDp" name="m" />
		<input type="hidden" value="index" name="a" />
		<input type="submit" class="button" value="<?php echo L("SEARCH");?>" />
	</form>
</div>
<!-- Think 系统列表组件开始 -->
<table id="checkList" class="dataTable" cellpadding=0 cellspacing=0 ><tr><td colspan="10" class="topTd" >&nbsp; </td></tr><tr class="row" ><th width="8"><input type="checkbox" id="check" onclick="CheckAll('checkList')"></th><th width="80"><a href="javascript:sortBy('id','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照<?php echo L("ID");?><?php echo ($sortType); ?> "><?php echo L("ID");?><?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('title','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照标题<?php echo ($sortType); ?> ">标题<?php if(($order)  ==  "title"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('user_id','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照会员<?php echo ($sortType); ?> ">会员<?php if(($order)  ==  "user_id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('id','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照点评项目<?php echo ($sortType); ?> ">点评项目<?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('is_img','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照有图<?php echo ($sortType); ?> ">有图<?php if(($order)  ==  "is_img"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('create_time','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照发表时间<?php echo ($sortType); ?> ">发表时间<?php if(($order)  ==  "create_time"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('reply_content','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照回复<?php echo ($sortType); ?> ">回复<?php if(($order)  ==  "reply_content"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('is_index','<?php echo ($sort); ?>','SupplierLocationDp','index')" title="按照置顶<?php echo ($sortType); ?> ">置顶<?php if(($order)  ==  "is_index"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th >操作</th></tr><?php if(is_array($list)): $i = 0; $__LIST__ = $list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$dp): ++$i;$mod = ($i % 2 )?><tr class="row" ><td><input type="checkbox" name="key" class="key" value="<?php echo ($dp["id"]); ?>"></td><td>&nbsp;<?php echo ($dp["id"]); ?></td><td>&nbsp;<?php echo (msubstr($dp["title"])); ?></td><td>&nbsp;<?php echo (getUNAME($dp["user_id"])); ?></td><td>&nbsp;<?php echo (get_dp_item($dp["id"],$dp)); ?></td><td>&nbsp;<?php echo (getIsImg($dp["is_img"])); ?></td><td>&nbsp;<?php echo (to_date($dp["create_time"])); ?></td><td>&nbsp;<?php echo (get_is_reply($dp["reply_content"])); ?></td><td>&nbsp;<?php echo (get_toogle_status($dp["is_index"],$dp['id'],is_index)); ?></td><td><a href="javascript:edit('<?php echo ($dp["id"]); ?>')"><?php echo L("EDIT");?></a>&nbsp;<a href="javascript:foreverdel('<?php echo ($dp["id"]); ?>')"><?php echo L("DEL");?></a>&nbsp;</td></tr><?php endforeach; endif; else: echo "" ;endif; ?><tr><td colspan="10" class="bottomTd"> &nbsp;</td></tr></table>
<!-- Think 系统列表组件结束 -->

<div class="blank5"></div>
<div class="page"><?php echo ($page); ?></div>
</div>
</body>
</html>
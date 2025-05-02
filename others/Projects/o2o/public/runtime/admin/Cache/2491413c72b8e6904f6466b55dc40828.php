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

<?php function get_youhui_send_type($type)
	{
		return l("YOUHUI_SEND_TYPE_".$type);
	}
	function get_pub_by($pub_by)
	{
		return l("PUB_BY_".$pub_by);
	}
	function get_brand_name($bid)
	{
		return M("Brand")->where("id=".$bid)->getField("name");
	} ?>
<script type="text/javascript">
	function preview(id)
	{
		window.open("__ROOT__/index.php?ctl=preview&act=youhui&id="+id+"&type=0");
	}
</script>
<div class="main">
<div class="main_title"><?php echo ($main_title); ?></div>
<div class="blank5"></div>
<div class="button_row">
	<input type="button" class="button" value="<?php echo L("ADD");?>" onclick="add();" />
	<input type="button" class="button" value="<?php echo L("DEL");?>" onclick="foreverdel();" />
</div>
<div class="blank5"></div>
<div class="search_row">
	<form name="search" action="__APP__" method="get">	
		名称：<input type="text" class="textbox" name="name" value="<?php echo strim($_REQUEST['name']);?>" />		
		<input type="hidden" value="Youhui" name="m" />
		<input type="hidden" value="index" name="a" />
		<input type="submit" class="button" value="<?php echo L("SEARCH");?>" />
	</form>
</div>
<div class="blank5"></div>
<!-- Think 系统列表组件开始 -->
<table id="dataTable" class="dataTable" cellpadding=0 cellspacing=0 ><tr><td colspan="16" class="topTd" >&nbsp; </td></tr><tr class="row" ><th width="8"><input type="checkbox" id="check" onclick="CheckAll('dataTable')"></th><th width="50px    "><a href="javascript:sortBy('id','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("ID");?><?php echo ($sortType); ?> "><?php echo L("ID");?><?php if(($order)  ==  "id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('name','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("YOUHUI_NAME");?>    <?php echo ($sortType); ?> "><?php echo L("YOUHUI_NAME");?>    <?php if(($order)  ==  "name"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('city_id','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("CITY_NAME");?>     <?php echo ($sortType); ?> "><?php echo L("CITY_NAME");?>     <?php if(($order)  ==  "city_id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('total_num','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("YOUHUI_TOTAL_NUM");?>    <?php echo ($sortType); ?> "><?php echo L("YOUHUI_TOTAL_NUM");?>    <?php if(($order)  ==  "total_num"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('total_fee','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("USE_YOUHUI_FEE");?>    <?php echo ($sortType); ?> "><?php echo L("USE_YOUHUI_FEE");?>    <?php if(($order)  ==  "total_fee"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('user_count','<?php echo ($sort); ?>','Youhui','index')" title="按照总下载量    <?php echo ($sortType); ?> ">总下载量    <?php if(($order)  ==  "user_count"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('is_sms','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("IS_SMS");?>    <?php echo ($sortType); ?> "><?php echo L("IS_SMS");?>    <?php if(($order)  ==  "is_sms"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('user_id','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("EVENT_PUB_USER");?>    <?php echo ($sortType); ?> "><?php echo L("EVENT_PUB_USER");?>    <?php if(($order)  ==  "user_id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('supplier_id','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("SUPPLIER_NAME");?>    <?php echo ($sortType); ?> "><?php echo L("SUPPLIER_NAME");?>    <?php if(($order)  ==  "supplier_id"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('create_time','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("CREATE_TIME");?>    <?php echo ($sortType); ?> "><?php echo L("CREATE_TIME");?>    <?php if(($order)  ==  "create_time"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('pub_by','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("PUB_BY");?>    <?php echo ($sortType); ?> "><?php echo L("PUB_BY");?>    <?php if(($order)  ==  "pub_by"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('is_effect','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("IS_EFFECT");?>    <?php echo ($sortType); ?> "><?php echo L("IS_EFFECT");?>    <?php if(($order)  ==  "is_effect"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('is_recommend','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("IS_RECOMMEND");?>    <?php echo ($sortType); ?> "><?php echo L("IS_RECOMMEND");?>    <?php if(($order)  ==  "is_recommend"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th><a href="javascript:sortBy('sort','<?php echo ($sort); ?>','Youhui','index')" title="按照<?php echo L("SORT");?><?php echo ($sortType); ?> "><?php echo L("SORT");?><?php if(($order)  ==  "sort"): ?><img src="__TMPL__Common/images/<?php echo ($sortImg); ?>.gif" width="12" height="17" border="0" align="absmiddle"><?php endif; ?></a></th><th >操作</th></tr><?php if(is_array($list)): $i = 0; $__LIST__ = $list;if( count($__LIST__)==0 ) : echo "" ;else: foreach($__LIST__ as $key=>$youhui): ++$i;$mod = ($i % 2 )?><tr class="row" ><td><input type="checkbox" name="key" class="key" value="<?php echo ($youhui["id"]); ?>"></td><td>&nbsp;<?php echo ($youhui["id"]); ?></td><td>&nbsp;<?php echo (msubstr($youhui["name"])); ?></td><td>&nbsp;<?php echo (get_city_name($youhui["city_id"])); ?></td><td>&nbsp;<?php echo ($youhui["total_num"]); ?></td><td>&nbsp;<?php echo ($youhui["total_fee"]); ?></td><td>&nbsp;<?php echo ($youhui["user_count"]); ?></td><td>&nbsp;<?php echo (get_status($youhui["is_sms"])); ?></td><td>&nbsp;<?php echo (get_submit_user($youhui["user_id"])); ?></td><td>&nbsp;<?php echo (get_supplier_name($youhui["supplier_id"])); ?></td><td>&nbsp;<?php echo (to_date($youhui["create_time"])); ?></td><td>&nbsp;<?php echo (get_pub_by($youhui["pub_by"])); ?></td><td>&nbsp;<?php echo (get_is_effect($youhui["is_effect"],$youhui['id'])); ?></td><td>&nbsp;<?php echo (get_toogle_status($youhui["is_recommend"],$youhui['id'],is_recommend)); ?></td><td>&nbsp;<?php echo (get_sort($youhui["sort"],$youhui['id'])); ?></td><td><a href="javascript:edit('<?php echo ($youhui["id"]); ?>')"><?php echo L("EDIT");?></a>&nbsp;<a href="javascript: foreverdel('<?php echo ($youhui["id"]); ?>')"><?php echo L("DEL");?></a>&nbsp;<a href="javascript:preview('<?php echo ($youhui["id"]); ?>')">预览</a>&nbsp;</td></tr><?php endforeach; endif; else: echo "" ;endif; ?><tr><td colspan="16" class="bottomTd"> &nbsp;</td></tr></table>
<!-- Think 系统列表组件结束 -->
 

<div class="blank5"></div>
<div class="page"><?php echo ($page); ?></div>
</div>
</body>
</html>
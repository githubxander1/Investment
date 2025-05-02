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

<style type="text/css">
    td span label{float:left; padding:3px; margin:2px; background:#E6E6E6; cursor:pointer; display:inline-block;}
    td span label.active{background:#F60; color:#fff;}
    #container{height:200px; width: 200px; float:left;}  
    #container_front{width: 600px; height:500px; border: 1px solid #000; position: absolute; top: 10px; background-color: #fff; overflow: hidden;}
    #container_m{ width: 550px; height: 450px; margin: 0 auto;}
    #cancel_btn{display: block; width: 600px; height: 18px; line-height: 18px; text-align: right;}
</style>
<?php function get_location_link($id)
	{
		$name = M("SupplierLocation")->where("id=".$id)->getField("name");
		return "<a href='".u("SupplierLocation/edit",array("id"=>$id))."' target='_blank'>".$name."</a>";
	} ?>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=<?php echo app_conf("BAIDU_MAP_APPKEY"); ?>"></script> 
<script type="text/javascript" src="__TMPL__Common/js/map.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/location.js"></script>
<script type="text/javascript">
var blue_point = "__ROOT__/system/blue_point.png";
var red_point = "__ROOT__/system/red_point.png";
	$(document).ready(function(){
		draw_map('<?php echo ($vo["xpoint"]); ?>','<?php echo ($vo["ypoint"]); ?>');		
		$("input[name='supplier_key_btn']").bind("click",function(){
			search_supplier();
		});
	});

</script>

<div class="main">
<div class="main_title"> 查看商家入驻申请 <a href="<?php echo u("SupplierSubmit/index");?>" class="back_list"><?php echo L("BACK_LIST");?></a></div>
<div class="blank5"></div>
<form name="edit" action="__APP__" method="post" enctype="multipart/form-data">
<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>	
	<?php if($vo['location_id'] == 0): ?><tr>
		<td class="item_title">商家名称:</td>
		<td class="item_input"><?php echo ($vo["name"]); ?></td>
	</tr>
	
	<tr>
		<td class="item_title">所属大类:</td>
		<td class="item_input">
		<?php echo ($vo["deal_cate"]); ?>
		</td>
	</tr>	
	<tr>
		<td class="item_title">所属小类:</td>
		<td class="item_input">
			<?php if(is_array($vo["deal_cate_type"])): foreach($vo["deal_cate_type"] as $key=>$type): ?><?php echo ($type["name"]); ?> &nbsp;&nbsp;<?php endforeach; endif; ?>
		</td>
	</tr>
	
	<tr>
		<td class="item_title"><?php echo L("DEAL_CITY");?>:</td>
		<td class="item_input">
		<?php echo ($vo["city"]); ?>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("AREA_LIST");?>:</td>
		<td class="item_input" id="area_list">
			<?php if(is_array($vo["area_list"])): foreach($vo["area_list"] as $key=>$area): ?><?php echo ($area["name"]); ?> &nbsp;&nbsp;<?php endforeach; endif; ?>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_ADDRESS");?>:</td>
		<td class="item_input"><?php echo ($vo["address"]); ?></td>
	</tr>	

	<tr>
		<td class="item_title"><?php echo L("LOCATION_TEL");?>:</td>
		<td class="item_input"><?php echo ($vo["tel"]); ?></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_OPENTIME");?>:</td>
		<td class="item_input"><?php echo ($vo["open_time"]); ?></td>
	</tr>
	
	
	<tr>
            <td class="item_title">地图定位</td>
            <td class="item_input">           	
            	
                <div id="container"></div>
				
            </td>
    </tr>
	
	<tr>
		<td class="item_title">商家logo:</td>
		<td class="item_input"><a href="<?php echo ($vo["h_supplier_logo"]); ?>" target="_blank">查看</a></td>
	</tr>

	<tr>
		<td class="item_title">店面图片:</td>
		<td class="item_input"><a href="<?php echo ($vo["h_supplier_image"]); ?>" target="_blank">查看</a></td>
	</tr><?php endif; ?>
	<tr>
		<td class="item_title">企业名称:</td>
		<td class="item_input"><?php echo ($vo["h_name"]); ?></td>
	</tr>
	
	<tr>
		<td class="item_title">法人:</td>
		<td class="item_input"><?php echo ($vo["h_faren"]); ?></td>
	</tr>
	
	<tr>
		<td class="item_title">营业执照:</td>
		<td class="item_input"><a href="<?php echo ($vo["h_license"]); ?>" target="_blank">查看</a></td>
	</tr>

	<tr>
		<td class="item_title">其他资质:</td>
		<td class="item_input"><a href="<?php echo ($vo["h_other_license"]); ?>" target="_blank">查看</a></td>
	</tr>

		
	<tr>
		<td class="item_title">商户后台手机号:</td>
		<td class="item_input"><?php echo ($vo["account_mobile"]); ?><span class="tip_span">[用于商户管理平台提现，修改资料等操作验证]</span></td>
	</tr>
	<tr>
		<td class="item_title">联系人电话:</td>
		<td class="item_input"><?php echo ($vo["h_tel"]); ?></td>
	</tr>
	
	<tr>
		<td class="item_title">开户行户名:</td>
		<td class="item_input"><?php echo ($vo["h_bank_user"]); ?></td>
	</tr>
	<tr>
		<td class="item_title">开户行名称:</td>
		<td class="item_input"><?php echo ($vo["h_bank_name"]); ?></td>
	</tr>
	<tr>
		<td class="item_title">开户行帐号:</td>
		<td class="item_input"><?php echo ($vo["h_bank_info"]); ?></td>
	</tr>
	
	<tr>
		<td class="item_title">申请会员:</td>
		<td class="item_input"><?php echo ($vo["h_user_name"]); ?></td>
	</tr>	
	

	<tr>
		<td class="item_title"></td>
		<td class="item_input">
			<?php if($vo['is_publish'] == 1): ?>已审核
			<?php else: ?>
			<!--隐藏元素-->
			<input type="hidden" name="id" value="<?php echo ($vo["id"]); ?>" />
			<input type="hidden" name="<?php echo conf("VAR_MODULE");?>" value="SupplierSubmit" />
			<input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="update" />
			<!--隐藏元素-->
			<input type="submit" class="button" value="通过审核" />
			<input type="button" class="button" value="取消" onclick="location.href='<?php echo u("SupplierSubmit/index");?>';" /><?php endif; ?>
			
		</td>
	</tr>
	<tr>
		<td colspan=2 class="bottomTd"></td>
	</tr>
</table>	 
</form>
</div>
</body>
</html>
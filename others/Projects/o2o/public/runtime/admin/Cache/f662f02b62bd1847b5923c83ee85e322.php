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

<script type="text/javascript" src="__TMPL__Common/js/user_edit.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/conf.js"></script>
<div class="main">
<div class="main_title"><?php echo L("EDIT");?> <a href="<?php echo u("User/index");?>" class="back_list"><?php echo L("BACK_LIST");?></a></div>
<div class="blank5"></div>
<form name="edit" action="__APP__" method="post" enctype="multipart/form-data">
<div class="button_row">
	<input type="button" class="button conf_btn" rel="1" value="基本信息" />&nbsp;
	<input type="button" class="button conf_btn" rel="2" value="权限分配" />&nbsp;
</div>
<div class="blank5"></div>
<table class="form conf_tab" cellpadding=0 cellspacing=0 rel="1">
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_NAME");?>:</td>
		<td class="item_input"><input type="<?php if($vo['is_tmp'] == 1): ?>text<?php else: ?>hidden<?php endif; ?>" class="textbox require" name="user_name" value="<?php echo ($vo["user_name"]); ?>" /><?php if($vo['is_tmp'] == 0): ?><?php echo ($vo["user_name"]); ?><?php endif; ?></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_EMAIL");?>:</td>
		<td class="item_input">
			<input type="text" class="textbox" name="email" value="<?php echo ($vo["email"]); ?>" />
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_MOBILE");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="mobile" value="<?php echo ($vo["mobile"]); ?>" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_PASSWORD");?>:</td>
		<td class="item_input"><input type="password" class="textbox" name="user_pwd" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_CONFIRM_PASSWORD");?>:</td>
		<td class="item_input"><input type="password" class="textbox" name="user_confirm_pwd" /></td>
	</tr>
	<tr>
		<td class="item_title">累积积分:</td>
		<td class="item_input"><input type="text" class="textbox" name="total_score" value="<?php echo ($vo["total_score"]); ?>" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_GROUP");?>:</td>
		<td class="item_input">
			<select name="group_id">
				<?php if(is_array($group_list)): foreach($group_list as $key=>$group_item): ?><option value="<?php echo ($group_item["id"]); ?>" <?php if($vo['group_id'] == $group_item['id']): ?>selected="selected"<?php endif; ?>><?php echo ($group_item["name"]); ?></option><?php endforeach; endif; ?>
			</select>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_IS_MERCHANT");?>:</td>
		<td class="item_input">
			<select name="is_merchant">
				<option value="0" <?php if($vo['is_merchant'] == 0): ?>selected="selected"<?php endif; ?>><?php echo L("USER_IS_MERCHANT_0");?></option>
				<option value="1" <?php if($vo['is_merchant'] == 1): ?>selected="selected"<?php endif; ?>><?php echo L("USER_IS_MERCHANT_1");?></option>
			</select>
			<span id="merchant_name">
				<?php echo L("BIND_MERCHANT_NAME");?>：<input type="text" name="merchant_name" class="textbox" value="<?php echo ($vo["merchant_name"]); ?>" />
			</span>
		</td>
	</tr>
	
	<tr>
		<td class="item_title"><?php echo L("USER_IS_DAREN");?>:</td>
		<td class="item_input">
			<select name="is_daren">
				<option value="0" <?php if($vo['is_daren'] == 0): ?>selected="selected"<?php endif; ?>><?php echo L("USER_IS_DAREN_0");?></option>
				<option value="1" <?php if($vo['is_daren'] == 1): ?>selected="selected"<?php endif; ?>><?php echo L("USER_IS_DAREN_1");?></option>
			</select>
			<span id="daren_title">
				<?php echo L("DAREN_TITLE");?>：<input type="text" class="textbox" name="daren_title" value="<?php echo ($vo["daren_title"]); ?>" />
			</span>
		</td>
	</tr>
	<tr id="daren_cate">
		<td class="item_title">达人分类:</td>
		<td class="item_input">
			<?php if(is_array($cate_list)): foreach($cate_list as $key=>$cate_item): ?><label><?php echo ($cate_item["name"]); ?><input type="checkbox" name="cate_id[]" value="<?php echo ($cate_item["id"]); ?>" <?php if($cate_item['checked'] > 0): ?>checked="checked"<?php endif; ?> /></label><?php endforeach; endif; ?>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("USER_BIRTHDAY");?>:</td>
		<td class="item_input">
			<input type="text" name="byear" class="textbox" value="<?php echo ($vo["byear"]); ?>"  style="width:40px" maxlength="4" /><?php echo L("USER_BYEAR");?>
			<input type="text" name="bmonth" class="textbox" value="<?php echo ($vo["bmonth"]); ?>" style="width:20px" maxlength="2"/><?php echo L("USER_BMONTH");?>
			<input type="text" name="bday" class="textbox" value="<?php echo ($vo["bday"]); ?>"  style="width:20px" maxlength="2" /><?php echo L("USER_BDAY");?>
		</td>
	</tr>
	
	<tr>
		<td class="item_title"><?php echo L("IS_EFFECT");?>:</td>
		<td class="item_input">
			<lable><?php echo L("IS_EFFECT_1");?><input type="radio" name="is_effect" value="1" <?php if($vo['is_effect'] == 1): ?>checked="checked"<?php endif; ?> /></lable>
			<lable><?php echo L("IS_EFFECT_0");?><input type="radio" name="is_effect" value="0" <?php if($vo['is_effect'] == 0): ?>checked="checked"<?php endif; ?> /></lable>
		</td>
	</tr>
	<?php if(is_array($field_list)): foreach($field_list as $key=>$field_item): ?><tr>
		<td class="item_title"><?php echo ($field_item["field_show_name"]); ?>:</td>
		<td class="item_input">
			 <?php if($field_item['input_type'] == 0): ?><input type="text" class="textbox <?php if($field_item['is_must'] == 1): ?>require<?php endif; ?>" name="<?php echo ($field_item["field_name"]); ?>" value="<?php echo ($field_item["value"]); ?>" /><?php endif; ?>
			 
			 <?php if($field_item['input_type'] == 1): ?><select name="<?php echo ($field_item["field_name"]); ?>">
			 		<?php if(is_array($field_item["value_scope"])): foreach($field_item["value_scope"] as $key=>$value_item): ?><option value="<?php echo ($value_item); ?>" <?php if($field_item['value'] == $value_item): ?>selected="selected"<?php endif; ?>><?php echo ($value_item); ?></option><?php endforeach; endif; ?>
			 	</select><?php endif; ?>
		</td>
	</tr><?php endforeach; endif; ?>
	
	<tr>
		<td colspan=2 class="bottomTd"></td>
	</tr>
</table>

<table class="form conf_tab" cellpadding=0 cellspacing=0 rel="2">
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>
	<tr>
		<td class="item_title">分享管理:</td>
		<td class="item_input">
			<label>删除分享<input type="checkbox" value="del" name="auth[topic][]" <?php if($auth_list[topic]['del'] == 1): ?>checked="checked"<?php endif; ?> /></label>
			<label>删除回复<input type="checkbox" value="replydel" name="auth[topic][]" <?php if($auth_list[topic]['replydel'] == 1): ?>checked="checked"<?php endif; ?> /></label>
		</td>
	</tr>
	
	<tr>
		<td class="item_title">小组管理:</td>
		<td class="item_input">
			<label>删除<input type="checkbox" value="del" name="auth[group][]"  <?php if($auth_list[group]['del'] == 1): ?>checked="checked"<?php endif; ?>/></label>
			<label>删除回复<input type="checkbox" value="replydel" name="auth[group][]" <?php if($auth_list[group]['replydel'] == 1): ?>checked="checked"<?php endif; ?> /></label>
			<label>置顶<input type="checkbox" value="settop" name="auth[group][]"  <?php if($auth_list[group]['settop'] == 1): ?>checked="checked"<?php endif; ?>/></label>
			<label>推荐<input type="checkbox" value="setbest" name="auth[group][]"  <?php if($auth_list[group]['setbest'] == 1): ?>checked="checked"<?php endif; ?> /></label>
			<label>编辑小组说明<input type="checkbox" value="setmemo" name="auth[group][]"  <?php if($auth_list[group]['setmemo'] == 1): ?>checked="checked"<?php endif; ?> /></label>
		</td>
	</tr>
	<!-- 
	<tr>
		<td class="item_title">商户点评管理:</td>
		<td class="item_input">
			<label>删除<input type="checkbox" value="del" name="auth[dp][]"  <?php if($auth_list[dp]['del'] == 1): ?>checked="checked"<?php endif; ?>/></label>
			<label>删除回复<input type="checkbox" value="replydel" name="auth[dp][]"  <?php if($auth_list[dp]['replydel'] == 1): ?>checked="checked"<?php endif; ?>/></label>
			<label>推荐<input type="checkbox" value="setbest" name="auth[dp][]"  <?php if($auth_list[dp]['setbest'] == 1): ?>checked="checked"<?php endif; ?>/></label>
		</td>
	</tr>
	
	<tr>
		<td class="item_title">其他留言管理:</td>
		<td class="item_input">
			<label>删除<input type="checkbox" value="del" name="auth[msg][]"  <?php if($auth_list[msg]['del'] == 1): ?>checked="checked"<?php endif; ?>/></label>
		</td>
	</tr>		
	 -->	

	
	<tr>
		<td colspan=2 class="bottomTd"></td>
	</tr>
</table>	

<div class="blank5"></div>
	<table class="form" cellpadding=0 cellspacing=0>
		<tr>
			<td colspan=2 class="topTd"></td>
		</tr>
		<tr>
			<td class="item_title"></td>
			<td class="item_input">
			<!--隐藏元素-->
			<input type="hidden" name="id" value="<?php echo ($vo["id"]); ?>" />
			<input type="hidden" name="<?php echo conf("VAR_MODULE");?>" value="User" />
			<input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="update" />
			<!--隐藏元素-->
			<input type="submit" class="button" value="<?php echo L("EDIT");?>" />
			<input type="reset" class="button" value="<?php echo L("RESET");?>" />
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
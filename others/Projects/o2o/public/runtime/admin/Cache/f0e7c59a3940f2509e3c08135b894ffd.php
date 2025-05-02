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
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=<?php echo app_conf("BAIDU_MAP_APPKEY"); ?>"></script> 
<script type="text/javascript" src="__TMPL__Common/js/map.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/location.js"></script>
<script type="text/javascript">
var blue_point = "__ROOT__/system/blue_point.png";
var red_point = "__ROOT__/system/red_point.png";
	$(document).ready(function(){
		 $("input[name='search_api']").bind("click",function(){  
		 	var api_address = $("input[name='api_address']").val();
			var city=$("select[name='city_id']").find("option:selected").attr("rel");
			if ($.trim(api_address) == '') {
				alert("<?php echo L("INPUT_KEY_PLEASE");?>");
			}
			else 
			{
				search_api(api_address, city);
			}
        });
		draw_map('<?php echo ($vo["xpoint"]); ?>','<?php echo ($vo["ypoint"]); ?>');
		$("#container_front").hide();
        $("#cancel_btn").bind("click",function(){ $("#container_front").hide(); });
        $("input[name='chang_api']").bind("click",function(){ 
            editMap($("input[name='xpoint']").attr('value'),$("input[name='ypoint']").attr('value'));
        });
		
		
	});

</script>
<script type="text/javascript" src="__TMPL__Common/js/supplier.js"></script>
<div class="main">
<div class="main_title"> <?php echo L("EDIT_LOCATION");?> <a href="<?php echo u("SupplierLocation/index");?>" class="back_list"><?php echo L("BACK_LIST");?></a></div>
<div class="blank5"></div>
<form name="edit" action="__APP__" method="post" enctype="multipart/form-data">
<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("NAME");?>:</td>
		<td class="item_input"><input type="text" class="textbox require" name="name" value="<?php echo ($vo["name"]); ?>" /></td>
	</tr>
	<tr>
		<td class="item_title">是否支持外卖:</td>
		<td class="item_input">
			<select name="is_dc">
				<option value="0" <?php if($vo["is_dc"] == 0): ?>selected="selected"<?php endif; ?>>否</option>
				<option value="1" <?php if($vo["is_dc"] == 1): ?>selected="selected"<?php endif; ?>>是</option>

			</select>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("TAGS");?>:</td>
		<td class="item_input">
			<input type="text" class="textbox" name="tags"  style="width:50%"  value="<?php echo ($vo["tags"]); ?>" />
			<span class="tip_span">[<?php echo L("ADV_TAGS_TIPS");?>]</span>
		</td>
	</tr>
	<!--<tr>
		<td class="item_title">首页图片:</td>
		<td class="item_input">
			<div style='width:120px; height:40px; margin-left:10px; display:inline-block;  float:left;' class='none_border'><script type='text/javascript'>var eid = 'index_img';KE.show({id : eid,items : ['upload_image'],skinType: 'tinymce',allowFileManager : true,resizeMode : 0});</script><div style='font-size:0px;'><textarea id='index_img' name='index_img' style='width:120px; height:25px;' ><?php echo ($vo["index_img"]); ?></textarea> </div></div><input type='text' id='focus_index_img' style='font-size:0px; border:0px; padding:0px; margin:0px; line-height:0px; width:0px; height:0px;' /></div><img src='<?php if($vo["index_img"] == ''): ?>./admin/Tpl/default/Common/images/no_pic.gif<?php else: ?><?php echo ($vo["index_img"]); ?><?php endif; ?>' <?php if($vo["index_img"] != ''): ?>onclick='openimg("index_img")'<?php endif; ?> style='display:inline-block; float:left; cursor:pointer; margin-left:10px; border:#ccc solid 1px; width:35px; height:35px;' id='img_index_img' /><img src='/o2o/admin/Tpl/default/Common/images/del.gif' style='<?php if($vo["index_img"] == ''): ?>display:none;<?php else: ?>display:inline-block;<?php endif; ?> margin-left:10px; float:left; border:#ccc solid 1px; width:35px; height:35px; cursor:pointer;' id='img_del_index_img' onclick='delimg("index_img")' title='删除' />
		</td>
	</tr>-->
	<tr>
		<td class="item_title"><?php echo L("SUPPLIER_PREVIEW");?>:</td>
		<td class="item_input"><div style='width:120px; height:40px; margin-left:10px; display:inline-block;  float:left;' class='none_border'><script type='text/javascript'>var eid = 'preview';KE.show({id : eid,items : ['upload_image'],skinType: 'tinymce',allowFileManager : true,resizeMode : 0});</script><div style='font-size:0px;'><textarea id='preview' name='preview' style='width:120px; height:25px;' ><?php echo ($vo["preview"]); ?></textarea> </div></div><input type='text' id='focus_preview' style='font-size:0px; border:0px; padding:0px; margin:0px; line-height:0px; width:0px; height:0px;' /></div><img src='<?php if($vo["preview"] == ''): ?>./admin/Tpl/default/Common/images/no_pic.gif<?php else: ?><?php echo ($vo["preview"]); ?><?php endif; ?>' <?php if($vo["preview"] != ''): ?>onclick='openimg("preview")'<?php endif; ?> style='display:inline-block; float:left; cursor:pointer; margin-left:10px; border:#ccc solid 1px; width:35px; height:35px;' id='img_preview' /><img src='/o2o/admin/Tpl/default/Common/images/del.gif' style='<?php if($vo["preview"] == ''): ?>display:none;<?php else: ?>display:inline-block;<?php endif; ?> margin-left:10px; float:left; border:#ccc solid 1px; width:35px; height:35px; cursor:pointer;' id='img_del_preview' onclick='delimg("preview")' title='删除' /></td>
	</tr>	
	<tr>
		<td class="item_title"><?php echo L("SUPPLIER_NAME");?>:</td>
		<td class="item_input">
			<span id="supplier_list">
			<select name="supplier_id">
				<option value="0"><?php echo L("EMPTY_SELECT_SUPPLIER");?></option>
				<?php if($supplier_info): ?><option value="<?php echo ($supplier_info["id"]); ?>" selected="selected"><?php echo ($supplier_info["name"]); ?></option><?php endif; ?>
			</select>
			</span>
			<input type="text" class="textbox" name="supplier_key" /> 
			<input type="button" name="supplier_key_btn" class="button" value="<?php echo L("SEARCH");?>" />
			<span class="tip_span"><?php echo L("AUTO_CREATE");?></span>
		</td>
	</tr>
	<!--<tr>
		<td class="item_title"><?php echo L("LOCATION_BRAND");?>:</td>
		<td class="item_input">
			<?php if(is_array($brand_list)): foreach($brand_list as $key=>$brand): ?><label>
					<input type="checkbox" name="brand_id[]" value="<?php echo ($brand["id"]); ?>" <?php if($brand['checked']): ?>checked="checked"<?php endif; ?> />
					<?php echo ($brand["name"]); ?>
				</label><?php endforeach; endif; ?>
		</td>
	</tr>-->
	<tr>
		<td class="item_title"><?php echo L("DEAL_CITY");?>:</td>
		<td class="item_input">
		<select name="city_id">
			<?php if(is_array($city_list)): foreach($city_list as $key=>$city_item): ?><option value="<?php echo ($city_item["id"]); ?>" rel="<?php echo ($city_item["name"]); ?>" <?php if($vo['city_id'] == $city_item['id']): ?>selected="selected"<?php endif; ?> <?php if($city_item['pid'] == 0): ?>disabled="disabled"<?php endif; ?>><?php echo ($city_item["title_show"]); ?></option><?php endforeach; endif; ?>
		</select>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("AREA_LIST");?>:</td>
		<td class="item_input" id="area_list">
			
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("DEAL_CATE_TREE");?>:</td>
		<td class="item_input">
		<select name="deal_cate_id">
			<option value="0">==非生活服务商户==</option>
			<?php if(is_array($deal_cate_tree)): foreach($deal_cate_tree as $key=>$cate_item): ?><option value="<?php echo ($cate_item["id"]); ?>" <?php if($vo['deal_cate_id'] == $cate_item['id']): ?>selected="selected"<?php endif; ?>><?php echo ($cate_item["title_show"]); ?></option><?php endforeach; endif; ?>
		</select>
		</td>
	</tr>	
	<tr id="sub_cate_box">
		<td class="item_title"><?php echo L("DEALCATETYPE_INDEX");?>:</td>
		<td class="item_input">
			
		</td>
	</tr>
	<tr id="tag_group_preset">
		<td class="item_title">商户标签设置</td>
		<td class="item_input">
			
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("IS_MAIN");?>:</td>
		<td class="item_input">
			<select name="is_main">
				<option value="1" <?php if($vo[is_main] == 1): ?>selected="selected"<?php endif; ?> ><?php echo L("YES");?></option>
				<option value="0" <?php if($vo[is_main] == 0): ?>selected="selected"<?php endif; ?> ><?php echo L("NO");?></option>				
			</select>
			<span class="tip_span">[<?php echo L("IS_MAIN_TIP");?>]</span>
		</td>
	</tr>
	
	<tr>
		<td class="item_title"><?php echo L("LOCATION_ADDRESS");?>:</td>
		<td class="item_input"><input class="textbox" name="address" style="width:50%" value="<?php echo ($vo["address"]); ?>" /></td>
	</tr>	
	<tr>
		<td class="item_title"><?php echo L("LOCATION_ROUTE");?>:</td>
		<td class="item_input"><textarea class="textarea" name="route" ><?php echo ($vo["route"]); ?></textarea></td>
	</tr>	
	<tr>
		<td class="item_title"><?php echo L("LOCATION_TEL");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="tel" value="<?php echo ($vo["tel"]); ?>" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_CONTACT");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="contact" value="<?php echo ($vo["contact"]); ?>" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_OPENTIME");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="open_time" value="<?php echo ($vo["open_time"]); ?>"  /></td>
	</tr>
	<tr>
            <td class="item_title">地图定位</td>
            <td class="item_input">            	
            	关键词：<input type="text" class="textbox" name="api_address" value="" /> 
				<input type="button" value="查找" class="button" name="search_api" id="search_api" >
				<div style="height:10px; clear:both;"></div>
                <div id="container"></div>
				<div style="height:10px; clear:both;"></div>
                <script type="text/javascript"></script> 
                <input type="button" value="手动修改" name="chang_api" id="chang_api">
                <div style="position:relative; top:-400px;">
                    <div  id="container_front">
                        <a href="#" id="cancel_btn">取消</a>
                        <div id="container_m"></div>
                    </div>
                </div>
				<input type="hidden" name="xpoint" value="<?php echo ($vo["xpoint"]); ?>" />
				<input type="hidden" name="ypoint" value="<?php echo ($vo["ypoint"]); ?>" />
            </td>
    </tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_BRIEF");?>:</td>
		<td class="item_input">
		 <script type='text/javascript'> var eid = 'brief';KE.show({id : eid,skinType: 'tinymce',allowFileManager : true,resizeMode : 0,items : [
							'source','fullscreen', 'undo', 'redo', 'print', 'cut', 'copy', 'paste',
							'plainpaste', 'wordpaste', 'justifyleft', 'justifycenter', 'justifyright',
							'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', 'subscript',
							'superscript', 'selectall', '-',
							'title', 'fontname', 'fontsize', 'textcolor', 'bgcolor', 'bold',
							'italic', 'underline', 'strikethrough', 'removeformat', 'image',
							'flash', 'media', 'table', 'hr', 'emoticons', 'link', 'unlink'
						]});</script><div  style='margin-bottom:5px; '><textarea id='brief' name='brief' style='width:750px; height:350px;' ><?php echo ($vo["brief"]); ?></textarea> </div>
		</td>
	</tr>
	<tr>
		<td class="item_title">手机端列表简介:</td>
		<td class="item_input"><textarea class="textarea" name="mobile_brief" ><?php echo ($vo["mobile_brief"]); ?></textarea></td>
	</tr>
	<!--<tr>
		<td class="item_title">短信内容:</td>
		<td class="item_input">
		 <textarea id="sms_content" style="width:300px;height:80px" name="sms_content" ><?php echo ($vo["sms_content"]); ?></textarea><br>
		 <span class="tip_span">[若不填发送的短信内容为：名称+电话+地址]</span>
		</td>
	</tr>-->
	<tr>
		<td class="item_title">总评分预设值[0-5]:</td>
		<td class="item_input">
		 <input type="text" class="textbox" id="avg_point" name="avg_point" value="<?php echo ($vo["avg_point"]); ?>" />
		</td>
	</tr>
	<tr>
		<td class="item_title">好评预设值[0-1]:</td>
		<td class="item_input">
		 <input type="text" class="textbox" id="good_rate" name="good_rate" value="<?php echo ($vo["good_rate"]); ?>" />
		</td>
	</tr>
	<tr>
		<td class="item_title">SEO标题:</td>
		<td class="item_input"><textarea class="textarea" name="seo_title" ><?php echo ($vo["seo_title"]); ?></textarea></td>
	</tr>
	<tr>
		<td class="item_title">SEO关键词:</td>
		<td class="item_input"><textarea class="textarea" name="seo_keyword" ><?php echo ($vo["seo_keyword"]); ?></textarea></td>
	</tr>
	<tr>
		<td class="item_title">SEO描述:</td>
		<td class="item_input"><textarea class="textarea" name="seo_description" ><?php echo ($vo["seo_description"]); ?></textarea></td>
	</tr>
	
	<tr>
		<td class="item_title"><?php echo L("IS_RECOMMEND");?>:</td>
		<td class="item_input">
			<select name="is_recommend">
				<option value="0" <?php if($vo['is_recommend'] == 0): ?>selected="selected"<?php endif; ?>>否</option>
				<option value="1" <?php if($vo['is_recommend'] == 1): ?>selected="selected"<?php endif; ?>>是</option>
			</select>
		</td>
	</tr>
	<tr>
		<td class="item_title"></td>
		<td class="item_input">
			<!--隐藏元素-->
			<input type="hidden" name="id" value="<?php echo ($vo["id"]); ?>" />
			<input type="hidden" name="location_id" value="<?php echo ($vo["location_id"]); ?>" />
			<input type="hidden" name="edit_type" value="2" />
			<input type="hidden" name="<?php echo conf("VAR_MODULE");?>" value="SupplierLocation" />
			<?php if(($vo["biz_apply_status"] == 2) AND ($vo["location_id"] > 0) ): ?><input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="update" />
			<?php elseif($vo["biz_apply_status"] == 1): ?>
				<input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="insert" /><?php endif; ?>
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
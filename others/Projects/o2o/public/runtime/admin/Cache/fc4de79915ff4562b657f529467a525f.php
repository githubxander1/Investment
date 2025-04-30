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
    .cbox_div{
	width:110px;display:inline-block;float:left;
    }
</style>
<script type="text/javascript" src="__TMPL__Common/js/calendar/calendar.php?lang=zh-cn" ></script>
<link rel="stylesheet" type="text/css" href="__TMPL__Common/js/calendar/calendar.css" />
<script type="text/javascript" src="__TMPL__Common/js/calendar/calendar.js"></script>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=<?php echo app_conf("BAIDU_MAP_APPKEY"); ?>"></script> 
<script type="text/javascript" src="__TMPL__Common/js/conf.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/map.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/location.js"></script>
<script type="text/javascript" src="__TMPL__Common/js/dc.js"></script>
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
		draw_map('0','0');
		$("#container_front").hide();
        $("#cancel_btn").bind("click",function(){ $("#container_front").hide(); });
        $("input[name='chang_api']").bind("click",function(){ 
            editMap($("input[name='xpoint']").attr('value'),$("input[name='ypoint']").attr('value'));
        });
		

	});

</script>
<script type="text/javascript" src="__TMPL__Common/js/supplier.js"></script>
<div class="main">
<div class="main_title"><?php echo L("ADD_LOCATION");?> <a href="<?php echo u("SupplierLocation/index");?>" class="back_list"><?php echo L("BACK_LIST");?></a></div>
<div class="blank5"></div>
<form name="edit" action="__APP__" method="post" enctype="multipart/form-data">
<div class="button_row">
	<input type="button" class="button conf_btn" rel="1" value="<?php echo L("STORE_BASE_INFO");?>" />&nbsp;
	<input type="button" class="button conf_btn" rel="2" value="<?php echo L("STORE_CERTIFICATION_RECOMMEND");?>" />&nbsp;
	<input type="button" class="button conf_btn" rel="3" value="<?php echo L("DC_MANAGE");?>" />&nbsp;	
	<input type="button" class="button conf_btn" rel="4" value="<?php echo L("SEO_CONFIG");?>" />&nbsp;	
</div>
<div class="blank5"></div>
<table class="form conf_tab" rel="1" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("NAME");?>:</td>
		<td class="item_input"><input type="text" class="textbox require" name="name" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("TAGS");?>:</td>
		<td class="item_input">
			<input type="text" class="textbox" name="tags"  style="width:50%"  />
			<span class="tip_span">[<?php echo L("ADV_TAGS_TIPS");?>]</span>
		</td>
	</tr>
	<!--<tr>
		<td class="item_title">首页图片:</td>
		<td class="item_input">
			<div style='width:120px; height:40px; margin-left:10px; display:inline-block;  float:left;' class='none_border'><script type='text/javascript'>var eid = 'index_img';KE.show({id : eid,items : ['upload_image'],skinType: 'tinymce',allowFileManager : true,resizeMode : 0});</script><div style='font-size:0px;'><textarea id='index_img' name='index_img' style='width:120px; height:25px;' ></textarea> </div><input type='text' id='focus_index_img' style='font-size:0px; border:0px; padding:0px; margin:0px; line-height:0px; width:0px; height:0px;' /></div><img src='./admin/Tpl/default/Common/images/no_pic.gif'  style='display:inline-block; float:left; cursor:pointer; margin-left:10px; border:#ccc solid 1px; width:35px; height:35px;' id='img_index_img' /><img src='/o2o/admin/Tpl/default/Common/images/del.gif' style='display:none; margin-left:10px; float:left; border:#ccc solid 1px; width:35px; height:35px; cursor:pointer;' id='img_del_index_img' onclick='delimg("index_img")' title='删除' />
		</td>
	</tr>-->
	<tr>
		<td class="item_title"><?php echo L("SUPPLIER_PREVIEW");?>:</td>
		<td class="item_input"><div style='width:120px; height:40px; margin-left:10px; display:inline-block;  float:left;' class='none_border'><script type='text/javascript'>var eid = 'preview';KE.show({id : eid,items : ['upload_image'],skinType: 'tinymce',allowFileManager : true,resizeMode : 0});</script><div style='font-size:0px;'><textarea id='preview' name='preview' style='width:120px; height:25px;' ></textarea> </div><input type='text' id='focus_preview' style='font-size:0px; border:0px; padding:0px; margin:0px; line-height:0px; width:0px; height:0px;' /></div><img src='./admin/Tpl/default/Common/images/no_pic.gif'  style='display:inline-block; float:left; cursor:pointer; margin-left:10px; border:#ccc solid 1px; width:35px; height:35px;' id='img_preview' /><img src='/o2o/admin/Tpl/default/Common/images/del.gif' style='display:none; margin-left:10px; float:left; border:#ccc solid 1px; width:35px; height:35px; cursor:pointer;' id='img_del_preview' onclick='delimg("preview")' title='删除' /></td>
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
					<input type="checkbox" name="brand_id[]" value="<?php echo ($brand["id"]); ?>" />
					<?php echo ($brand["name"]); ?>
				</label><?php endforeach; endif; ?>
		</td>
	</tr>-->
	<tr>
		<td class="item_title"><?php echo L("DEAL_CITY");?>:</td>
		<td class="item_input">
		<select name="city_id">
			<?php if(is_array($city_list)): foreach($city_list as $key=>$city_item): ?><option value="<?php echo ($city_item["id"]); ?>" rel="<?php echo ($city_item["name"]); ?>" <?php if($city_item['pid'] == 0): ?>disabled="disabled"<?php endif; ?>><?php echo ($city_item["title_show"]); ?></option><?php endforeach; endif; ?>
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
			<?php if(is_array($deal_cate_tree)): foreach($deal_cate_tree as $key=>$cate_item): ?><option value="<?php echo ($cate_item["id"]); ?>"><?php echo ($cate_item["title_show"]); ?></option><?php endforeach; endif; ?>
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
				<option value="1"><?php echo L("YES");?></option>
				<option value="0"><?php echo L("NO");?></option>				
			</select>
			<span class="tip_span">[<?php echo L("IS_MAIN_TIP");?>]</span>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_ADDRESS");?>:</td>
		<td class="item_input"><input class="textbox" name="address" style="width:50%" /></td>
	</tr>	
	<tr>
		<td class="item_title"><?php echo L("LOCATION_ROUTE");?>:</td>
		<td class="item_input"><textarea class="textarea" name="route" ></textarea></td>
	</tr>	
	<tr>
		<td class="item_title"><?php echo L("LOCATION_TEL");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="tel" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_CONTACT");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="contact" /></td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("LOCATION_OPENTIME");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="open_time" /></td>
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
				<input type="hidden" name="xpoint" />
				<input type="hidden" name="ypoint" />
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
						]});</script><div  style='margin-bottom:5px; '><textarea id='brief' name='brief' style='width:750px; height:350px;' ></textarea> </div>
		</td>
	</tr>
	<tr>
		<td class="item_title">手机端列表简介:</td>
		<td class="item_input"><textarea class="textarea" name="mobile_brief"></textarea></td>
	</tr>
	<!--<tr>
		<td class="item_title">短信内容:</td>
		<td class="item_input">
		 <textarea id="sms_content" style="width:300px;height:80px" name="sms_content" ></textarea><br>
		 <span class="tip_span">[若不填发送的短信内容为：名称+电话+地址]</span>
		</td>
	</tr>-->
	<tr>
		<td class="item_title">总评分预设值[0-5]:</td>
		<td class="item_input">
		 <input type="text" id="avg_point" name="avg_point" class="textbox" value="0" />
		</td>
	</tr>
	<tr>
		<td class="item_title">好评预设值[0-1]:</td>
		<td class="item_input">
		 <input type="text" class="textbox" id="good_rate" name="good_rate" value="0" />
		</td>
	</tr>
	<tr >
		<td class="item_title">门店顶部广告位:</td>
		<td class="item_input">
			 <script type='text/javascript'> var eid = 'adv_img_1';KE.show({id : eid,skinType: 'tinymce',allowFileManager : true,resizeMode : 0,items : [
							'source','fullscreen', 'undo', 'redo', 'print', 'cut', 'copy', 'paste',
							'plainpaste', 'wordpaste', 'justifyleft', 'justifycenter', 'justifyright',
							'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', 'subscript',
							'superscript', 'selectall', '-',
							'title', 'fontname', 'fontsize', 'textcolor', 'bgcolor', 'bold',
							'italic', 'underline', 'strikethrough', 'removeformat', 'image',
							'flash', 'media', 'table', 'hr', 'emoticons', 'link', 'unlink'
						]});</script><div  style='margin-bottom:5px; '><textarea id='adv_img_1' name='adv_img_1' style='width:750px; height:350px;' ></textarea> </div>
		</td>
	</tr>
	<tr>
		<td class="item_title">门店侧边广告位:</td>
		<td class="item_input">
			 <script type='text/javascript'> var eid = 'adv_img_2';KE.show({id : eid,skinType: 'tinymce',allowFileManager : true,resizeMode : 0,items : [
							'source','fullscreen', 'undo', 'redo', 'print', 'cut', 'copy', 'paste',
							'plainpaste', 'wordpaste', 'justifyleft', 'justifycenter', 'justifyright',
							'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', 'subscript',
							'superscript', 'selectall', '-',
							'title', 'fontname', 'fontsize', 'textcolor', 'bgcolor', 'bold',
							'italic', 'underline', 'strikethrough', 'removeformat', 'image',
							'flash', 'media', 'table', 'hr', 'emoticons', 'link', 'unlink'
						]});</script><div  style='margin-bottom:5px; '><textarea id='adv_img_2' name='adv_img_2' style='width:750px; height:350px;' ></textarea> </div>
		</td>
	</tr>
	<tr>
		<td class="item_title">门店客服QQ:</td>
		<td class="item_input">
		 <input type="text" id="location_qq" name="location_qq" class="textbox" value="" />
		</td>
	</tr>
</table>
<table class="form conf_tab" rel="2" cellpadding=0 cellspacing=0>
	<tr>
		<td class="item_title">首页推荐:</td>
		<td class="item_input">
			<label><input type="checkbox" name="is_recommend" value="1" ></label>
		</td>
	</tr>
	<tr>
		<td class="item_title"><?php echo L("IS_VERIFY_SHOP");?></td>
		<td class="item_input">
			<label><input type="checkbox" name="is_verify" value="1" ></label>
		</td>
	</tr>
	
	<tr>
		<td class="item_title">营业执照:</td>
		<td class="item_input">
			<div style='width:120px; height:40px; margin-left:10px; display:inline-block;  float:left;' class='none_border'><script type='text/javascript'>var eid = 'biz_license';KE.show({id : eid,items : ['upload_image'],skinType: 'tinymce',allowFileManager : true,resizeMode : 0});</script><div style='font-size:0px;'><textarea id='biz_license' name='biz_license' style='width:120px; height:25px;' ><?php echo ($vo["biz_license"]); ?></textarea> </div></div><input type='text' id='focus_biz_license' style='font-size:0px; border:0px; padding:0px; margin:0px; line-height:0px; width:0px; height:0px;' /></div><img src='<?php if($vo["biz_license"] == ''): ?>./admin/Tpl/default/Common/images/no_pic.gif<?php else: ?><?php echo ($vo["biz_license"]); ?><?php endif; ?>' <?php if($vo["biz_license"] != ''): ?>onclick='openimg("biz_license")'<?php endif; ?> style='display:inline-block; float:left; cursor:pointer; margin-left:10px; border:#ccc solid 1px; width:35px; height:35px;' id='img_biz_license' /><img src='/o2o/admin/Tpl/default/Common/images/del.gif' style='<?php if($vo["biz_license"] == ''): ?>display:none;<?php else: ?>display:inline-block;<?php endif; ?> margin-left:10px; float:left; border:#ccc solid 1px; width:35px; height:35px; cursor:pointer;' id='img_del_biz_license' onclick='delimg("biz_license")' title='删除' />
		</td>
	</tr>
	
	<tr>
		<td class="item_title">其他资质:</td>
		<td class="item_input">
			<div style='width:120px; height:40px; margin-left:10px; display:inline-block;  float:left;' class='none_border'><script type='text/javascript'>var eid = 'biz_other_license';KE.show({id : eid,items : ['upload_image'],skinType: 'tinymce',allowFileManager : true,resizeMode : 0});</script><div style='font-size:0px;'><textarea id='biz_other_license' name='biz_other_license' style='width:120px; height:25px;' ><?php echo ($vo["biz_other_license"]); ?></textarea> </div></div><input type='text' id='focus_biz_other_license' style='font-size:0px; border:0px; padding:0px; margin:0px; line-height:0px; width:0px; height:0px;' /></div><img src='<?php if($vo["biz_other_license"] == ''): ?>./admin/Tpl/default/Common/images/no_pic.gif<?php else: ?><?php echo ($vo["biz_other_license"]); ?><?php endif; ?>' <?php if($vo["biz_other_license"] != ''): ?>onclick='openimg("biz_other_license")'<?php endif; ?> style='display:inline-block; float:left; cursor:pointer; margin-left:10px; border:#ccc solid 1px; width:35px; height:35px;' id='img_biz_other_license' /><img src='/o2o/admin/Tpl/default/Common/images/del.gif' style='<?php if($vo["biz_other_license"] == ''): ?>display:none;<?php else: ?>display:inline-block;<?php endif; ?> margin-left:10px; float:left; border:#ccc solid 1px; width:35px; height:35px; cursor:pointer;' id='img_del_biz_other_license' onclick='delimg("biz_other_license")' title='删除' />
		</td>
	</tr>
</table>
<table class="form conf_tab" rel="3" cellpadding=0 cellspacing=0>
	<tr>
		<td class="item_title">服务类型:</td>
		<td class="item_input">
			<label class="cbox_div"><input type="checkbox" name="is_dc" value="1">外卖</label>		
			<label class="cbox_div"><input type="checkbox" name="is_reserve" value="1">预订</label>
		</td>
	</tr>
		
	<tr id="dc_cate">
		<td class="item_title"><?php echo L("DCCATE_INDEX");?>:</td>
		<td class="item_input">
			<?php if($dc_cate_list): ?><?php if(is_array($dc_cate_list)): foreach($dc_cate_list as $key=>$dc_cate): ?><label class="cbox_div">
				<input type="checkbox" value="<?php echo ($dc_cate["id"]); ?>" name="dc_cate[]"><?php echo ($dc_cate["name"]); ?>
				</label><?php endforeach; endif; ?>
			<?php else: ?>
			<a href="<?php echo u("DcCate/index");?>">暂无分类，请先添加餐厅分类</a><?php endif; ?>
			
		</td>
	</tr>
	
	
	<tr id="forbid_online_pay_box">
			<td class="item_title">支付方式：</td>
			<td class="item_input">
			<label class="cbox_div"><input type="checkbox" name="dc_online_pay" value="1">在线支付</label>
			
			<label class="cbox_div"><input type="checkbox" name="dc_allow_cod" value="1">货到付款</label>
			</td>
		</tr>
		<tr id="dc_allow_refund_box">
			<td class="item_title">额外服务：</td>
			<td class="item_input">
			<label class="cbox_div"><input type="checkbox" value="1" name="dc_allow_invoice" >支持发票</label>
			<label class="cbox_div"><input type="checkbox" value="1" name="dc_allow_ecv" >支持代金劵</label>
			</td>
		</tr>
		<tr id="balance_type_box">
			<td class="item_title" >平台提成方式:</td>
			<td class="item_input">
				<select name="balance_type" >
					<option value="0">按百分比</option>
					<option value="1">按单</option>								
				</select>
			</td>		
		</tr>
		<tr id="balance_amount_box">
			<td class="item_title">提成设置:</td>
			<td class="item_input">
				<input type="text" name="balance_amount"  value="<?php echo ($vo['balance_amount']); ?>">
					<span class="b_number"><?php if($vo['balance_type'] == 0): ?>例：网站收取每笔订单20%做为提成，填写 0.2，不能超过1<?php else: ?>元，不能超过10元<?php endif; ?></span>
			</td>
		</tr>
		<tr>
			<td class="item_title">营业状态:</td>
			<td class="item_input">
				<label class="cbox_div"><input type="radio" name="is_close" value="0" checked="checked">营业中</label>
				<label class="cbox_div"><input type="radio" name="is_close" value="1">暂停营业</label>
			</td>
		</tr>
	<tr>
		<td class="item_title">营业时间:</td>
		<td class="item_input">
				<div class="open_time_box">
				<span><a href="javascript:void(0);" onclick="add_open_time();">[+]</a>:&nbsp;</span><span class="tip_span">默认24小时营业</span>
				<?php echo ($open_time_html); ?>
			</div>
		</td>
	</tr>

	<tr id="takeaway_box" <?php if($vo['is_dc'] == 0): ?>style="display:none"<?php endif; ?>>
		<td class="item_title">配送信息:</td>
		<td class="item_input">
				<div class="delivery_price_box">
				<span><a href="javascript:void(0);" onclick="add_delivery_price();">[+]</a>:&nbsp;</span><span class="tip_span">默认不收配送费</span>
				<?php echo ($delivery_price_html); ?>
			</div>
		</td>
	</tr>
	<tr id="takeaway_box" <?php if($vo['is_dc'] == 0): ?>style="display:none"<?php endif; ?>>
		<td class="item_title">包装费信息:</td>
		<td class="item_input">
			基础价:<input type="text" class="textbox" name="package_start_price" value="<?php echo (round($package_price["package_start_price"],2)); ?>"  />&nbsp;<span class="tip_span">0:为不收打包费，-1:全收打包费，大于0:小于该值，收取打包费;大于该值，不收打包费 </span><br>
			打包费:<input type="text" class="textbox" name="package_price" value="<?php echo (round($package_price["package_price"],2)); ?>"  />&nbsp;元<span class="tip_span">（每样菜的打包费） </span>
		</td>
	</tr>
	
	<tr id="takeaway_box" <?php if($vo['is_dc'] == 0): ?>style="display:none"<?php endif; ?>>
		<td class="item_title">促销活动:</td>
		<td class="item_input">
			<label class="cbox_div"><input type="checkbox" value="1" name="is_firstorderdiscount" >首单立减</label>
			<label class="cbox_div"><input type="checkbox" value="1" name="is_payonlinediscount" >在线支付优惠</label>
		</td>
	</tr>
	<tr>
		<td class="item_title">商家公告:</td>
		 <td class="item_input"><textarea class="textarea" name="dc_location_notice" ></textarea></td>
	</tr>
	
</table>
<table class="form conf_tab" rel="4" cellpadding=0 cellspacing=0>
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
	
</table>
<div class="blank5"></div>
<table id="location" class="form" cellpadding=0 cellspacing=0>
		<tr>
			<td colspan=2 class="topTd"></td>
		</tr>	 
	<tr>
		<td class="item_title"></td>
		<td class="item_input">
			<!--隐藏元素-->			
			<input type="hidden" name="<?php echo conf("VAR_MODULE");?>" value="SupplierLocation" />
			<input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="insert" />
			<!--隐藏元素-->
			<input type="submit" class="button" value="<?php echo L("ADD");?>" />
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
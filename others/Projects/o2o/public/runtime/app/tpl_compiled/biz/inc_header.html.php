<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="Generator" />

<?php 
$k = array (
  'name' => 'load_compatible',
);
echo $k['name']();
?>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title><?php if ($this->_var['page_title']): ?><?php echo $this->_var['page_title']; ?> - <?php endif; ?><?php echo $this->_var['site_seo']['title']; ?>商家中心</title>
<meta name="keywords" content="<?php if ($this->_var['page_keyword']): ?><?php echo $this->_var['page_keyword']; ?><?php else: ?><?php echo $this->_var['site_seo']['keyword']; ?><?php endif; ?>商家中心" />
<meta name="description" content="<?php if ($this->_var['page_description']): ?><?php echo $this->_var['page_description']; ?><?php else: ?><?php echo $this->_var['site_seo']['description']; ?><?php endif; ?>商家中心" />
<script type="text/javascript">
var APP_ROOT = '<?php echo $this->_var['APP_ROOT']; ?>';
<?php if (app_conf ( "APP_MSG_SENDER_OPEN" ) == 1): ?>
var send_span = <?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'SEND_SPAN',
);
echo $k['name']($k['v']);
?>000;
var IS_RUN_CRON = 1;
var DEAL_MSG_URL = '<?php
echo parse_url_tag("u:index|cron#deal_msg_list|"."".""); 
?>';
<?php endif; ?>
var AJAX_URL	= '<?php
echo parse_url_tag("u:biz|ajax|"."".""); 
?>';

//关于图片上传的定义
var LOADER_IMG = '<?php echo $this->_var['TMPL']; ?>/images/loader_img.gif';
var LOADER_IMG_GIF = '<?php echo $this->_var['TMPL']; ?>/images/css_bg/loading.gif';
var UPLOAD_SWF = '<?php echo $this->_var['TMPL']; ?>/js/utils/Moxie.swf';
var UPLOAD_XAP = '<?php echo $this->_var['TMPL']; ?>/js/utils/Moxie.xap';
var MAX_IMAGE_SIZE = '<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'MAX_IMAGE_SIZE',
);
echo $k['name']($k['v']);
?>';
var MAX_SP_IMAGE = '<?php echo MAX_SP_IMAGE; ?>';
var ALLOW_IMAGE_EXT = '<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'ALLOW_IMAGE_EXT',
);
echo $k['name']($k['v']);
?>';
var UPLOAD_URL = '<?php
echo parse_url_tag("u:biz|file#upload|"."".""); 
?>';

//关于编辑器上传的定义
var K_UPLOAD_URL = "<?php
echo parse_url_tag("u:biz|file#upload|"."".""); 
?>";
var K_BASE_PATH = '<?php echo $this->_var['TMPL']; ?>/js/utils/kindeditor/';
var K_THEMES_PATH = '<?php echo $this->_var['TMPL']; ?>/css/utils/kindeditor/';

var OFC_SWF = '<?php echo $this->_var['TMPL']; ?>/js/open-flash-chart.swf';
</script>
<?php
//前台队列功能开启
if(app_conf("APP_MSG_SENDER_OPEN")==1)
{
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/msg_sender.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/msg_sender.js";
}
?>
<script type="text/javascript" src="<?php echo $this->_var['APP_ROOT']; ?>/public/runtime/app/lang.js"></script>
<link rel="stylesheet" type="text/css" href="<?php 
$k = array (
  'name' => 'parse_css',
  'v' => $this->_var['pagecss'],
);
echo $k['name']($k['v']);
?>" />
<script type="text/javascript" src="<?php 
$k = array (
  'name' => 'parse_script',
  'v' => $this->_var['pagejs'],
  'c' => $this->_var['cpagejs'],
);
echo $k['name']($k['v'],$k['c']);
?>"></script>

</head>
<body>
<!-- 顶部横栏 -->
<div class="biz_header">
	<div class="head_box wrap_full">
		<a class="logo f_l" href="<?php
echo parse_url_tag("u:index|index|"."".""); 
?>"><h1><?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'SHOP_TITLE',
);
echo $k['name']($k['v']);
?>商户管理平台</h1></a>
		<ul class="head_nav">
			<?php 
$k = array (
  'name' => 'load_biz_user_tip',
);
echo $this->_hash . $k['name'] . '|' . base64_encode(serialize($k)) . $this->_hash;
?>
		</ul>

	</div>
</div>
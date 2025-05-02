<?php
//本页不引用header.html， 直接在页面内编写单独header
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/msg_page.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/msg_page.js";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="Generator" />
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title><?php if ($this->_var['page_title']): ?><?php echo $this->_var['page_title']; ?> - <?php endif; ?><?php echo $this->_var['site_seo']['title']; ?></title>
<meta name="keywords" content="<?php if ($this->_var['page_keyword']): ?><?php echo $this->_var['page_keyword']; ?><?php else: ?><?php echo $this->_var['site_seo']['keyword']; ?><?php endif; ?>" />
<meta name="description" content="<?php if ($this->_var['page_description']): ?><?php echo $this->_var['page_description']; ?><?php else: ?><?php echo $this->_var['site_seo']['description']; ?><?php endif; ?>" />
<script type="text/javascript">
var APP_ROOT = '<?php echo $this->_var['APP_ROOT']; ?>';
var CART_URL = '<?php
echo parse_url_tag("u:index|cart|"."".""); 
?>';
var CART_CHECK_URL = '<?php
echo parse_url_tag("u:index|cart#check|"."".""); 
?>';
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
var AJAX_LOGIN_URL	= '<?php
echo parse_url_tag("u:index|user#ajax_login|"."".""); 
?>';
var AJAX_URL	= '<?php
echo parse_url_tag("u:index|ajax|"."".""); 
?>';
var LOADER_IMG = '<?php echo $this->_var['TMPL']; ?>/images/loader_img.gif';
var order_id = <?php 
$k = array (
  'name' => 'intval',
  'value' => $this->_var['order_info']['id'],
);
echo $k['name']($k['value']);
?>;
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
<script type="text/javascript" src="<?php echo $this->_var['APP_ROOT']; ?>/public/runtime/region.js"></script>	
</head>
<body>
<img src="<?php echo $this->_var['TMPL']; ?>/images/loader_img.gif" style="display:none;" /><!--延时加载的替代图片生成-->
<div class="top_nav">
	<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
		<span class="f_l">欢迎来到<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'SHOP_TITLE',
);
echo $k['name']($k['v']);
?></span>	
		<span class="f_r">
			<ul class="head_tip">
				<li class="cart_tip" id="cart_tip"><?php 
$k = array (
  'name' => 'load_cart_count',
);
echo $this->_hash . $k['name'] . '|' . base64_encode(serialize($k)) . $this->_hash;
?></li>
				<li class="user_tip" id="head_user_tip"><?php 
$k = array (
  'name' => 'load_user_tip',
);
echo $this->_hash . $k['name'] . '|' . base64_encode(serialize($k)) . $this->_hash;
?></li>
			</ul>
		</span>
	</div>
</div><!--顶部横栏-->
<div class="blank15"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> head_main">
	<div class="logo f_l">
	<a class="link" href="<?php echo $this->_var['APP_ROOT']; ?>/">
		<?php
			$this->_var['logo_image'] = app_conf("SHOP_LOGO");
		?>
		<?php 
$k = array (
  'name' => 'load_page_png',
  'v' => $this->_var['logo_image'],
);
echo $k['name']($k['v']);
?>
	</a>
	</div>
	
</div><!--logo与头部搜索-->

<div class="blank20"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">

	<div class="layout_box msg_box">
		<div class="title"><?php echo $this->_var['page_title']; ?></div>
		<div class="content">
			<div>
			<?php echo $this->_var['msg']; ?>
			</div>
			<?php if ($this->_var['stay'] == 0): ?>
			<div class="jump_tip">				
				系统将在 <span>5</span> 秒后自动跳转，或者直接点击 [<a href="<?php echo $this->_var['jump']; ?>">这里</a>] 直接返回			
			</div>
			<?php else: ?>
			<div class="jump_tip">
				请点击 [<a href="<?php echo $this->_var['jump']; ?>">这里</a>] 返回
			</div>
			<?php endif; ?>
		</div>
	</div>

</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
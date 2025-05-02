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
var CITY_COUNT	= <?php echo $this->_var['city_count']; ?>;

//关于图片上传的定义
var LOADER_IMG = '<?php echo $this->_var['TMPL']; ?>/images/loader_img.gif';
var UPLOAD_SWF = '<?php echo $this->_var['TMPL']; ?>/js/utils/Moxie.swf';
var UPLOAD_XAP = '<?php echo $this->_var['TMPL']; ?>/js/utils/Moxie.xap';
var MAX_IMAGE_SIZE = '<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'MAX_IMAGE_SIZE',
);
echo $k['name']($k['v']);
?>';
var ALLOW_IMAGE_EXT = '<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'ALLOW_IMAGE_EXT',
);
echo $k['name']($k['v']);
?>';
var UPLOAD_URL = '<?php
echo parse_url_tag("u:index|file#upload|"."".""); 
?>';
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
<div class="head_main user_head theme_morning">
	<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> cm_hd">
		<a href="<?php
echo parse_url_tag("u:index|index|"."".""); 
?>"  style="font-size: 24px;font-family: "Microsoft YaHei" ! important;"><i class="iconfont" style="font-size: 40px;color: #f80;">&#xe635;</i>个人主页</a>
		<div class="btn_group" <?php echo $this->_var['is_why']; ?>>
				<?php if ($this->_var['is_why'] == 1): ?>
				<a href="javascript:void(0);" onclick="$.fast_publish()"  class="publish_btn"><i>发布</i></a>	
				<?php elseif ($this->_var['is_why'] == 2): ?>
				<a href="<?php
echo parse_url_tag("u:index|uc_home#index|"."".""); 
?>" class="back_home"><i class="iconfont">&#xe61e;</i>&nbsp;返回我的主页</a>
				<?php endif; ?>
		</div>
	</div>
	<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> ">
		<div class="user_info_box">
			<div class="u_img">
				<?php 
$k = array (
  'name' => 'show_avatar',
  'id' => $this->_var['home_user_info']['id'],
  'type' => 'middle',
  'is_card' => '0',
);
echo $k['name']($k['id'],$k['type'],$k['is_card']);
?>
			</div>
			<div class="u_info u_info_bg">
				<div class="info">
					<p class="line">
						<strong class="name"><?php echo $this->_var['home_user_info']['user_name']; ?></strong><?php if ($this->_var['home_user_info']['is_merchant'] == 1): ?><span class="is_merchant" title="认证商家"></span><?php endif; ?><?php if ($this->_var['home_user_info']['is_daren'] == 1): ?><span class="is_daren" title="分享达人"></span><?php endif; ?>
					</p>
					<p class="line">
						<?php if ($this->_var['home_user_info']['sex'] == 1): ?><i class="iconfont sex_1">&#xe637;</i>男<?php elseif ($this->_var['home_user_info']['sex'] == - 1): ?><i class="iconfont">&#xe639;</i>保密<?php else: ?><i class="iconfont sex_0">&#xe638;</i>女<?php endif; ?> <?php if ($this->_var['home_user_info']['is_daren'] == 1): ?><i class="dot"></i> <?php echo $this->_var['home_user_info']['daren_title']; ?> <?php endif; ?> <?php if ($this->_var['user_location']): ?> <i class="dot"></i><?php echo $this->_var['user_location']; ?><?php endif; ?>
						
					</p>
					<p class="line medal">
						<?php $_from = $this->_var['home_user_info']['medal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'medal');if (count($_from)):
    foreach ($_from AS $this->_var['medal']):
?>
							<a href="<?php
echo parse_url_tag("u:index|uc_medal|"."".""); 
?>" title="<?php echo $this->_var['medal']['name']; ?>"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['medal']['icon'],
  'w' => '20',
  'h' => '20',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" align="absmiddle" /></a>	
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					</p>
				</div>
				<div class="sns">
					<?php if ($this->_var['is_why'] == 1): ?>
					<p class="line edit_btn"><button class="ui-button edit_link_btn" rel="white" act="<?php
echo parse_url_tag("u:index|uc_myinfo#index|"."".""); 
?>" type="button">账户中心</button></p>
					
					<?php elseif ($this->_var['is_why'] == 2 || $this->_var['is_why'] == 3): ?>
					<a class="fav_btn <?php if ($this->_var['is_fav']): ?>fav_checked<?php endif; ?>" href="javascript:void(0);" onclick="$.fav_btn(<?php echo $this->_var['home_user_info']['id']; ?>,this)">
						<ul>
							<li><i class="iconfont">&#xe626;</i>关注</li>
							<li>关注 +1</li>
							<li><i class="iconfont">&#xe62d;</i>已关注</li>
							<li>取消关注</li>
						</ul>
					</a>
					<?php endif; ?>
					<br/>
					<ul class="ff_count">
						<li class="atten_item fans">
							<a href="<?php
echo parse_url_tag("u:index|uc_home#uc_fans_list|"."id=".$this->_var['home_user_info']['id']."".""); 
?>">
							<p class="atten_link">
								<strong><?php echo $this->_var['home_user_info']['focused_count']; ?></strong>
								<span>粉丝</span>
							</p>
							</a>
						</li> 
						<li class="atten_item follow">
							<a href="<?php
echo parse_url_tag("u:index|uc_home#uc_follow_list|"."id=".$this->_var['home_user_info']['id']."".""); 
?>">
							<p class="atten_link">
								<strong><?php echo $this->_var['home_user_info']['focus_count']; ?></strong>
								<span>关注</span>
							</p>
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</div><!--头部个人信息-->
	<div class="user_nav_box">
		<div class="user_nav_con <?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
			<ul>
				<?php $_from = $this->_var['uc_nav']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'nav');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['nav']):
?>
					<li class="nav_item <?php if ($this->_var['ACTION_NAME'] == $this->_var['key']): ?>current<?php endif; ?>"><a class="nav_link" href="<?php echo $this->_var['nav']['url']; ?>"><?php echo $this->_var['nav']['name']; ?></a><i class="top_triangle"></i></li>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</ul>
			<div class="back_index_link"><a href="<?php
echo parse_url_tag("u:index|index|"."".""); 
?>"><i class="iconfont">&#xe61e;</i>返回首页</a></div>
		</div>
		
	</div>
</div>
<div class="blank15"></div>



<?php
//本页不引用header.html， 直接在页面内编写单独header
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/cart_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/cart_check.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/cart_check.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/cart_check.js";
?>

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
	<div class="cart_step f_r">
		<ul>
			<li>1. 提交订单</li>
			<li class="current">2. 选择支付方式</li>
			<li>3. 购买成功</li>
		</ul>
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

<form name="cart_form" id="cart_form" action="<?php if ($this->_var['order_info']): ?><?php
echo parse_url_tag("u:index|cart#order_done|"."".""); 
?><?php else: ?><?php
echo parse_url_tag("u:index|cart#done|"."".""); 
?><?php endif; ?>" method="post">

<div class="cart_row">
<div class="cart_table">
		
		<table>
			<tr>
				<th class="w_name">项目</th>
				<th class="w_unit">单价</th>
				<th class="w_num">数量</th>
				<th class="w_total">总价</th>
			</tr>
			<?php $_from = $this->_var['cart_list_group']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'cart_item_group');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['cart_item_group']):
?>
			<?php if ($this->_var['cart_item_group']['supplier']): ?>
			<tr class="cart_supplier_title">
				<td colspan=2 class="tl"><?php echo $this->_var['cart_item_group']['supplier']; ?></td>
				<td colspan=2 class="tr"><span id="delivery_fee_<?php echo $this->_var['key']; ?>"></span></td>
			</tr>
			<?php endif; ?>
			<?php $_from = $this->_var['cart_item_group']['goods_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'cart_item');if (count($_from)):
    foreach ($_from AS $this->_var['cart_item']):
?>
				<tr rel="<?php echo $this->_var['cart_item']['id']; ?>">
					<td class="w_name">
						<div class="cart_img">
							<a href="<?php echo $this->_var['cart_item']['url']; ?>" target="_blank" title="<?php echo $this->_var['cart_item']['name']; ?>"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['cart_item']['icon'],
  'w' => '50',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" alt="<?php echo $this->_var['cart_item']['name']; ?>"  style="width:50px;height:50px;" /></a>
						</div>
						<div class="cart_name">
							<a href="<?php echo $this->_var['cart_item']['url']; ?>" target="_blank" title="<?php echo $this->_var['cart_item']['name']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['cart_item']['name'],
  'b' => '0',
  'e' => '70',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a>
						</div>
					</td>
					<td class="w_unit">
						<?php if ($this->_var['cart_item']['buy_type'] != 1): ?>
						&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['cart_item']['unit_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?>
						<?php else: ?>
						<?php 
$k = array (
  'name' => 'abs',
  'v' => $this->_var['cart_item']['return_score'],
);
echo $k['name']($k['v']);
?>积分
						<?php endif; ?>
					</td>
					<td class="w_num">
						<?php echo $this->_var['cart_item']['number']; ?>
					</td>
					<td class="w_total">
						<?php if ($this->_var['cart_item']['buy_type'] != 1): ?>
						&yen;<span><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['cart_item']['total_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
						<?php else: ?>
						<span><?php 
$k = array (
  'name' => 'abs',
  'v' => $this->_var['cart_item']['return_total_score'],
);
echo $k['name']($k['v']);
?></span>积分					
						<?php endif; ?>
					</td>
				</tr>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</table>
		
</div>
</div>




<div class="blank"></div>
<?php if ($this->_var['is_delivery']): ?>
<div class="cart_row layout_box">
	<div class="title">
		<div class="f_l"><?php
echo lang("CONSIGNEE_INFO"); 
?></div>	
		<?php if ($this->_var['consignee_count'] > 1): ?>
		<div class="f_r modify_consignee"><a href="javascript:void(0);" id="modify_consignee">修改</a></div>	
		<?php endif; ?>
	</div>
	<div class="content">
		<div id="cart_consignee" rel="<?php echo $this->_var['consignee_id']; ?>"></div>
	</div>
</div>
<div class="blank"></div>
<div class="cart_row layout_box">
	<div class="title"><?php echo $this->_var['LANG']['DELIVERY_INFO']; ?></div>
	<div class="content">
		<div id="cart_delivery"></div>
	</div>
</div>
<?php endif; ?>




<div class="blank"></div>
<div id="cart_memo">
<div class="cart_row layout_box">
	<div class="title"><?php
echo lang("ORDER_MEMO"); 
?></div>
	<div class="content">
		<textarea id="memo" name="memo" class="ui-textbox" holder="选填：对本次交易的说明，建议先与客服咨询沟通"><?php echo $this->_var['order_info']['memo']; ?></textarea>
	</div>
</div>
</div>




<?php if ($this->_var['show_payment']): ?>
<div class="blank"></div>
<div id="cart_payment">
<div class="cart_row layout_box">
	<div class="title"><?php
echo lang("PAYMENT_INFO"); 
?></div>
	<div class="content">
		<?php if ($this->_var['bank_paylist']): ?>
		<?php $_from = $this->_var['bank_paylist']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'payment_item');if (count($_from)):
    foreach ($_from AS $this->_var['payment_item']):
?>	
			<?php echo $this->_var['payment_item']['display_code']; ?>											
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>	
		<div class="blank"></div>
		<?php endif; ?>
		<?php if ($this->_var['icon_paylist']): ?>
		<?php $_from = $this->_var['icon_paylist']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'payment_item');if (count($_from)):
    foreach ($_from AS $this->_var['payment_item']):
?>	
			<?php echo $this->_var['payment_item']['display_code']; ?>											
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>	
		<div class="blank"></div>
		<?php endif; ?>
		<?php $_from = $this->_var['disp_paylist']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'payment_item');if (count($_from)):
    foreach ($_from AS $this->_var['payment_item']):
?>	
			<?php echo $this->_var['payment_item']['display_code']; ?>	
			<div class="blank"></div>										
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>	
	</div>
</div>
</div>
<?php endif; ?>



<div class="blank"></div>
<div class="cart_row layout_box clearfix">
	
	
	<div id="user_mobile">
	<?php if ($this->_var['user_info']['mobile']): ?>
	<input type="hidden" name="user_mobile" value="<?php echo $this->_var['user_info']['mobile']; ?>" />
	<?php else: ?>
	<div class="form_panel">
	<div class="panel">
		
			<dl>
				<dt>手机号</dt>
				<dd>
					<input class="ui-textbox" name="user_mobile" value="" holder="请输入手机号" />
					<span class="form_tip"></span>
				</dd>
			</dl>
			<?php if (app_conf ( "SMS_ON" ) == 1): ?>
			<dl class="ph_img_verify" <?php if ($this->_var['sms_ipcount'] > 1): ?>style="display:block"<?php endif; ?>>
				<dt>图片验证码</dt>
				<dd>
					<input type="text" name="verify_code" class="ui-textbox img_verify" holder="请输入图片文字" />
					<img src="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" class="verify" rel="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" />
					<a href="javascript:void(0);" class="refresh_verify">看不清楚？换一张！</a>
					<span class="form_tip"></span>
				</dd>
			</dl>
					
			<dl>
				<dt>验证码</dt>
				<dd>
					<input class="ui-textbox ph_verify" name="sms_verify" holder="请输入验证码" />
					<button class="ui-button f_l light ph_verify_btn" rel="light" form_prefix="<?php echo $this->_var['form_prefix']; ?>" lesstime="<?php echo $this->_var['sms_lesstime']; ?>" type="button">发送验证码</button>
					
					<span class="form_tip"></span>
				</dd>
			</dl>
			<?php endif; ?>

		</div>
		</div>
	<?php endif; ?>
	</div>
	
	
	
	<div id="cart_total">
	</div>
	
	<div class="blank"></div>
	<div id="cart_submit">
		<input type="hidden" value="<?php 
$k = array (
  'name' => 'intval',
  'value' => $this->_var['order_info']['id'],
);
echo $k['name']($k['value']);
?>" name="id" />
		<input type="hidden" name="hd_is_coupon" value="<?php echo $this->_var['is_coupon']; ?>">
		<button id="order_done" class="ui-button f_r" rel="blue" type="button"><?php echo $this->_var['LANG']['CONFIRM_ORDER_AND_PAY']; ?></button>	
	</div><!--cart_submit-->	

</div>


</form>

</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
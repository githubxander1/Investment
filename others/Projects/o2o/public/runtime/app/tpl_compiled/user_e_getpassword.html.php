<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/getpassword_page.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/user_getpassword.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/user_getpassword.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>
<div class="blank20"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">

	
	<div class="layout_box">	
	<div class="title">邮箱找回密码</div>
	<div class="content clearfix" id="getpassword_form">	
		<div class="form_panel">
		<div class="panel">
		<form name="getpassword_form" class="getpassword" method="post" action="<?php
echo parse_url_tag("u:index|user#dogetpassword|"."".""); 
?>">
			
			<dl>
				<dt>邮箱</dt>
				<dd>
					<input class="ui-textbox" name="getpassword_email" holder="请输入您用来登录的 Email地址" />
					<span class="form_tip"></span>
				</dd>
			</dl>			
			<dl>
				<dt>图片验证码</dt>
				<dd>
					<input type="text" name="verify_code" class="ui-textbox img_verify" holder="请输入图片文字" />
					<img src="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" class="verify" rel="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" />
					<a href="javascript:void(0);" class="refresh_verify">看不清楚？换一张！</a>
					<span class="form_tip"></span>
				</dd>
			</dl>
			<dl>
				<dt></dt>
				<dd>

					<button class="ui-button orange f_l" rel="orange" type="submit">找回密码</button>
				</dd>
			</dl>
			
		</form>
		</div>
		</div>
	</div><!--end content-->
	</div>
	

</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
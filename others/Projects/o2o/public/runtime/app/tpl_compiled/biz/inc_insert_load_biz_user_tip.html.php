	<?php if ($this->_var['account_info']): ?>
	<li class="option"><a href="<?php
echo parse_url_tag("u:biz|index|"."".""); 
?>">【<?php echo $this->_var['supplier_name']; ?>】 <?php echo $this->_var['account_info']['account_name']; ?><i class="vertical-bar"></i></a></li>
	<li class="option"><a href="<?php
echo parse_url_tag("u:biz|user#logout|"."".""); 
?>">退出<i class="vertical-bar"></i></a></li>
	<li class="option"><a href="<?php
echo parse_url_tag("u:biz|user#edit_password|"."".""); 
?>">修改密码<i class="vertical-bar"></i></a></li>
	<?php else: ?>
	<li class="option"><a href="<?php
echo parse_url_tag("u:biz|user#login|"."".""); 
?>">登录<i class="vertical-bar"></i></a></li>
	<?php endif; ?>

	<li class="option"><a href="<?php
echo parse_url_tag("u:index|index|"."".""); 
?>">回到首页<i class="vertical-bar"></i></a></li>
	<li class="option option-qrcode">
		<a>下载商家手机客户端</a>
		<i class="triangle"></i>
		<div class="qrcode-box">
			<a href="javascript:void(0);"><img src="<?php echo $this->_var['biz_gen_qrcode']; ?>" /></a>
			<span class="qrcode-text">手机版验证快捷更方便</span>
			<div class="blank"></div>
		</div>
	</li>
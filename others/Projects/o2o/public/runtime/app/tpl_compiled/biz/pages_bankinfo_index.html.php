<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/bankinfo.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery-1.8.2.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/bankinfo/bankinfo.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/bankinfo/bankinfo.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
SMS_URL = "<?php
echo parse_url_tag("u:biz|bankinfo#biz_sms_code|"."".""); 
?>";
</script>
<div class="blank20"></div>
<div class="page wrap_full">
	<div class="left_box">
		<?php echo $this->fetch('inc/biz_nav_list.html'); ?>
	</div>
	<div class="right_box">
		<div class="content">
			<div class="head_box">
				<h2><?php echo $this->_var['head_title']; ?></h2>
			</div>



			<div class="info_box">
				<div class="blank20"></div>

				<div class="bg_box growth_content">
					
					<div class="info_items">
						<ul>
							<li><label>商户名称：</label><span class="main_color"><?php echo $this->_var['supplier_info']['name']; ?></span></li>
						</ul>
					</div>
				</div>
			</div>


			<div class="blank20"></div>

		
			<div id="withdraw">
		
					<form name="withdraw_form" action="<?php
echo parse_url_tag("u:biz|bankinfo#update|"."".""); 
?>" method="post" />	
					<div class="info_table">
					<table>
						<tr>
							<td class="withdraw">
								开户行名称
							</td>
							<td class="withcontent">
								<input type="text" name="bank_name" class="ui-textbox"  value="<?php echo $this->_var['supplier_info']['bank_name']; ?>" />
							</td>
						</tr>
						<tr>
							<td class="withdraw">
								开户行账号
							</td>
							<td class="withcontent">
								<input type="text" name="bank_num" class="ui-textbox"  value="<?php echo $this->_var['supplier_info']['bank_info']; ?>" />
							</td>
						</tr>
						<tr>
							<td class="withdraw">
								真实姓名
							</td>
							<td class="withcontent">
								<input type="text" name="bank_user" class="ui-textbox"  value="<?php echo $this->_var['supplier_info']['bank_user']; ?>" />
							</td>
						</tr>

						<?php if (app_conf ( "SMS_ON" ) == 1): ?>
						<tr>
							<td class="withdraw">
								请输入验证码
							</td>
							<td class="withcontent">
								<input class="ui-textbox f_l ph_verify" id="sms_verify" name="sms_verify"  />
								<button class="ui-button f_l light ph_verify_btn" rel="light" lesstime="<?php echo $this->_var['sms_lesstime']; ?>" type="button">发送验证码</button>
							</td>
						</tr>
						
						<tr  class="ph_img_verify" <?php if ($this->_var['sms_ipcount'] > 1): ?>style="display:table-row;*display:block;"<?php endif; ?>>
							<td class="withdraw">
								图片验证码
							</td>

							<td class="withcontent img_verify_box">
								<input type="text" id="verify_code" name="verify_code" class="ui-textbox img_verify f_l"  />
								<img src="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" class="verify f_l" rel="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" />
								<a href="javascript:void(0);" class="refresh_verify f_l">看不清楚？换一张！</a>
							</td>
						</tr>
						<?php else: ?>
						<tr>
							<td class="withdraw">
								登入密码
							</td>
							<td class="withcontent">
								<input type="password" name="pwd" class="ui-textbox" holder="请输入密码" />
							</td>
						</tr>
						<?php endif; ?>
						<tr>		
							<td colspan=2><button class="ui-button orange" rel="orange" type="submit">修改</button></td>
						</tr>
					</table>
					</div>
					</form>					
	
			</div><!--end form-->

			<div class="blank20"></div>


			
		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
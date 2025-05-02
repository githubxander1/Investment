<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/withdrawal.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/withdrawal/withdrawal.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/withdrawal/withdrawal.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
SMS_URL = "<?php
echo parse_url_tag("u:biz|withdrawal#biz_sms_code|"."".""); 
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
							<li><label>当前可提现余额：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['money'],
);
echo $k['name']($k['v']);
?></span></li>							
							<li><label>提现银行名称：</label><span class="main_color"><?php echo $this->_var['supplier_info']['bank_name']; ?></span></li>								
							<li><label>提现银行账号：</label><span class="main_color"><?php echo $this->_var['supplier_info']['bank_info']; ?></span></li>

						</ul>
					</div>
				</div>
			</div>


			<div class="blank20"></div>

		
			<div id="withdraw">		
					<form name="withdraw_form" action="<?php
echo parse_url_tag("u:biz|withdrawal#withdraw_done|"."".""); 
?>" method="post" />	
					<div class="info_table">
						
							<div class="field_group_long">
								<label class="f_label">提现金额</label> 
								<div class="f_text">
									<input type="text" name="money"  class="ui-textbox normal" holder="提现金额（元）" />
								</div>				
								<div class="clear"></div>
							</div>	
						
							<?php if (app_conf ( "SMS_ON" ) == 1): ?>
							<!--防止多次短信验证手机号图片验证-->
							<div class="field_group_long ph_img_verify" <?php if ($this->_var['sms_ipcount'] > 1): ?>style="display:block"<?php endif; ?>>
								<label class="f_label">图片验证码</label> 
								<div class="img_verify_box">
									<div class="f_text">
										<input type="text" id="verify_code" name="verify_code" class="ui-textbox img_verify " holder="请输入验证码" />
									</div>
									<img src="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" class="verify f_l" rel="<?php echo $this->_var['APP_ROOT']; ?>/verify.php" />
									<a href="javascript:void(0);" class="refresh_verify f_l">看不清楚？换一张！</a>
								</div>
								<div class="status_icon hide"> <i class=""></i></div>
								<div class="clear"></div>
							</div>
							
							<div class="field_group_long">
								<label class="f_label">手机验证码</label> 
								<div class="sms_verify_box">
									<div class="f_text">
									<input class="ui-textbox  ph_verify" id="sms_verify" name="sms_verify" holder="请输入验证码" />
									</div>
									<button class="ui-button f_l light ph_verify_btn" rel="light" lesstime="<?php echo $this->_var['sms_lesstime']; ?>" type="button">发送验证码</button>
									
								</div>
								<div class="status_icon hide"> <i class=""></i></div>
								<div class="clear"></div>
							</div>						
							<?php else: ?>
							<div class="field_group_long">
								<label class="f_label">登入密码</label> 
								<div class="f_text">
								<input type="password" name="pwd"  class="ui-textbox normal f_text " holder="请输入密码" />		
								</div>		
								<div class="clear"></div>
							</div>	
							<?php endif; ?>
						
							<div class="field_group_long">
								<button class="ui-button " rel="orange" type="submit">提交申请</button>
								<div class="clear"></div>
							</div>
					</div>
					</form>		
			</div>

			<div class="blank20"></div>
		
			
			<?php if ($this->_var['list']): ?>
			<div class="info_table">
			
				<h3>提现记录</h3>
				<div class="blank20"></div>
				<table>
					<tbody>
						<tr>
							<th>提现时间</th>
							<th>提现金额</th>
							<th>状态</th>
							

						</tr>
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
						<tr class="alt">
                               <td><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['create_time'],
);
echo $k['name']($k['v']);
?></td>
                               <td  class="detail"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['money'],
);
echo $k['name']($k['v']);
?></td>
                               <td><?php echo $this->_var['item']['status']; ?></td>                               
                         </tr>
                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                          

					</tbody>
				</table>
				
			</div>	
			
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>			
			<?php else: ?>
			<div class="empty_tip">没有提现记录</div>
			<?php endif; ?>			
		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
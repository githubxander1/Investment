<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/verify.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/verify.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/verify.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
	var ajax_url = '<?php
echo parse_url_tag("u:biz|dealv|"."".""); 
?>';
</script>
<div class="blank20"></div>
<div class="page wrap_full">
	<div class="left_box">
		<?php echo $this->fetch('inc/biz_nav_list.html'); ?>
	</div>
	<div class="right_box">
		<div class="content content_hastab">
			<div class="standard_tab cf">
				<ul>
					<li class="<?php if ($this->_var['ACTION_NAME'] == 'index'): ?>curr<?php endif; ?>"><a href="<?php
echo parse_url_tag("u:biz|dealv#index|"."".""); 
?>">团购券验证</a></li>
					<li class="<?php if ($this->_var['ACTION_NAME'] == 'batch'): ?>curr<?php endif; ?>"><a href="<?php
echo parse_url_tag("u:biz|dealv#batch|"."".""); 
?>">团购券批量验证</a></li>
					<li class="<?php if ($this->_var['ACTION_NAME'] == 'super'): ?>curr<?php endif; ?>"><a href="<?php
echo parse_url_tag("u:biz|dealv#super|"."".""); 
?>">超级验证</a></li>
				</ul>
			</div>
			<div class="verify_content">
				<form id="verify_form" name="verify_form" method="post" action="<?php
echo parse_url_tag("u:biz|dealv#check_coupon|"."".""); 
?>">
					<div class="verify_box group_box">
						<h3>选择门店</h3>
						<div class="blank10"></div>
						<div class="field_select">
							<select name="location_id" class="ui-select ">
								<?php $_from = $this->_var['location_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
									<option value="<?php echo $this->_var['row']['id']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['row']['name'],
  'l' => '0',
  'e' => '10',
);
echo $k['name']($k['v'],$k['l'],$k['e']);
?></option>
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							</select>
						</div>
						<div class="blank10"></div>
						<h3>请先验证团购券，再接待</h3>
						<div class="blank10"></div>
						<div class="form_field">
							<div class="f_text"><input type="text" name="coupon_pwd" id="coupon_pwd" value="" class="ui-textbox " holder="请输入验证码" /></div>							
						</div>
						<div class="verify_btn">
							<button class="ui-button" rel="orange" type="submit">验证团购券</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
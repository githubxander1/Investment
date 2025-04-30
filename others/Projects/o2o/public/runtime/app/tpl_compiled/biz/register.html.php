<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/user.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/plupload.full.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user_register.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user_register.js";

?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
UPLOAD_URL = "<?php
echo parse_url_tag("u:biz|file#user_register_upload|"."".""); 
?>";
</script>
<div class="wrap_full msg_tip_box">
		<div class="msg_tip">
			<i class="status"></i>
			<p class="msg_content"></p>
			<span class="close"></span>
		</div>
</div>
<div class="blank20"></div>
<div class="bdw">
<div class=" wrap_full">
	<div class="box_main">
		<div class="box_head">
			<h2>商家入驻</h2>
			<div class="step_tip">
				<ul class="step_list">
					<li class="step_item <?php if ($this->_var['step'] == 1): ?>curr<?php elseif ($this->_var['step'] > 1): ?>passed<?php else: ?>tobe<?php endif; ?>"><span>入驻须知</span></li>
					<li class="step_item <?php if ($this->_var['step'] == 2): ?>curr<?php elseif ($this->_var['step'] > 2): ?>passed<?php else: ?>tobe<?php endif; ?>" ><span>门店信息</span></li>
					<li class="step_item <?php if ($this->_var['step'] == 3): ?>curr<?php elseif ($this->_var['step'] > 3): ?>passed<?php else: ?>tobe<?php endif; ?>" ><span>填写信息</span></li>
					<li class="step_item <?php if ($this->_var['step'] == 4): ?>curr<?php elseif ($this->_var['step'] < 4): ?>tobe<?php endif; ?>"><span>等待审核</span></li>
				</ul>
			</div>
		</div>
		<div class="box_form">
			<?php if ($this->_var['step'] == 2): ?>
				<?php echo $this->fetch('inc/register_step2.html'); ?>
			<?php elseif ($this->_var['step'] == 3): ?>
				<?php echo $this->fetch('inc/register_step3.html'); ?>
			<?php elseif ($this->_var['step'] == 4): ?>
				<?php echo $this->fetch('inc/register_step4.html'); ?>
			<?php else: ?>
				<?php echo $this->fetch('inc/register_step1.html'); ?>
			<?php endif; ?>
			<div class="blank"></div>
		</div>
	</div>
</div>
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
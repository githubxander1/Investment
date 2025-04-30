<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/project.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/project/project.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/project/project.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
var ajax_url = '<?php echo $this->_var['ajax_url']; ?>';
</script>
<div class="blank20"></div>
<div class="page wrap_full">
	<div class="left_box">
		<?php echo $this->fetch('inc/biz_nav_list.html'); ?>
	</div>
	<div class="right_box">
		<div class="content">
			<div class="head_box clearfix">
				<h2 class="f_l"><?php echo $this->_var['page_title']; ?></h2>
				<div class="publish_project_btn f_r">
					<a href="<?php echo $this->_var['publish_btn_url']; ?>">
						<button class="ui-button testformbtn" rel="orange" type="button">发布</button>
					</a>
				</div>
			</div>
			<div class="blank50"></div>
			<div class="form_box  content_hastab">
				<div class="standard_tab cf">
					<ul>
						<li class="<?php if ($this->_var['ACTION_NAME'] == 'index'): ?>curr<?php endif; ?>"><a href="<?php echo $this->_var['index_url']; ?>">已发布上线</a></li>
						<li class="<?php if ($this->_var['ACTION_NAME'] == 'no_online_index'): ?>curr<?php endif; ?>"><a href="<?php echo $this->_var['no_online_index_url']; ?>">审核记录</a></li>
					</ul>
				</div>
				<form name="project_form" action="<?php echo $this->_var['form_url']; ?>" method="post">
					<?php echo $this->fetch('pages/location/data_list_box.html'); ?>
				</form>
			</div>
		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
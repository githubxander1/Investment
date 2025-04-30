<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_home_index.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/publish.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/pin_layout.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/pin_box.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/login_page.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/user_header.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_follow_fans.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/plupload.full.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/pin.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/pin.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/topic.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/topic.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/uc_best.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/uc_best.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc_home_index.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc_home_index.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc_follow_fans.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc_follow_fans.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/publish.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/publish.js";
?>
<?php echo $this->fetch('inc/user_header.html'); ?>
<script type="text/javascript">
	var TOPIC_IMAGE_UPLOAD = '<?php
echo parse_url_tag("u:index|file#upload_topic|"."".""); 
?>'; //分享点评的图片上传路径
	var is_best_user = '<?php echo $this->_var['is_best_user']; ?>';
</script>
<div class="blank"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
	<div class="pin_layout" id="pin_layout_box">
	</div>
</div>
<?php if ($this->_var['is_best_user']): ?>
<div class="null_data_box <?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
	<div class="u_list_main">
		<div class="u_list_box">
			
		</div>
		<div class="tip"><h3><?php if ($this->_var['is_why'] != 1): ?>TA没关发布动态，<?php endif; ?>上面可能是你感兴趣的用户 ^_^ </h3>&nbsp;<a href="javascript:void(0);" onclick="load_best_user()"><i class="iconfont">&#xe624;</i>换一批</a></div>
	</div>
</div>
<?php endif; ?>
<input type="hidden" name="page" id="hd_page" value="<?php echo $this->_var['page']; ?>" />
<input type="hidden" name="step_size" id="hd_step_size" value="<?php echo $this->_var['step_size']; ?>" />
<input type="hidden" name="step" id="hd_step" /> 
<input type="hidden" name="ajax_wait" id="ajax_wait" /> 
<input type="hidden" name="user_id" value="<?php echo $this->_var['id']; ?>" id="user_id"/>
<div id="loading"> <span class="loading_span"></span><span>正在玩命加载中......</span></div>
<div class="pages"><?php echo $this->_var['pages']; ?></div>
<div class="blank"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
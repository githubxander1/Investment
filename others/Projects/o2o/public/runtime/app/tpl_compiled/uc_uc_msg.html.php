<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_msg.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/plupload.full.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_msg.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_msg.js";

?>
<?php echo $this->fetch('inc/header.html'); ?>

<div class="blank20"></div>

<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> clearfix">
	<div class="side_nav left_box">
		<?php echo $this->fetch('inc/uc_nav_list.html'); ?>
	</div>
	<div class="right_box">
		
		<div class="main_box">
			<div class="content">
				<div class="title"><span>我的消息</span></div>
				<div class="blank20"></div>
				
			</div>
			<?php if ($this->_var['list']): ?>
			<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'msg');if (count($_from)):
    foreach ($_from AS $this->_var['msg']):
?>
			<div class="msg_row clearfix">
				<div class="msg_icon f_l">
					<?php if ($this->_var['msg']['icon']): ?>
						<?php if ($this->_var['msg']['link']): ?><a href="<?php echo $this->_var['msg']['link']; ?>" title="<?php echo $this->_var['msg']['title']; ?>" target="_blank"><?php endif; ?>					
						<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['msg']['icon'],
  'w' => '50',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" />
						<?php if ($this->_var['msg']['link']): ?></a><?php endif; ?>	
					<?php else: ?>
					<i class="iconfont">&#xe62c;</i>
					<?php endif; ?>
				</div>
				<div class="msg_main f_r">
					<div class="msg_title">
						<span class="title">
						<?php if ($this->_var['msg']['is_read'] == 0): ?><i class="iconfont new_msg">&#xe636;</i><?php endif; ?>
						<?php if ($this->_var['msg']['title']): ?>
							<?php if ($this->_var['msg']['link']): ?><a href="<?php echo $this->_var['msg']['link']; ?>" title="<?php echo $this->_var['msg']['title']; ?>" target="_blank"><?php endif; ?>
								<?php echo $this->_var['msg']['short_title']; ?>
							<?php if ($this->_var['msg']['link']): ?></a><?php endif; ?>	
						<?php endif; ?>
						</span>
						<span class="pub_date"><i class="iconfont">&#xe621;</i> <?php echo $this->_var['msg']['create_time']; ?></span>
					</div>
					<div class="msg_content">
						<div class="content"><?php echo $this->_var['msg']['content']; ?></div>
						<div class="op">
							<a href="javascript:void(0);" action="<?php
echo parse_url_tag("u:index|uc_msg#remove_msg|"."id=".$this->_var['msg']['id']."".""); 
?>"><i class="iconfont">&#xe62f;</i></a>
						</div>
					</div>
				</div>
			</div>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>
			<?php else: ?>
			<div class="empty_tip">没有消息记录</div>
			<?php endif; ?>
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
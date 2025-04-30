<div class="pin_box">
	<div class="img_box">
		
		<?php if ($this->_var['message_item']['id'] != $this->_var['message_item']['origin_id'] && $this->_var['message_item']['origin']): ?>
			<?php $_from = $this->_var['message_item']['origin']['images']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'img');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['img']):
?>
			<?php if ($this->_var['key'] == 0): ?>
			<a href="<?php echo $this->_var['message_item']['origin']['url']; ?>" class="topic_img"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img']['o_path'],
  'w' => '225',
);
echo $k['name']($k['v'],$k['w']);
?>" width="225" height="<?php echo intval(225/$this->_var['img']['width']*$this->_var['img']['height']); ?>" /></a>
			<?php endif; ?>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			<?php if ($this->_var['message_item']['origin']['images'] == null): ?>  <div class="blank20">&nbsp;</div><?php endif; ?>
		<?php else: ?>
			<?php $_from = $this->_var['message_item']['images']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'img');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['img']):
?>
			<?php if ($this->_var['key'] == 0): ?>
				<a href="<?php echo $this->_var['message_item']['url']; ?>" class="topic_img"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img']['o_path'],
  'w' => '225',
);
echo $k['name']($k['v'],$k['w']);
?>" width="225" height="<?php echo intval(225/$this->_var['img']['width']*$this->_var['img']['height']); ?>" /></a>
			<?php endif; ?>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			<?php if ($this->_var['message_item']['images'] == null): ?> <div class="blank20">&nbsp;</div><?php endif; ?>
		<?php endif; ?>
	</div>
	<div class="user_info_box">
		<span class="avatar" ><?php 
$k = array (
  'name' => 'show_avatar',
  'uid' => $this->_var['message_item']['user_id'],
  'type' => 'small',
);
echo $k['name']($k['uid'],$k['type']);
?></span>
		<span class="user_name">
			<?php if ($this->_var['message_item']['fav_id'] > 0): ?>
				<strong>
					<?php 
$k = array (
  'name' => 'get_user_name',
  'value' => $this->_var['message_item']['user_id'],
  'show_tag' => '0',
);
echo $k['name']($k['value'],$k['show_tag']);
?> 
				</strong>
				<br />
				<span style="font-size:12px; color:#999;">
				<?php echo sprintf($GLOBALS['lang']['USER_FAV_THIS'],pass_date($this->_var['message_item']['create_time']));?>
				</span>
				<?php elseif ($this->_var['message_item']['relay_id'] > 0): ?>	
				<strong>
					<?php 
$k = array (
  'name' => 'get_user_name',
  'value' => $this->_var['message_item']['user_id'],
  'show_tag' => '0',
);
echo $k['name']($k['value'],$k['show_tag']);
?> 
				</strong>
				<br />
				<span style="font-size:12px; color:#999;">
				<?php echo sprintf($GLOBALS['lang']['USER_RELAY_THIS'],pass_date($this->_var['message_item']['create_time']));?>
				</span>
				<?php else: ?>							
				<strong>
					<?php 
$k = array (
  'name' => 'get_user_name',
  'value' => $this->_var['message_item']['user_id'],
  'show_tag' => '0',
);
echo $k['name']($k['value'],$k['show_tag']);
?> 
				</strong>
				<br />
				<span style="font-size:12px; color:#999;">
				<?php echo sprintf($GLOBALS['lang']['SUPPLIER_COMMENT_SAY'],pass_date($this->_var['message_item']['create_time']));?>
				</span>
			<?php endif; ?>
		</span>
	</div>
	<div class="brief_box">
		<?php if ($this->_var['message_item']['images'] == null && $this->_var['message_item']['origin']['images'] == null): ?>
			<a href="<?php echo $this->_var['message_item']['url']; ?>" target="_blank">
			<?php if ($this->_var['message_item']['fav_id'] > 0 || $this->_var['message_item']['relay_id'] > 0): ?>
				<?php if ($this->_var['message_item']['origin']['short_content']): ?>
					<i class="iconfont">&#xe628;</i>
					<?php echo $this->_var['message_item']['origin']['short_content']; ?>
					<i class="iconfont">&#xe627;</i>
				<?php endif; ?>
			<?php else: ?>
				<?php if ($this->_var['message_item']['short_content']): ?>
					<i class="iconfont">&#xe628;</i>
					<?php echo $this->_var['message_item']['short_content']; ?>
					<i class="iconfont">&#xe627;</i>
				<?php endif; ?>
			<?php endif; ?>
			</a>
		<?php else: ?>
			<?php if ($this->_var['message_item']['fav_id'] > 0 || $this->_var['message_item']['relay_id'] > 0): ?>
				<?php if ($this->_var['message_item']['origin']['short_content']): ?>
					<i class="iconfont">&#xe628;</i>
					<?php echo $this->_var['message_item']['origin']['short_content']; ?>
					<i class="iconfont">&#xe627;</i>
				<?php endif; ?>
			<?php else: ?>
				<?php if ($this->_var['message_item']['short_content']): ?>
					<i class="iconfont">&#xe628;</i>
					<?php echo $this->_var['message_item']['short_content']; ?>
					<i class="iconfont">&#xe627;</i>
				<?php endif; ?>
			<?php endif; ?>
		<?php endif; ?>
		
		
	</div>
	<div class="func_box">
		<div class="fav_icon f_l">
			<?php if ($this->_var['message_item']['id'] != $this->_var['message_item']['origin_id'] && $this->_var['message_item']['origin']): ?>
			<span class="fav_title" onclick="fav_topic(<?php echo $this->_var['message_item']['origin']['id']; ?>);"></span>
			<span class="fav_count"><a href="javascript:void(0);" onclick="fav_topic(<?php echo $this->_var['message_item']['origin']['id']; ?>);" class="topic_fav_<?php echo $this->_var['message_item']['origin']['id']; ?>"><?php echo $this->_var['message_item']['origin']['fav_count']; ?></a><i></i></span>
			<?php else: ?>
			<span class="fav_title" onclick="fav_topic(<?php echo $this->_var['message_item']['id']; ?>);"></span>
			<span class="fav_count"><a href="javascript:void(0);" onclick="fav_topic(<?php echo $this->_var['message_item']['id']; ?>);" class="topic_fav_<?php echo $this->_var['message_item']['id']; ?>"><?php echo $this->_var['message_item']['fav_count']; ?></a><i></i></span>
			<?php endif; ?>
		</div>
		
		<div class="comment_box f_r">
			<?php if ($this->_var['message_item']['id'] != $this->_var['message_item']['origin_id'] && $this->_var['message_item']['origin']): ?>
			<a href="<?php echo $this->_var['message_item']['origin']['url']; ?>">评论(<?php echo $this->_var['message_item']['origin']['reply_count']; ?>)</a>			
			<a href="javascript:void(0);" onclick="relay_topic(<?php echo $this->_var['message_item']['origin']['id']; ?>);">转载(<span class="topic_relay_<?php echo $this->_var['message_item']['origin']['id']; ?>"><?php echo $this->_var['message_item']['origin']['relay_count']; ?></span>)</a>
			<?php else: ?>
			<a href="<?php echo $this->_var['message_item']['url']; ?>">评论(<?php echo $this->_var['message_item']['reply_count']; ?>)</a>			
			<a href="javascript:void(0);" onclick="relay_topic(<?php echo $this->_var['message_item']['id']; ?>);">转载(<span class="topic_relay_<?php echo $this->_var['message_item']['id']; ?>"><?php echo $this->_var['message_item']['relay_count']; ?></span>)</a>
			<?php endif; ?>
		</div>
	</div>
	
</div>

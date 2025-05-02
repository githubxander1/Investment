<?php if ($this->_var['dp_list']): ?>
<div class="comments_details">
	<ul>
		<?php $_from = $this->_var['dp_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'dp_item');if (count($_from)):
    foreach ($_from AS $this->_var['dp_item']):
?>
		<li class="details_li">
			<div class="clearfix">
				<div class="f_l">
					<span class="user_name"><?php 
$k = array (
  'name' => 'get_user_name',
  'value' => $this->_var['dp_item']['user_id'],
  'show_tag' => '0',
);
echo $k['name']($k['value'],$k['show_tag']);
?> </span>
					<span class="date"><?php echo $this->_var['dp_item']['create_time_format']; ?></span>
					<?php if ($this->_var['dp_item']['data_info']): ?>
					对 <a href="<?php echo $this->_var['dp_item']['data_info']['url']; ?>" target="_blank" class="dp_data" title="<?php echo $this->_var['dp_item']['data_info']['name']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['dp_item']['data_info']['name'],
  'b' => '0',
  'e' => '30',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a> 点评：
					<?php endif; ?>
				</div>
				<div class="f_r">
					<input class="ui-starbar" value="<?php echo $this->_var['dp_item']['point']; ?>" disabled="true"  />
				</div>
			</div>
			<p class="content">
				<?php echo $this->_var['dp_item']['content']; ?>
			</p>
			
			<?php if ($this->_var['dp_item']['images']): ?>
			<div class="review_pic clearfix">
				<div class="over">
					<div  class="pic_box">
					     <ul>
					     	<?php $_from = $this->_var['dp_item']['images']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'img');if (count($_from)):
    foreach ($_from AS $this->_var['img']):
?>
					     	<li>
					     		<a href="javascript:void(0);" rel="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img'],
  'w' => '670',
  'h' => '0',
);
echo $k['name']($k['v'],$k['w'],$k['h']);
?>"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img'],
  'w' => '100',
  'h' => '100',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" /></a>
					     	</li>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>									
							
						 </ul>
					</div>
					
					<?php if (count ( $this->_var['dp_item']['images'] ) > 6): ?>
					<a href="javascript:void(0);" class="pre hide_tag"></a>
					<a href="javascript:void(0);" class="next hide_tag"></a>
					<?php endif; ?>
				</div>
				<div class="blank"></div>
				<div class="big_img">
					<a href="javascript:void(0);" class="bprev"></a>
					<a href="javascript:void(0);" class="bnext"></a>
					<img src="" />
				</div>
			</div>
			<?php endif; ?>
			<?php if ($this->_var['dp_item']['reply_content']): ?>
			<div class="supplier_reply"><span class="reply_title">掌柜回复：</span><?php echo $this->_var['dp_item']['reply_content']; ?></div>
			<?php endif; ?>
		</li>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>				
	</ul>
	<div class="blank"></div>
	<div class="pages">
		<?php echo $this->_var['pages']; ?>
	</div>
</div>
<?php else: ?>
<div class="empty_tip">
	没有相关点评数据
</div>
<?php endif; ?>	
		
				

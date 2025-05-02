<div class="publish_edit_box">
	
	<div class="item_textarea_box">
		<textarea id="publish_item_textarea" class="publish_item_textarea ui-textarea" placeholder="说点什么吧，让分享更精彩！" name="content"><?php echo $this->_var['content']; ?></textarea>
	</div>
	<div class="item_operation_box clearfix">
		<div class="f_l" >
			<span class="form_ico form_face form_face_publish_item_textarea"><i class="iconfont">&#xe60e;</i>&nbsp;表情</span>

		</div>
		<div class="f_r">
			<div class="publish_weibo"><label class="ui-checkbox" rel="common_cbo"><input type="checkbox" name="syn_weibo" value="1" checked="checked"/>同步到微博</label>&nbsp;<a href="<?php
echo parse_url_tag("u:index|uc_account|"."".""); 
?>">[设置]</a></div>

			<div class="publish_text_count"><em>0</em><span> / 140</span></div>

		</div>
	</div>
	

</div>

<div class="form_tags_box" style="display:none;">
		<input type="hidden" name="tags" value="<?php echo $this->_var['tags']; ?>"/>
</div>
<div class="blank10"></div>

<div id="face_box_tab_publish_item_textarea" style="display:none;">
	<ul class="lb_tab">
	<?php $_from = $this->_var['expression']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
	<li class="<?php if ($this->_var['key'] == 'qq'): ?>c<?php endif; ?> rt3 " f="<?php echo $this->_var['key']; ?>" title="<?php echo $this->_var['key']; ?>"><a onclick="toogle_mo(this);" onfocus="$(this).blur();" href="javascript:void(0)">
		<?php echo $GLOBALS['lang']['EXPRESSION_'.strtoupper($GLOBALS['tmpl']->_var['key'])];?>
	</a></li>
	<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	</ul>
</div>
<div id="face_box_hd_publish_item_textarea" style="display:none;">
<?php $_from = $this->_var['expression']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
	<div class="emotion emotion_publish_item_textarea <?php echo $this->_var['key']; ?>" f="<?php echo $this->_var['key']; ?>" <?php if ($this->_var['key'] != 'qq'): ?>style="display:none;"<?php endif; ?>>
	<div class="blank5"></div>
	<?php $_from = $this->_var['item']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'exp');if (count($_from)):
    foreach ($_from AS $this->_var['exp']):
?>
		<a href="javascript:void(0);" title="<?php echo $this->_var['exp']['title']; ?>" rel="<?php echo $this->_var['exp']['emotion']; ?>"><img src="<?php echo $this->_var['exp']['filename']; ?>" /></a>
	<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	</div>
<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
</div>

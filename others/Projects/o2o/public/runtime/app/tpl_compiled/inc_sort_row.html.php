<?php if ($this->_var['sort_row_data']): ?>
<div class="sort_row">
	<ul>
		<?php $_from = $this->_var['sort_row_data']['sort']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'sort_item');if (count($_from)):
    foreach ($_from AS $this->_var['sort_item']):
?>
		<li class="anode <?php if ($this->_var['sort_item']['current']): ?>current<?php endif; ?> <?php echo $this->_var['sort_item']['type']; ?>"><a href="<?php echo $this->_var['sort_item']['url']; ?>"><?php echo $this->_var['sort_item']['name']; ?><?php if ($this->_var['sort_item']['type']): ?><i class="iconfont"><?php if ($this->_var['sort_item']['type'] == 'asc'): ?>&#xe61c;<?php else: ?>&#xe61d;<?php endif; ?></i><?php endif; ?></a></li>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		
		<?php $_from = $this->_var['sort_row_data']['range']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'range_item');if (count($_from)):
    foreach ($_from AS $this->_var['range_item']):
?>
		<li class="dnode">
		<select class="ui-drop">
			<?php $_from = $this->_var['range_item']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'range_row');if (count($_from)):
    foreach ($_from AS $this->_var['range_row']):
?>
			<option value="<?php echo $this->_var['range_row']['url']; ?>" <?php if ($this->_var['range_row']['selected']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['range_row']['name']; ?></option>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</select>
		</li>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		
		<?php $_from = $this->_var['sort_row_data']['tag']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'tag_item');if (count($_from)):
    foreach ($_from AS $this->_var['tag_item']):
?>
		<li class="cnode">
		<label class="ui-checkbox dtag" rel="common_cbo"><input type="checkbox" <?php if ($this->_var['tag_item']['checked']): ?>checked="checked"<?php endif; ?> name="t1" value="<?php echo $this->_var['tag_item']['url']; ?>" /><?php echo $this->_var['tag_item']['name']; ?></label>
		</li>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	</ul>
</div>
<?php endif; ?>
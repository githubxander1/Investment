
<?php $_from = $this->_var['filter_group']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'filter_item');if (count($_from)):
    foreach ($_from AS $this->_var['filter_item']):
?>
	<div>
		<span id="title_<?php echo $this->_var['filter_item']['id']; ?>"><?php echo $this->_var['filter_item']['name']; ?></span>：
		<input type="text" class="textbox" name="filter[<?php echo $this->_var['filter_item']['id']; ?>]" value="<?php echo $this->_var['filter_item']['value']; ?>" />
		<div class="blank5"></div>
	</div>
<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
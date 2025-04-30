<div class="city_select_box clearfix">
	<div class="selected_city f_l"><span></span></div>
	<div class="select_city_btn_box f_l"><button class="ui-button select_city_btn" rel="white" type="button">选择城市</button></div>
	<input type="hidden"  name="city_id" value="<?php echo $this->_var['city_id']; ?>"/>
	<div class="city_list_box">
		<dl>
			<?php $_from = $this->_var['city_tree']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
				<dt><?php echo $this->_var['row']['name']; ?></dt>
				<?php $_from = $this->_var['row']['_child']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'sub_item');if (count($_from)):
    foreach ($_from AS $this->_var['sub_item']):
?>
					<dd><a class="city_item <?php if ($this->_var['sub_item']['selected'] == 1): ?> curr <?php endif; ?>" href="javascript:void(0);" onclick="select_city(this)" data="<?php echo $this->_var['sub_item']['id']; ?>"><?php echo $this->_var['sub_item']['name']; ?></a></dd>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</dl>
	</div>
</div>
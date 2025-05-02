<script type="text/javascript">
	$(document).ready(function(){
		load_attr_stock();
	});
	function addRow(obj)
	{
		var html = $(obj.parentNode).html();
		html = html.replace("addRow", "delRow");
		html = html.replace("+", "-");
		$("<div>"+html+"</div>").insertAfter($(obj.parentNode));
	}
	function delRow(obj)
	{
		$(obj.parentNode).remove();
	}
</script>
<?php $_from = $this->_var['goods_type_attr']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'attr_item');if (count($_from)):
    foreach ($_from AS $this->_var['attr_item']):
?>
<div>
		<span id="title_<?php echo $this->_var['attr_item']['id']; ?>"><?php echo $this->_var['attr_item']['name']; ?></span>：
		<?php if ($this->_var['attr_item']['input_type'] == 0): ?>
		<input type="text" class="textbox" style="width:50px;" name="deal_attr[<?php echo $this->_var['attr_item']['id']; ?>][]" value="<?php echo $this->_var['attr_item']['attr_name']; ?>" onchange="load_attr_stock();"  />			
		<?php endif; ?>
		<?php if ($this->_var['attr_item']['input_type'] == 1): ?>
			<select name="deal_attr[<?php echo $this->_var['attr_item']['id']; ?>][]" onchange="load_attr_stock();">
			<?php $_from = $this->_var['attr_item']['attr_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'attr_row');if (count($_from)):
    foreach ($_from AS $this->_var['attr_row']):
?>
				<option value="<?php echo $this->_var['attr_row']; ?>" <?php if ($this->_var['attr_item']['attr_name'] == $this->_var['attr_row']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['attr_row']; ?></option>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</select>			
		<?php endif; ?>
		
		递加价格：<input type="text" class="textbox" style="width:50px;" name="deal_attr_price[<?php echo $this->_var['attr_item']['id']; ?>][]" value="<?php echo $this->_var['attr_item']['price']; ?>" />
		<?php if ($this->_var['allow_publish_verify'] == 0): ?>
		递加结算价：<input type="text" class="textbox" style="width:50px;" name="deal_add_balance_price[<?php echo $this->_var['attr_item']['id']; ?>][]" value="<?php echo $this->_var['attr_item']['add_balance_price']; ?>" />
		<?php endif; ?>
		
		<?php if ($this->_var['attr_item']['is_first'] == 1): ?>
		[ <a href="javascript:void(0);" onclick="addRow(this);" style="text-decoration:none;">+</a> ]
		<?php else: ?>
		[ <a href="javascript:void(0);" onclick="delRow(this);" style="text-decoration:none;">-</a> ]
		<?php endif; ?>
		<label style="width:14px;"><input class="deal_attr_stock" style="width:14px;" type="checkbox" rel="<?php echo $this->_var['attr_item']['id']; ?>" name="deal_attr_stock[<?php echo $this->_var['attr_item']['id']; ?>][]" value="1" <?php if ($this->_var['attr_item']['is_checked'] == 1): ?>checked="checked"<?php endif; ?> onchange="load_attr_stock(this);"/>设置库存 -1或不设置为无限</label>
		<input type="hidden" class="deal_attr_stock_hd" name="deal_attr_stock_hd[<?php echo $this->_var['attr_item']['id']; ?>][]" />
		<div class="blank5"></div>
	</div>

<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
<div id="stock_table"></div>
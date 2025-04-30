<div class="item_name"><?php echo $this->_var['item']['name']; ?></div>
<form action="<?php
echo parse_url_tag("u:biz|goodso#do_delivery|"."".""); 
?>" method="post" name="delivery_form">
<table class="delivery_table">
	<tr>
		<td class="title">发货的门店</td>
		<td>
			<select name="location_id" class="ui-select location_select" height="50">
				<?php $_from = $this->_var['location_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'location');if (count($_from)):
    foreach ($_from AS $this->_var['location']):
?>
				<option value="<?php echo $this->_var['location']['id']; ?>"><?php echo $this->_var['location']['name']; ?></option>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</select>
		</td>
	</tr>
	<tr>
		<td class="title">快递</td>
		<td>
			<select name="express_id" class="ui-select express_select" height="50">
				<option value="0">其他</option>
				<?php $_from = $this->_var['express_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'express');if (count($_from)):
    foreach ($_from AS $this->_var['express']):
?>
				<option value="<?php echo $this->_var['express']['id']; ?>"><?php echo $this->_var['express']['name']; ?></option>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</select>
		</td>
	</tr>
	<tr>
		<td class="title">快递单号</td>
		<td>
			<div class="item_name">同一批发货的商品可填写相同的单号</div>
			<input type="text" class="ui-textbox" name="delivery_sn" holder="请输入相应的快递单号" />
		</td>
	</tr>
	<tr>
		<td class="title">备注</td>
		<td>
			<textarea name="memo" class="ui-textbox memo" holder="没有备注请留空"></textarea>
		</td>
	</tr>
	<tr>
		<td colspan=2  class="btn">
			<input type="hidden" name="id" value="<?php echo $this->_var['item']['id']; ?>" />
			<input type="hidden" name="ajax" value="1" />
			<button class="ui-button orange" rel="orange" type="submit">确认发货</button>
		</td>
	</tr>
</table>
</form>

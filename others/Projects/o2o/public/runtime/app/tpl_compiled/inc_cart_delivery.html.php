	<?php if ($this->_var['delivery_list']): ?>
	<table>
		<?php $_from = $this->_var['delivery_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'delivery_item');if (count($_from)):
    foreach ($_from AS $this->_var['delivery_item']):
?>
		<tr>
			<td class="delivery_title">
				<label class="ui-radiobox" rel="common_rdo">
					<input type="radio" value="<?php echo $this->_var['delivery_item']['id']; ?>" name="delivery"  >
					<?php echo $this->_var['delivery_item']['name']; ?>
				</label>			
			</td>
			<td>												
				<?php 
$k = array (
  'name' => 'nl2br',
  'value' => $this->_var['delivery_item']['description'],
);
echo $k['name']($k['value']);
?>
			</td>
		</tr>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	</table>
	<?php else: ?>
	<div class="empty_tip"><?php
echo lang("NO_SUPPORT_DELIVERY"); 
?></div>
	<?php endif; ?>	

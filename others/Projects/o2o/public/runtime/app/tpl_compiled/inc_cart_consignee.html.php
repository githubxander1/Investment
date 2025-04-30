




<div class="form_panel">

			<dl>
				<dt><?php
echo lang("CONSIGNEE"); 
?></dt>
				<dd>
					<input class="ui-textbox" value="<?php echo $this->_var['consignee_info']['consignee']; ?>" name="consignee" holder="请输入收货人姓名" />
					<span class="form_tip"></span>
				</dd>
			</dl>
			<dl>
				<dt><?php
echo lang("REGION_INFO"); 
?></dt>
				<dd>
					<select name="region_lv1" class="ui-select region_select" height="300">
					    <option value="0">=<?php
echo lang("SELECT_PLEASE"); 
?>=</option>
						<?php $_from = $this->_var['region_lv1']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'lv1');if (count($_from)):
    foreach ($_from AS $this->_var['lv1']):
?>
						<option <?php if ($this->_var['lv1']['selected'] == 1): ?>selected="selected"<?php endif; ?> value="<?php echo $this->_var['lv1']['id']; ?>"><?php echo $this->_var['lv1']['name']; ?></option>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
				  	</select>
									
					<select name="region_lv2" class="ui-select region_select" height="300">
						<option value="0">=<?php
echo lang("SELECT_PLEASE"); 
?>=</option>
						<?php $_from = $this->_var['region_lv2']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'lv2');if (count($_from)):
    foreach ($_from AS $this->_var['lv2']):
?>
						<option <?php if ($this->_var['lv2']['selected'] == 1): ?>selected="selected"<?php endif; ?> value="<?php echo $this->_var['lv2']['id']; ?>"><?php echo $this->_var['lv2']['name']; ?></option>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					  </select>
										
					<select name="region_lv3" class="ui-select region_select" height="300">
						<option value="0">=<?php
echo lang("SELECT_PLEASE"); 
?>=</option>		
						<?php $_from = $this->_var['region_lv3']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'lv3');if (count($_from)):
    foreach ($_from AS $this->_var['lv3']):
?>
						<option <?php if ($this->_var['lv3']['selected'] == 1): ?>selected="selected"<?php endif; ?> value="<?php echo $this->_var['lv3']['id']; ?>"><?php echo $this->_var['lv3']['name']; ?></option>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					 </select>
										
					<select name="region_lv4" class="ui-select region_select" height="300">
						<option value="0">=<?php
echo lang("SELECT_PLEASE"); 
?>=</option>
						<?php $_from = $this->_var['region_lv4']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'lv4');if (count($_from)):
    foreach ($_from AS $this->_var['lv4']):
?>
						<option <?php if ($this->_var['lv4']['selected'] == 1): ?>selected="selected"<?php endif; ?> value="<?php echo $this->_var['lv4']['id']; ?>"><?php echo $this->_var['lv4']['name']; ?></option>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					  </select>
				</dd>
			</dl>
			<dl>
				<dt><?php
echo lang("ADDRESS"); 
?></dt>
				<dd>
					<input  name="address" value="<?php echo $this->_var['consignee_info']['address']; ?>" class="ui-textbox" holder="请输入收货地址" />
					<span class="form_tip"></span>
				</dd>
			</dl>
			<dl>
				<dt><?php
echo lang("ZIP"); 
?></dt>
				<dd>
					<input  name="zip" value="<?php echo $this->_var['consignee_info']['zip']; ?>" class="ui-textbox" holder="请输入邮编" />
					<span class="form_tip"></span>
				</dd>
			</dl>

			<dl>
				<dt><?php
echo lang("MOBILE"); 
?></dt>
				<dd>
					<input  name="mobile" value="<?php echo $this->_var['consignee_info']['mobile']; ?>" class="ui-textbox" holder="请输入收货人手机" />
					<span class="form_tip"></span>
				</dd>
			</dl>
			<input type="hidden" name="consignee_id" value="<?php echo $this->_var['consignee_info']['id']; ?>" />
	</div>





<div class="side_nav">
<?php if ($this->_var['nav_list']): ?>
<?php $_from = $this->_var['nav_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('nav_key', 'nav_item');if (count($_from)):
    foreach ($_from AS $this->_var['nav_key'] => $this->_var['nav_item']):
?>
	<dl class="nav_item">
		<dt class="nav_item_title"><i class=" iconfont"><?php echo $this->_var['nav_item']['iconfont']; ?></i><?php echo $this->_var['nav_item']['name']; ?></dt>
		<?php $_from = $this->_var['nav_item']['node']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('s_nav_key', 's_nav_item');if (count($_from)):
    foreach ($_from AS $this->_var['s_nav_key'] => $this->_var['s_nav_item']):
?>
			<dd><div class="<?php if ($this->_var['s_nav_item']['module'] == $this->_var['MODULE_NAME']): ?>current<?php endif; ?>"><a href="<?php echo $this->_var['s_nav_item']['url']; ?>"><?php echo $this->_var['s_nav_item']['name']; ?></a></div></dd>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	</dl>
<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
<?php endif; ?>
<div class="blank20"></div>
</div>
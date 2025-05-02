<?php if ($this->_var['filter_row_data']): ?>
<div class="filter_row">
	<?php if ($this->_var['filter_row_data']['nav_list']): ?>
	<dl class=" orientation_row <?php if (count ( $this->_var['filter_row_data']['filter_list'] ) == 0): ?>bottom<?php endif; ?>">
		<dd>
			<!--begin select-->
			<div class="orientation clearfix">
				<?php $_from = $this->_var['filter_row_data']['nav_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'filter_row');$this->_foreach['nav_loop'] = array('total' => count($_from), 'iteration' => 0);
if ($this->_foreach['nav_loop']['total'] > 0):
    foreach ($_from AS $this->_var['filter_row']):
        $this->_foreach['nav_loop']['iteration']++;
?>
					<?php if ($this->_var['filter_row']['current']['url']): ?>
					<span class="tag">
				   	<a class="name" href="<?php echo $this->_var['filter_row']['current']['url']; ?>"><?php echo $this->_var['filter_row']['current']['name']; ?></a>
				    </span>
					<?php else: ?>
					<span class="tag choose_parent"><!--hover事件用active区别-->
				   	<div class="deceit"></div><!--在ie下有一个缺角，这个用来补充-->
				   	<span class="name">
				   		<?php echo $this->_var['filter_row']['current']['name']; ?>
					   <i></i>	
					</span>
					<a href="<?php echo $this->_var['filter_row']['current']['cancel']; ?>" class="hidden_but">
						<i class="iconfont">&#xe619;</i>
					</a>
					<?php if ($this->_var['filter_row']['list']): ?>
					    <div class="hidden_nav">
					    	
							<ul class="clearfix">
								<?php $_from = $this->_var['filter_row']['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'item_0_48617000_1484912912');if (count($_from)):
    foreach ($_from AS $this->_var['item_0_48617000_1484912912']):
?>
								<li>
									<a href="<?php echo $this->_var['item_0_48617000_1484912912']['url']; ?>" class="font_hover"><?php echo $this->_var['item_0_48617000_1484912912']['name']; ?></a>
								</li>
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							</ul>
						</div>
					<?php endif; ?>
					</span>
					<?php endif; ?>
					<?php if (! ($this->_foreach['nav_loop']['iteration'] == $this->_foreach['nav_loop']['total'])): ?>
					<span class="arrow"></span>
					<?php endif; ?>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>				   
			  </div>
			<!--end select-->
		</dd>
	</dl>
	<?php endif; ?>
	<?php $_from = $this->_var['filter_row_data']['filter_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'filter_item');$this->_foreach['filter_loop'] = array('total' => count($_from), 'iteration' => 0);
if ($this->_foreach['filter_loop']['total'] > 0):
    foreach ($_from AS $this->_var['filter_item']):
        $this->_foreach['filter_loop']['iteration']++;
?>
	<?php if ($this->_var['filter_item']['list']): ?>
	<dl class="clearfix <?php if (($this->_foreach['filter_loop']['iteration'] == $this->_foreach['filter_loop']['total'])): ?>bottom<?php endif; ?>">
		<dt><?php echo $this->_var['filter_item']['name']; ?>：</dt>
		<dd class="wrap_filter">
			<ul>
				<?php $_from = $this->_var['filter_item']['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'item_0_48667000_1484912912');if (count($_from)):
    foreach ($_from AS $this->_var['item_0_48667000_1484912912']):
?>
				<li <?php if ($this->_var['item_0_48667000_1484912912']['current'] == 1): ?>class="current"<?php endif; ?>><a href="<?php echo $this->_var['item_0_48667000_1484912912']['url']; ?>" ><?php echo $this->_var['item_0_48667000_1484912912']['name']; ?></a></li>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</ul>
		</dd>
		<dd class="expend">
			<a href="javascript:void(0);" class="open">更多</a>
			<a href="javascript:void(0);" class="close">收起</a>
		</dd>
	</dl>
	<?php endif; ?>
	<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	
</div>
<?php endif; ?>
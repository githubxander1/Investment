<ul class="side_deal_list">
	<?php $_from = $this->_var['side_deal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'side_deal');if (count($_from)):
    foreach ($_from AS $this->_var['side_deal']):
?>
	<li>
		<a href="<?php echo $this->_var['side_deal']['url']; ?>" class="deal_img"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['side_deal']['icon'],
  'w' => '198',
  'h' => '134',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" /></a>
		<a href="<?php echo $this->_var['side_deal']['url']; ?>"  class="deal_title"><?php echo $this->_var['side_deal']['sub_name']; ?></a>
		<div class="deal_info">
			<span class="deal_price f_l">
				<?php if ($this->_var['side_deal']['buy_type'] == 1): ?>
				<span class="current_price"><?php 
$k = array (
  'name' => 'abs',
  'v' => $this->_var['side_deal']['return_score'],
);
echo $k['name']($k['v']);
?><i>积分</i></span>
				<?php else: ?>
				<span class="current_price"><i>&yen;</i><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['side_deal']['current_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
				<span class="origin_price">&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['side_deal']['origin_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
				<?php endif; ?>
			</span>
			<span class="sale_count f_r">
				<?php if ($this->_var['side_deal']['buy_type'] == 1): ?>
				已兑换<span><?php echo $this->_var['side_deal']['buy_count']; ?></span>
				<?php else: ?>
				已售<span><?php echo $this->_var['side_deal']['buy_count']; ?></span>
				<?php endif; ?>
			</span>
		</div>
	</li>
	<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	
</ul>
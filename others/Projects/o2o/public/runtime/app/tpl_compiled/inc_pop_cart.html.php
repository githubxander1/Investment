<div class="pop_cart">
	<div class="tip_row">
		<span class="icon"></span>
		<span class="message">
		<h2>商品已加入购物车！</h2>
		<h3>购物车内共<i><?php echo $this->_var['cart_total']; ?></i>种商品</h3>
		</span>
	</div>
	<div class="btn_row">
	<button class="ui-button" rel="blue" action="close">继续购买</button>
	<button class="ui-button" rel="orange" action="checkout" action-url="<?php
echo parse_url_tag("u:index|cart|"."".""); 
?>">去结算</button>
	</div>
	<div class="blank"></div>
	<?php if ($this->_var['relate_list']): ?>	
	<div class="relate_row">
		<div class="title">购买此商品的用户还购买了：</div>
		<div class="content">
		<?php $_from = $this->_var['relate_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal');if (count($_from)):
    foreach ($_from AS $this->_var['deal']):
?>
		<div class="relate_item">
			<a href="<?php echo $this->_var['deal']['url']; ?>" class="item_img" title="<?php echo $this->_var['deal']['name']; ?>" target="_blank"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['deal']['icon'],
  'w' => '127',
  'h' => '77',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" /></a>
			<a href="<?php echo $this->_var['deal']['url']; ?>" class="item_name" title="<?php echo $this->_var['deal']['name']; ?>" target="_blank"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['deal']['sub_name'],
  'b' => '0',
  'e' => '8',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a>
			<span class="item_price">&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['current_price'],
  'e' => '2',
);
echo $k['name']($k['v'],$k['e']);
?></span>
		</div>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</div>
	</div>
	<?php endif; ?>
</div>

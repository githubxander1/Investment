<?php if ($this->_var['cart_list']): ?>
<script type="text/javascript">
	var jsondata = <?php echo $this->_var['jsondata']; ?>;
</script>
<form name="cart_form" action="<?php
echo parse_url_tag("u:index|ajax#check_cart|"."".""); 
?>">
<div class="cart_table">
		
		<table>
			<tr>
				<th class="w_name">项目</th>
				<th class="w_unit">单价</th>
				<th class="w_num">数量</th>
				<th class="w_total">总价</th>
				<th class="w_op">操作</th>
			</tr>
			<?php $_from = $this->_var['cart_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'cart_item');if (count($_from)):
    foreach ($_from AS $this->_var['cart_item']):
?>
			<tr rel="<?php echo $this->_var['cart_item']['id']; ?>">
				<td class="w_name">
					<div class="cart_img">
						<a href="<?php echo $this->_var['cart_item']['url']; ?>" target="_blank" title="<?php echo $this->_var['cart_item']['name']; ?>"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['cart_item']['icon'],
  'w' => '50',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" alt="<?php echo $this->_var['cart_item']['name']; ?>" style="width:50px;height:50px;" /></a>
					</div>
					<div class="cart_name">
						<a href="<?php echo $this->_var['cart_item']['url']; ?>" target="_blank" title="<?php echo $this->_var['cart_item']['name']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['cart_item']['name'],
  'b' => '0',
  'e' => '70',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a>
					</div>
				</td>
				<td class="w_unit">
					<?php if ($this->_var['cart_item']['buy_type'] != 1): ?>
					&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['cart_item']['unit_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?>
					<?php else: ?>
					<?php 
$k = array (
  'name' => 'abs',
  'v' => $this->_var['cart_item']['return_score'],
);
echo $k['name']($k['v']);
?>积分
					<?php endif; ?>
				</td>
				<td class="w_num">
					<input type="hidden" name="id[]" value="<?php echo $this->_var['cart_item']['id']; ?>" />
					<i class="minus" rel="<?php echo $this->_var['cart_item']['id']; ?>">-</i>
					<input type="text" maxlength="4" class="num_ipt ui-textbox" name="number[]" value="<?php echo $this->_var['cart_item']['number']; ?>" rel="<?php echo $this->_var['cart_item']['id']; ?>" />
					<i class="add" rel="<?php echo $this->_var['cart_item']['id']; ?>">+</i>
				</td>
				<td class="w_total">
					<?php if ($this->_var['cart_item']['buy_type'] != 1): ?>
					&yen;<span><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['cart_item']['total_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
					<?php else: ?>
					<span><?php 
$k = array (
  'name' => 'abs',
  'v' => $this->_var['cart_item']['return_total_score'],
);
echo $k['name']($k['v']);
?></span>积分					
					<?php endif; ?>
				</td>
				<td class="w_op">
					<a href="javascript:void(0);" rel="<?php echo $this->_var['cart_item']['id']; ?>">删除</a>
				</td>
			</tr>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</table>
		
</div>
<div class="cart_total">
	<table>
		<tr>
			<td class="cart_back"><a href="<?php
echo parse_url_tag("u:index|index|"."".""); 
?>">继续购物</a></td>
			<td class="cart_sum">总计（不包含运费）：<?php if ($this->_var['cart_item']['buy_type'] != 1): ?><span>&yen;</span><?php endif; ?><span id="sum"><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['total_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span><?php if ($this->_var['cart_item']['buy_type'] == 1): ?><span>积分</span><?php endif; ?></td>
			<td class="cart_btn">
				<button class="ui-button f_l remove" rel="blue" type="button">清空购物车</button>
				<button class="ui-button f_l check" rel="orange" type="submit">去结算</button>
			</td>
		</tr>
	</table>	
</div>
</form>
<?php else: ?>
<div class="cart_empty">
	<span>
		购物车内暂时没有商品<br />
		马上去 [ <a href="<?php
echo parse_url_tag("u:index|index|"."".""); 
?>">首页</a> ] 挑选商品<br />
		或者<?php if (! $this->_var['user_info']): ?> [<a href="<?php
echo parse_url_tag("u:index|user#login|"."".""); 
?>">登录</a>] 后<?php endif; ?>去 [ <a href="<?php
echo parse_url_tag("u:index|uc_collect|"."".""); 
?>">我的收藏夹</a> ] 看看。
	</span>
</div>
<?php endif; ?>
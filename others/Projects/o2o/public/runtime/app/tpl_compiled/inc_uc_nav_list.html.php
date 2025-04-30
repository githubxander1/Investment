<div class="user_info_box clearfix">
	<div class="f_l avatar_box"><?php 
$k = array (
  'name' => 'show_avatar',
  'id' => $this->_var['user_info']['id'],
  'type' => 'small',
  'is_card' => '0',
);
echo $k['name']($k['id'],$k['type'],$k['is_card']);
?></div>
	<div class="f_r u_name">
		<?php echo $this->_var['user_info']['user_name']; ?>
		<div class="blank5"></div>
		<?php if ($this->_var['user_info']['is_merchant'] == 1): ?><span class="is_merchant" title="认证商家"></span><?php endif; ?><?php if ($this->_var['user_info']['is_daren'] == 1): ?><span class="is_daren" title="<?php echo $this->_var['user_info']['daren_title']; ?>"></span><?php endif; ?>
	</div>
	<div class="blank5"></div>
	
</div>
<div class="nav_account_info">
		<a class="account_item item_l" href="<?php
echo parse_url_tag("u:index|uc_log#money|"."".""); 
?>"><?php 
$k = array (
  'name' => 'round',
  'p' => $this->_var['user_info']['money'],
  'l' => '2',
);
echo $k['name']($k['p'],$k['l']);
?><span>余额</span></a>
		<a class="account_item item_r" href="<?php
echo parse_url_tag("u:index|uc_log#score|"."".""); 
?>"><?php 
$k = array (
  'name' => 'intval',
  'p' => $this->_var['user_info']['score'],
);
echo $k['name']($k['p']);
?><span>积分</span></a>
	</div>
	<div class="blank5"></div>
<div class="side_nav">
<?php if ($this->_var['uc_nav_list']): ?>
<?php $_from = $this->_var['uc_nav_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('nav_key', 'nav_item_0_93973000_1484821381');if (count($_from)):
    foreach ($_from AS $this->_var['nav_key'] => $this->_var['nav_item_0_93973000_1484821381']):
?>
	<dl class="nav_item">
		<dt class="nav_item_title"><i class=""></i><?php echo $this->_var['nav_item_0_93973000_1484821381']['name']; ?></dt>
		<?php $_from = $this->_var['nav_item_0_93973000_1484821381']['node']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('s_nav_key', 's_nav_item');if (count($_from)):
    foreach ($_from AS $this->_var['s_nav_key'] => $this->_var['s_nav_item']):
?>
			<dd><div class="s_item clearfix <?php if ($this->_var['s_nav_item']['current'] == 1): ?>current<?php endif; ?>"><i class="dot"></i>&nbsp;&nbsp;<a href="<?php echo $this->_var['s_nav_item']['url']; ?>"><?php echo $this->_var['s_nav_item']['name']; ?></a><i class="triangle"></i></div></dd>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	</dl>
<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
<?php endif; ?>
<div class="blank20"></div>
</div>
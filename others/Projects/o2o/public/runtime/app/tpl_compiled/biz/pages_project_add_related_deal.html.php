<div class="deal_add_goods_type_page">
	<form name="search_relate"  method="post">
	<div class="search_relate">
		<input class="ui-textbox" name="search_relate_deal" value=""/>
		<button class="ui-button add_related_deal" rel="white" type="submit">搜索</button>
	</div>	
	</form>
	<div class="blank10"></div>
	<div class="con_box">
		<div id="relate_deal">
	
		</div>	
				
	
		<div class="blank20"></div>
		<div class="select_relate" id="relate1">
				<ul>
					<?php if ($this->_var['related_deal']): ?>
					<?php $_from = $this->_var['related_deal']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['item']):
?>
					<li rel="<?php echo $this->_var['item']['id']; ?>">
						<a href="javascript:void(0);" title="<?php echo $this->_var['item']['name']; ?>"></a>
						<div class="relate_img"><img  src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['item']['icon'],
  'w' => '70',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" style="width:70px;height:50px;"></div>
						<div class="relate_name"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['item']['name'],
  'l' => '0',
  'e' => '5',
);
echo $k['name']($k['v'],$k['l'],$k['e']);
?></div>
					</li>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					<?php endif; ?>
	
				</ul>
				<input type="hidden" name="related_deal" value="<?php echo $this->_var['related_deal_id']; ?>"/>
		</div>
		<div class="blank20"></div>
		<div style="text-align:right;padding-right: 20px;">
				<button class="ui-button sure_relate" rel="orange" type="button">确认</button>
		</div>

	</div>

</div>
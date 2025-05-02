<?php if ($this->_var['goodsList']): ?>
<script>
	var jsonDeal  = <?php echo $this->_var['jsonDeal']; ?>;
	var jsonAttr  = <?php echo $this->_var['jsonAttr']; ?>;
	var jsonStock = <?php echo $this->_var['jsonStock']; ?>;
	
	
	
</script>
<div style="display: block;"  id="fitting-suit"> 
	<div class="mt"> 
		<ul class="tab">
			<li style="display:" class="curr"><a href="javascript:void(0);"><strong>最佳组合</strong></a> </li> 
		</ul>  
	</div> 
    
	<div class="mc clearfix">
    	<!--主商品box-->
		<div class="main-good-box">
			<div class="p-img"> 
				<a href="<?php
echo parse_url_tag("u:index|deal|"."act=".$this->_var['mainDeal']['id']."".""); 
?>" target="_blank">
					<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['mainDeal']['icon'],
  'w' => '130',
  'h' => '130',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" alt="<?php echo $this->_var['mainDeal']['sub_name']; ?>" origin="<?php echo $this->_var['mainDeal']['icon']; ?>" width="130" height="130">
				</a> 
			</div> 
			<div class="p-name ac"> 
				<a href="<?php
echo parse_url_tag("u:index|deal|"."act=".$this->_var['mainDeal']['id']."".""); 
?>" title="" target="_blank"><?php echo $this->_var['mainDeal']['name']; ?></a> 
			</div> 
			<div class="p-price ac"> 
            	<?php if ($this->_var['mainDeal']['deal_attr']): ?>
				<label class="ui-checkbox" rel="common_cbo"><input type="checkbox" name="relateCheckbox" value="<?php echo $this->_var['mainDeal']['id']; ?>" id="main_goods" /><strong>&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['mainDeal']['current_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></strong></label>
               	<?php else: ?>
				<input type="checkbox" name="relateCheckbox" value="<?php echo $this->_var['mainDeal']['id']; ?>" style="display:none;" checked="true" id="main_goods" /><strong>&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['mainDeal']['current_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></strong>
			    <?php endif; ?>
				 
			</div>
        </div>
		<div class="jia">+</div>
        <!--关联商品列表box-->
		<div class="combine-content" id="relate_content"> 
		<?php if (count ( $this->_var['goodsList'] ) > 3): ?>
			<i class="t_left"></i>
			<i class="t_right"></i>
		<?php endif; ?>
		<ul class="roll">
		<?php $_from = $this->_var['goodsList']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal');$this->_foreach['goodsList'] = array('total' => count($_from), 'iteration' => 0);
if ($this->_foreach['goodsList']['total'] > 0):
    foreach ($_from AS $this->_var['deal']):
        $this->_foreach['goodsList']['iteration']++;
?>
		<li>
			<div class="p-img"> 
				<a href="<?php
echo parse_url_tag("u:index|deal|"."act=".$this->_var['deal']['id']."".""); 
?>" target="_blank">
					<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['deal']['icon'],
  'w' => '130',
  'h' => '130',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" alt="<?php echo $this->_var['deal']['sub_name']; ?>" origin="<?php echo $this->_var['deal']['icon']; ?>" width="130" height="130">
				</a> 
			</div> 
			<div class="p-name ac"> 
				<a href="<?php
echo parse_url_tag("u:index|deal|"."act=".$this->_var['deal']['id']."".""); 
?>" title="" target="_blank"><?php echo $this->_var['deal']['name']; ?></a> 
			</div> 
			<div class="p-price ac"> 
				<label class="ui-checkbox" rel="common_cbo"><input type="checkbox" name="relateCheckbox"  value="<?php echo $this->_var['deal']['id']; ?>"/><strong>&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['current_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></strong> </label>
				
			</div>
		</li> 
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		
		</ul>
		</div> 
		<!--价格总计div-->
		<div class="relate-price-box">
			<div class="relate-check-num">已选择<span id="relateCheckNum">0</span>个配件</div>
			<div class="relate-check-price" >搭 配 价：<span id="relateCheckCurrPrice">￥0.00</span><br /><span style="text-decoration:line-through;">参 考 价：￥<span id="relateCheckOrigPrice">0.00</span></span></div>
			<div class="relate-check-btn" >
				<button class="ui-button blue" rel="blue" type="button" id="relate_buy_btn">组合购买</button>
			</div>
		</div>
		
		
		
	</div> 
</div>
<?php endif; ?>

<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/filter_row.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/sort_row.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/side_deal_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/deal_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/filter_row.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/filter_row.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/sort_row.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/sort_row.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/deal_list.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/deal_list.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/side_deal_list.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/side_deal_list.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/cate.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/cate.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>
<div class="blank20"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
<!--筛选行-->	
	<?php echo $this->fetch('inc/filter_row.html'); ?>
<!--end筛选行-->	
<div class="blank"></div>
<!--排序行-->	
	<?php echo $this->fetch('inc/sort_row.html'); ?>
<!--end排序行-->	
<div class="blank"></div>
<div class="deal_list_box wrap_full2 f_l">	
	<?php if ($this->_var['deal_list']): ?>
	<ul class="deal_list clearfix">
		<?php $_from = $this->_var['deal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal');if (count($_from)):
    foreach ($_from AS $this->_var['deal']):
?>
			<li>
				<div class="deal_item deal_item_border">
					<!--qr码扫描区-->
					<div rel="qrcode" class="scanbox_deal_list_inner">
					<a class="scan_outter" href="<?php echo $this->_var['deal']['url']; ?>" title="<?php echo $this->_var['deal']['name']; ?>">
						<table><tr><td><img src="<?php 
$k = array (
  'name' => 'gen_scan_qrcode',
  'v' => $this->_var['deal']['url'],
  's' => '4',
);
echo $k['name']($k['v'],$k['s']);
?>" /> </td></tr></table>
						<div></div>
					</a>
					</div>
					<!--end qr码扫描区-->
					<div class="deal_img">
						<div class="tags">					
						<?php $_from = $this->_var['deal']['deal_tags']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'tag');if (count($_from)):
    foreach ($_from AS $this->_var['tag']):
?>				
						<h2 class="tag<?php echo $this->_var['tag']; ?>"></h2>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
						<?php if ($this->_var['deal']['buyin_app'] == 1): ?>
						<h2 class="tag_buyinapp"></h2>
						<?php endif; ?>
						</div>	
						<a href="<?php echo $this->_var['deal']['url']; ?>" class="img"><img lazy="true" src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['deal']['icon'],
  'w' => '296',
  'h' => '200',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" /></a>
						<?php if ($this->_var['deal']['brief']): ?>
						<a href="<?php echo $this->_var['deal']['url']; ?>" class="quan">
							<?php echo $this->_var['deal']['brief']; ?>
						</a>
						<?php endif; ?>
					</div><!--团购图片-->
					<div class="deal_name">
						<a href="<?php echo $this->_var['deal']['url']; ?>"><?php echo $this->_var['deal']['sub_name']; ?></a>
					</div>
					<div class="deal_brief">
							<a href="<?php echo $this->_var['deal']['url']; ?>">
							<?php echo $this->_var['deal']['name']; ?>
							</a>
					</div>
					<div class="deal_price">
						<span class="current_price"><i>&yen;</i><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['current_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
						<span class="origin_price">门店价：&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['origin_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
					</div>
					<div class="deal_extra">
						<div class="sale_count">
							已售<span><?php echo $this->_var['deal']['buy_count']; ?></span>
						</div>
						<div class="sale_review">							
				        	<span>
								<input class="ui-starbar" value="<?php echo $this->_var['deal']['avg_point']; ?>" disabled="true"  />
							</span>
							</span>
							<span class="review_count"><i><?php echo $this->_var['deal']['dp_count']; ?></i>人点评</span>						
						</div>
					</div>
				</div><!--end deal_item-->
			</li>
			
			
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</ul>

		<div class="pages"><?php echo $this->_var['pages']; ?></div>
		<div class="blank"></div>
		<?php else: ?>
		<div class="empty_tip">没有数据</div>
		<?php endif; ?>
</div><!--end deal_list_box-->
<div class="f_r wrap_s2">
	<?php if ($this->_var['side_deal_list']): ?>
	<div class="side_deal_box">
	<div class="title_row">销量排行</div>
	<div class="content_row">		
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
					</span>
					<span class="sale_count f_r">
						已售<span><?php echo $this->_var['side_deal']['buy_count']; ?></span>
					</span>
				</div>
			</li>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			
		</ul>
		
		
		
	</div>
	</div>
	<div class="blank"></div>
	<?php endif; ?>
	
	
	<?php if ($this->_var['history_deal_list']): ?>
	<div class="side_deal_box">
	<div class="title_row">
		<span>浏览历史</span>
		<a href="javascript:void(0);" class="clear_history" type="shop">清空</a>
	</div>
	<div class="content_row">		
		<ul class="side_deal_list">
			<?php $_from = $this->_var['history_deal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'side_deal');if (count($_from)):
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
					</span>
					<span class="sale_count f_r">
						已售<span><?php echo $this->_var['side_deal']['buy_count']; ?></span>
					</span>
				</div>
			</li>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			
		</ul>	
		
	</div>
	</div>
	<?php endif; ?>
</div>
<div class="blank"></div>
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
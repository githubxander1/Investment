<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/mall.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/mall.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/mall.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>

<?php if ($this->_var['index_cates']): ?>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>" id="flow_cate_outer">
<div id="flow_cate">
		<ul>
			<?php $_from = $this->_var['index_cates']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'index_cate');if (count($_from)):
    foreach ($_from AS $this->_var['index_cate']):
?>
			<?php if ($this->_var['index_cate']['deal_list']): ?>
			<li rel="index_cate_<?php echo $this->_var['index_cate']['id']; ?>" <?php if ($this->_var['index_cate']['iconcolor']): ?>bg="<?php echo $this->_var['index_cate']['iconcolor']; ?>"<?php endif; ?>>
				<?php if ($this->_var['index_cate']['iconfont']): ?>
				<i class="diyfont"><?php echo $this->_var['index_cate']['iconfont']; ?></i>
				<?php endif; ?>
				<font><?php echo $this->_var['index_cate']['name']; ?></font>
			</li>
			<?php endif; ?>
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		</ul>
</div>
</div>
<?php endif; ?>


<div id="main_roll">
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>" id="wrap">
	<div id="full_outer">
		<div id="scroll_outer">
		<ul>
		<li><adv adv_id="商城首页轮播广告1" /></li>
		<li><adv adv_id="商城首页轮播广告2" /></li>
		</ul>
		</div>
	</div>		
</div>	
</div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> cate_row">
	<div class="fix_cate_tree">
			<?php 
$k = array (
  'name' => 'load_cate_tree',
  'c' => '6',
  't' => $this->_var['cate_tree_type'],
);
echo $k['name']($k['c'],$k['t']);
?>
	</div>
</div>	
<?php if ($this->_var['notice_list']): ?>
<div class="notice_row">
	<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
			<div class="notice_board">
				<i class="iconfont f_l">&#xe618;</i>
				<ul>
					<?php $_from = $this->_var['notice_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'news');if (count($_from)):
    foreach ($_from AS $this->_var['news']):
?>
					<li><a href="<?php echo $this->_var['news']['url']; ?>"><?php echo $this->_var['news']['title']; ?></a></li>									
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
				</ul>
				<a href="<?php
echo parse_url_tag("u:index|news|"."".""); 
?>" class="more f_l news_more">更多</a>
			</div>
	</div>	
</div>
<?php endif; ?>

<div class="blank"></div>

<!--推荐的团购分类-->
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
	
<?php if ($this->_var['index_cates']): ?>	
	<?php $_from = $this->_var['index_cates']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'index_cate');if (count($_from)):
    foreach ($_from AS $this->_var['index_cate']):
?>
	<?php if ($this->_var['index_cate']['deal_list']): ?>
	<div class="index_cate" rel="index_cate_<?php echo $this->_var['index_cate']['id']; ?>">
		<div class="title_row">
			<div class="title"><?php if ($this->_var['index_cate']['iconfont']): ?><i class="diyfont"><?php echo $this->_var['index_cate']['iconfont']; ?></i>&nbsp;&nbsp;<?php endif; ?><?php echo $this->_var['index_cate']['name']; ?></div>
			
			<ul>
				<?php $_from = $this->_var['index_cate']['deal_cate_type_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'cate_type');$this->_foreach['type_loop'] = array('total' => count($_from), 'iteration' => 0);
if ($this->_foreach['type_loop']['total'] > 0):
    foreach ($_from AS $this->_var['cate_type']):
        $this->_foreach['type_loop']['iteration']++;
?>
				<li><a href="<?php
echo parse_url_tag("u:index|cate|"."cid=".$this->_var['cate_type']['id']."".""); 
?>"><?php echo $this->_var['cate_type']['name']; ?></a><?php if (! ($this->_foreach['type_loop']['iteration'] == $this->_foreach['type_loop']['total'])): ?> | <?php endif; ?></li>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</ul>
			<a href="<?php
echo parse_url_tag("u:index|cate|"."cid=".$this->_var['index_cate']['id']."".""); 
?>" class="more">更多</a>
		</div>
		<div class="content_row clearfix">
			<ul class="tuan_list">
				
				<?php $_from = $this->_var['index_cate']['deal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal');if (count($_from)):
    foreach ($_from AS $this->_var['deal']):
?>
				
				<li>
					<div class="tuan_item tuan_item_border">
						<!--qr码扫描区-->
						<div rel="qrcode" class="scanbox_deal_list">
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
						<div class="tuan_img">
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
  'w' => '275',
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
						<div class="tuan_name">
							<a href="<?php echo $this->_var['deal']['url']; ?>"><?php echo $this->_var['deal']['sub_name']; ?></a>
						</div>
						<div class="tuan_brief">
							<a href="<?php echo $this->_var['deal']['url']; ?>">
							<?php echo $this->_var['deal']['name']; ?>
							</a>
						</div>
						<div class="tuan_price">
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
						<div class="tuan_extra">
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
					</div><!--end tuan_item-->
				</li>
				
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
				
			</ul>
			<div class="clear"></div>
		</div>
	</div>
	<?php endif; ?>
	<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
<?php endif; ?>		
			
				
					


</div>
<!--end 推荐团购分类-->

<?php echo $this->fetch('inc/footer.html'); ?>
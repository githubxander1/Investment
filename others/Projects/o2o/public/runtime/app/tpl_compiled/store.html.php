<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/store.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/business_address.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/side_deal_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/review_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/sort_row.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fancybox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/jquery.fancybox-thumbs.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery-1.6.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.fancybox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.fancybox-thumbs.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/business_address.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/business_address.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/review_list.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/review_list.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/store.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/store.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/side_deal_list.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/side_deal_list.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'BAIDU_MAP_APPKEY',
);
echo $k['name']($k['v']);
?>"></script> 
<script type="text/javascript">
	var STORE_IMAGES = <?php echo $this->_var['store_images_json']; ?>;

</script>
<div class="blank20"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> clearfix">

		<div class="store_info clearfix">
			<div class="f_l show_img">
			<a href="javascript:void(0);" id="store_image">
				<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['store_info']['preview'],
  'w' => '100',
  'h' => '75',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" />
				<span>所有图片(<?php echo $this->_var['store_images_count']; ?>)</span>
			</a>
			</div>
			
			<div class="f_l show_detail">
				<div class="show_name"><?php echo $this->_var['store_info']['name']; ?><a class="kf_qq" href="http://wpa.qq.com/msgrd?v=3&uin=<?php echo $this->_var['store_info']['location_qq']; ?>&site=qq&menu=yes" ><i class="iconfont">&#xe64a;</i>客服QQ</a></div>
				<div class="show_address"><i class="iconfont">&#xe615;</i>&nbsp;<?php echo $this->_var['store_info']['address']; ?><?php if ($this->_var['store_info']['route']): ?>&nbsp;交通路线：<?php echo $this->_var['store_info']['route']; ?><?php endif; ?></div>
				<div class="show_tel"><i class="iconfont">&#xe623;</i>&nbsp;<?php echo $this->_var['store_info']['tel']; ?></div>
			</div>
			
			<div class="f_r store_dp">
				<div class="store_dp_avg">总评  <input class="ui-starbar" value="<?php echo $this->_var['store_info']['avg_point']; ?>" disabled="true" /> </div>
				<div class="store_dp_total"><i class="iconfont">&#xe621;</i> (<em><?php echo $this->_var['store_info']['dp_count']; ?></em>)人点评，好评率 <?php echo $this->_var['store_info']['good_rate_precent']; ?>%</div>
				<div class="store_dp_price"><i class="iconfont">&#xe622;</i> 人均消费：<em><?php echo $this->_var['store_info']['ref_avg_price']; ?></em> 元</div>
			</div>
		</div>
		<div class="store-adv-1">
			<?php echo $this->_var['store_info']['adv_img_1']; ?>
		</div>
		<div class="blank20"></div>
		
		
		<div class="clearfix">
			<div class="wrap_m2 f_l">
			

			<!--详情导航-->
			<div class="show-nav" id="rel_nav">
			<!--{start: 详情导航 -->
			<ul>	
				<?php if ($this->_var['store_info']['brief']): ?>
				<li rel="n0">商户介绍</li>
				<?php endif; ?>			
				<li rel="n1">商家位置</li>
				
				<?php if (! $this->_var['preview']): ?>
				<?php if ($this->_var['store_info']['tuan_count'] > 0): ?>
				<li rel="n2">正在团购</li>
				<?php endif; ?>
				<?php if ($this->_var['store_info']['shop_count'] > 0): ?>
				<li rel="n3">商城购物</li>
				<?php endif; ?>
				<?php if ($this->_var['store_info']['youhui_count'] > 0): ?>
				<li rel="n4">商家优惠</li>
				<?php endif; ?>
				<?php if ($this->_var['store_info']['event_count'] > 0): ?>
				<li rel="n5">商家活动</li>
				<?php endif; ?>
				<li rel="n6">消费评价</li>
				<?php endif; ?>
			</ul>
			<!--}end: 详情导航 -->
			</div>
			<div style="display:none;" class="fix-nav wrap_m2">
				<!--{start: 浮动导航 -->
				<div class="show-nav">
					<!--{start: 详情导航 -->
					<ul class="f_l">
						<?php if ($this->_var['store_info']['brief']): ?>
						<li rel="n0">商户介绍</li>
						<?php endif; ?>	
						<li rel="n1">商家位置</li>		
							
						<?php if (! $this->_var['preview']): ?>		
						<?php if ($this->_var['store_info']['tuan_count'] > 0): ?>
						<li rel="n2">正在团购</li>
						<?php endif; ?>
						<?php if ($this->_var['store_info']['shop_count'] > 0): ?>
						<li rel="n3">商城购物</li>
						<?php endif; ?>
						<?php if ($this->_var['store_info']['youhui_count'] > 0): ?>
						<li rel="n4">商家优惠</li>
						<?php endif; ?>
						<?php if ($this->_var['store_info']['event_count'] > 0): ?>
						<li rel="n5">商家活动</li>
						<?php endif; ?>
						<li rel="n6">消费评价</li>
						<?php endif; ?>
					</ul>
					
					<!--}end: 详情导航 -->
				</div>
				<!--}end: 浮动导航 -->
			</div>
			<!--end 详情导航-->
			<div class="show-content">
				<?php if ($this->_var['store_info']['brief']): ?>
				<div rel="n0" class="content_box">
					<div class="box_title nomargin">商户介绍</div>
					<div class="box_content">
						<?php echo $this->_var['store_info']['brief']; ?>
					</div>
				</div>
				<?php endif; ?>
				<div rel="n1" class="content_box">
					<div class="box_title nomargin">商家位置</div>
					<div class="box_content nopadding">
						<div id="business_address" supplier_id="<?php echo $this->_var['store_info']['supplier_id']; ?>">
						
						</div>
					</div>
				</div>		
				
				<?php if (! $this->_var['preview']): ?>		
				<?php if ($this->_var['store_info']['tuan_count'] > 0): ?>
				<div rel="n2" class="content_box">
					<div class="box_title nomargin">正在团购</div>
					<div class="box_content nopadding">
						<div id="supplier_deal" store_id="<?php echo $this->_var['store_info']['id']; ?>">
						</div>
					</div>
				</div>
				<?php endif; ?>
				<?php if ($this->_var['store_info']['shop_count'] > 0): ?>
				<div rel="n3" class="content_box">
					<div class="box_title nomargin">商城购物</div>
					<div class="box_content nopadding">
						<div id="supplier_shop" store_id="<?php echo $this->_var['store_info']['id']; ?>">
						</div>
					</div>
				</div>
				<?php endif; ?>
				<?php if ($this->_var['store_info']['youhui_count'] > 0): ?>
				<div rel="n4" class="content_box">
					<div class="box_title nomargin">商家优惠</div>
					<div class="box_content nopadding">
						<div id="supplier_youhui" store_id="<?php echo $this->_var['store_info']['id']; ?>">
						</div>
					</div>
				</div>
				<?php endif; ?>
				<?php if ($this->_var['store_info']['event_count'] > 0): ?>
				<div rel="n5" class="content_box">
					<div class="box_title nomargin">商家活动</div>
					<div class="box_content nopadding">
						<div id="supplier_event" store_id="<?php echo $this->_var['store_info']['id']; ?>">
						</div>
					</div>
				</div>
				<?php endif; ?>
				<div rel="n6" class="content_box">
					<div class="box_title">
						<div class="box_title_text">商户评价</div>
						<div class="box_title_more"><a href="<?php
echo parse_url_tag("u:index|review|"."location_id=".$this->_var['store_info']['id']."".""); 
?>" target="_blank">我要评价</a></div>
					</div>
					<div class="box_content">
						<div id="review_list" location_id="<?php echo $this->_var['store_info']['id']; ?>">
						</div>
					</div>
				</div>
				<?php endif; ?>
				<div class="content_box"></div>
			</div>
		</div><!--end wrap_m2-->
		<div class="wrap_s2 f_r">
		<div class="store-adv-2">
			<?php echo $this->_var['store_info']['adv_img_2']; ?>
		</div>
		<div class="blank"></div>
			<?php if ($this->_var['side_deal_list']): ?>
			<div class="side_deal_box">
			<div class="title_row">您可能喜欢的</div>
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
				<a href="javascript:void(0);" class="clear_history" type="store">清空</a>
			</div>
			<div class="content_row">
				<ul class="side_deal_list">
					<?php $_from = $this->_var['history_deal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'side_store');if (count($_from)):
    foreach ($_from AS $this->_var['side_store']):
?>
					<li>
						<a href="<?php echo $this->_var['side_store']['url']; ?>" class="deal_img"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['side_store']['preview'],
  'w' => '198',
  'h' => '134',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" /></a>
						<a href="<?php echo $this->_var['side_store']['url']; ?>"  class="deal_title"><?php echo $this->_var['side_store']['name']; ?></a>
						
					</li>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					
				</ul>
			</div>
			</div>
			<?php endif; ?>
		</div>
	</div>

</div>
<div class="blank20"></div>

<?php echo $this->fetch('inc/footer.html'); ?>
<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/filter_row.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/sort_row.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/stores.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/store_pop_map.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/side_deal_list.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/filter_row.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/filter_row.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/sort_row.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/sort_row.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/store_pop_map.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/store_pop_map.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/stores.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/stores.js";
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
<div class="blank15"></div>
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
</div>
<div class="blank"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> clearfix">	
	<div class="wrap_m2 f_l store_list">
		<?php if ($this->_var['supplier_info']): ?>
		<div class="supplier_info clearfix">
			<div class="sp_image f_l">
				<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['supplier_info']['preview'],
  'w' => '100',
  'h' => '75',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" />
			</div>
			<div class="sp_info f_l">
				<span class="sp_name"><?php echo $this->_var['supplier_info']['name']; ?></span>
				<?php if ($this->_var['location_count']): ?>
				<br />
				<span class="sp_total"><span class="sp_city"><i class="iconfont">&#xe615;</i><?php echo $this->_var['current_city']['name']; ?></span> 共有 <span class="sp_count"><?php echo $this->_var['location_count']; ?></span> 家分店</span>
				<?php endif; ?>
			</div>
		</div>
		<div class="blank"></div>
		<?php endif; ?>
		<?php if ($this->_var['store_list']): ?>
		<!--商家列表单行-->
		
		<?php $_from = $this->_var['store_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'store_item');if (count($_from)):
    foreach ($_from AS $this->_var['store_item']):
?>
		<div class="store_row clearfix">
			<!--qr码扫描区-->
			<div rel="qrcode" class="scan_store_list">
			<a class="scan_outter" href="<?php echo $this->_var['store_item']['url']; ?>" title="<?php echo $this->_var['store_item']['name']; ?>">
				<table><tr><td><img src="<?php 
$k = array (
  'name' => 'gen_scan_qrcode',
  'v' => $this->_var['store_item']['url'],
  's' => '3',
);
echo $k['name']($k['v'],$k['s']);
?>" /> </td></tr></table>
				<div></div>
			</a>
			</div>
			<!--end qr码扫描区-->
			<div class="store_image f_l">
				<a href="<?php echo $this->_var['store_item']['url']; ?>" title="<?php echo $this->_var['store_item']['name']; ?>">
				<img lazy="true" src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['store_item']['preview'],
  'w' => '200',
  'h' => '150',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" />
				</a>
			</div>
			<div class="store_info f_l">
				<a href="<?php echo $this->_var['store_item']['url']; ?>" class="store_name" title="<?php echo $this->_var['store_item']['name']; ?>">
					<?php echo $this->_var['store_item']['name']; ?>
					<?php if ($this->_var['store_item']['is_verify']): ?>
					<i class="iconfont" title="认证商户">&#xe629;</i>
					<?php endif; ?>
				</a>
				<div class="store_address"><i class="iconfont">&#xe615;</i> <?php if ($this->_var['store_item']['address']): ?><?php echo $this->_var['store_item']['address']; ?> &nbsp;<a href="javascript:void(0);" class="store_pop_map" rel="<?php echo $this->_var['store_item']['id']; ?>">[查看地图]</a><?php else: ?>商家未填写地址<?php endif; ?></div>
				<div class="store_phone"><i class="iconfont">&#xe623;</i> <em><?php if ($this->_var['store_item']['tel']): ?><?php echo $this->_var['store_item']['tel']; ?><?php else: ?>无<?php endif; ?></em></div>
			</div>
			
			<div class="store_dp f_r">
				<div class="store_dp_avg">总评  <input class="ui-starbar" value="<?php echo $this->_var['store_item']['avg_point']; ?>" disabled="true" /> </div>
				<div class="store_dp_total"><i class="iconfont">&#xe621;</i> (<em><?php echo $this->_var['store_item']['dp_count']; ?></em>)人点评，好评率 <?php echo $this->_var['store_item']['good_rate_precent']; ?>%</div>
				<div class="store_dp_price"><i class="iconfont">&#xe622;</i> 人均消费：<em><?php echo $this->_var['store_item']['ref_avg_price']; ?></em> 元</div>
			</div>
		</div>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		
		<!--商家列表单行-->
		<div class="blank"></div>
		<div class="pages"><?php echo $this->_var['pages']; ?></div>
		<?php else: ?>
		
		<div class="layout_box">
			<div class="content">					
				<div class="empty_tip">没有相关数据</div>
			</div>
		</div>
		
		<?php endif; ?>
		
	</div>	
	<div class="wrap_s2 f_r">
		<?php if ($this->_var['side_store_list']): ?>
		<div class="side_deal_box">
		<div class="title_row">口碑排行</div>
		<div class="content_row">
			<ul class="side_deal_list">
				<?php $_from = $this->_var['side_store_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'side_store');if (count($_from)):
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
					<div class="deal_info">
						<span class="deal_price f_l">
							好评率:<?php echo $this->_var['side_store']['good_rate_precent']; ?>%
						</span>
						<span class="sale_count f_r">
							总评：<input class="ui-starbar" disabled="true" value="<?php echo $this->_var['side_store']['avg_point']; ?>" />
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
</div><!--end wrap-->
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
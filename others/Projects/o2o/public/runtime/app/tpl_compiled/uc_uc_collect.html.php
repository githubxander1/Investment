<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_collect.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/plupload.full.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_collect.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_collect.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>

<div class="blank20"></div>

<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> clearfix">
	<div class="side_nav left_box">
		<?php echo $this->fetch('inc/uc_nav_list.html'); ?>
	</div>
	<div class="right_box">
		
		<div class="main_box uc_info_box">
			<div class="info_nav">
				<ul>
					<li id="deal_li"  <?php if ($this->_var['type'] == "deal"): ?>class="cur"<?php endif; ?>><a href="<?php
echo parse_url_tag("u:index|uc_collect|"."".""); 
?>">商品团购收藏</a></li>
					<li id="youhui_li" <?php if ($this->_var['type'] == "youhui"): ?>class="cur"<?php endif; ?>><a href="<?php
echo parse_url_tag("u:index|uc_collect#youhui_collect|"."".""); 
?>">优惠券收藏</a></li>
					<li id="event_li" <?php if ($this->_var['type'] == "event"): ?>class="cur"<?php endif; ?>><a href="<?php
echo parse_url_tag("u:index|uc_collect#event_collect|"."".""); 
?>">活动收藏</a></li>
					<li id="dc_location_li" <?php if ($this->_var['type'] == "dc_location"): ?>class="cur"<?php endif; ?>><a href="<?php
echo parse_url_tag("u:index|uc_collect#dc_location_collect|"."".""); 
?>">餐厅收藏</a></li>
				</ul>
			</div>						
			<div class="blank20"></div>
			
			
			<?php if ($this->_var['list']): ?>
			<div class="info_table">
				<table>
					<tbody>
						<tr>
							<th width="auto">名称</th>
							<th width="130">收藏时间</th>
							<th width="100">操作</th>
						</tr>
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'deal');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['deal']):
?>
						<tr class="alt">
                               <td><a href="<?php echo $this->_var['deal']['url']; ?>" title="<?php echo $this->_var['deal']['name']; ?>" target="_blank"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['deal']['name'],
  'b' => '0',
  'e' => '40',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a></td>
                               <td class="ctime"><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['deal']['add_time'],
);
echo $k['name']($k['v']);
?></td>
                               <td class="operate" >
									<a href="<?php echo $this->_var['deal']['url']; ?>" target="_blank"><?php echo $this->_var['LANG']['VIEW']; ?></a>												
									<a href="javascript:void(0);" class="del" url="<?php echo $this->_var['deal']['del_url']; ?>"><?php echo $this->_var['LANG']['DELETE']; ?></a>
								</td>
                         </tr>
                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                          

					</tbody>
				</table>
				
			</div>			
			
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>
			
			<?php else: ?>
			<div class="empty_tip">没有收藏记录</div>
			<?php endif; ?>
			
			
			
			
			
			
			
			
			
			



		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
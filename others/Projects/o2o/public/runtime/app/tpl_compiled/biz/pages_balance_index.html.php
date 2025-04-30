<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/balance.css";
/*日期控件*/
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/jquery.datetimepicker.css";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery-1.8.2.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";

/*日期控件*/
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.datetimepicker.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/time_ipt.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/time_ipt.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/search_page.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/search_page.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/swfobject.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/balance/balance.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/balance/balance.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script type="text/javascript">
	var ofc_data_url = '<?php echo $this->_var['ofc_data_url']; ?>';
</script>
<div class="blank20"></div>
<div class="page wrap_full">
	<div class="left_box">
		<?php echo $this->fetch('inc/biz_nav_list.html'); ?>
	</div>
	<div class="right_box">
		<div class="content">
			<div class="head_box">
				<div class="standard_tab cf">
				<ul>
					<li class="<?php if ($this->_var['ACTION_NAME'] == 'index'): ?>curr<?php endif; ?>"><a href="<?php
echo parse_url_tag("u:biz|balance#index|"."".""); 
?>">财务概况</a></li>
					<li class="<?php if ($this->_var['ACTION_NAME'] == 'line'): ?>curr<?php endif; ?>"><a href="<?php
echo parse_url_tag("u:biz|balance#line|"."".""); 
?>">销售走势</a></li>
					<li class="<?php if ($this->_var['ACTION_NAME'] == 'detail'): ?>curr<?php endif; ?>"><a href="<?php
echo parse_url_tag("u:biz|balance#detail|"."".""); 
?>">财务明细</a></li>
				</ul>
			</div>
			</div>
			
			<div class="info_table">
				<div class="blank"></div>
				<form name="search_form" action="<?php
echo parse_url_tag("u:biz|balance|"."".""); 
?>" method="post">
				<table>
					<tr>
						<td width="165"><input class="ui-textbox search_box time_input" name="begin_time"  value="<?php echo $this->_var['begin_time']; ?>" readonly="readonly" /></td>
						<td width="5">-</td>
						<td width="165"><input class="ui-textbox search_box time_input" name="end_time" value="<?php echo $this->_var['end_time']; ?>" readonly="readonly" /></td>
						<td width="100">
							<input type="hidden" name="method" value="search" />
							<button class="ui-button add_goods_type" rel="white" type="submit">搜索</button>
						</td>
						<td></td>
					</tr>
				</table>
				</form>

				<div class="blank"></div>
			</div>
			
			<div class="info_box">
				<table>
					<tr>
						<td width=450>
							<div class="main_color">总销售额<?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['sale_money'],
);
echo $k['name']($k['v']);
?>，财务概况图例</div>
							<div id="data_chart"></div>
						</td>
						<td valign="top">
							<div class="bg_box growth_content">					
							<div class="info_items">
								<ul>
									<li><label>总销售额：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['sale_money'],
);
echo $k['name']($k['v']);
?></span></li>	
									<li><label>退款金额：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['refund_money'],
);
echo $k['name']($k['v']);
?></span></li>							
									<li><label>未消费：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['lock_money'],
);
echo $k['name']($k['v']);
?></span></li>								
									<li><label>未提现：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['money'],
);
echo $k['name']($k['v']);
?></span> &nbsp;&nbsp; <a href="<?php
echo parse_url_tag("u:biz|withdrawal|"."".""); 
?>" >【申请提现】</a></li>
									<li><label>已提现：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['supplier_info']['wd_money'],
);
echo $k['name']($k['v']);
?></span></li>		
								</ul>
							</div>
							</div>
							<div class="bg_box growth_content">					
							<div class="info_items">
								<ul>
									<li><span class="main_color"><?php echo $this->_var['stat_title']; ?> 报表</span></li>	
									<li><label><?php echo $this->_var['stat_title']; ?> 销售额：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['stat_info']['sale_money'],
);
echo $k['name']($k['v']);
?></span></li>	
									<li><label><?php echo $this->_var['stat_title']; ?> 退款金额：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['stat_info']['refund_money'],
);
echo $k['name']($k['v']);
?></span></li>								
									<li><label><?php echo $this->_var['stat_title']; ?> 消费：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['stat_info']['money'],
);
echo $k['name']($k['v']);
?></span></li>
									<li><label><?php echo $this->_var['stat_title']; ?> 提现：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['stat_info']['wd_money'],
);
echo $k['name']($k['v']);
?></span></li>		
								</ul>
							</div>
							</div>
						</td>
					</tr>
					<tr>
						<td colspan=2 style="padding:5px 0px;">
							图示说明：
						</td>
					</tr>
					<tr>
						<td colspan=2>
							<span class="icon_span" style="background:#d01f3c;"></span>
							<span class="icon_tip">商户未提现</span>
							<span class="icon_span" style="background:#f5a8df;"></span>
							<span class="icon_tip">商户已提现</span>
							<span class="icon_span" style="background:#356aa0;"></span>
							<span class="icon_tip">客户未消费</span>
							<span class="icon_span" style="background:#C79810;"></span>
							<span class="icon_tip">客户退款</span>
						</td>
					</tr>
				</table>
				
			</div>		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
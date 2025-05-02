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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/balance/balance_line.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/balance/balance_line.js";
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
echo parse_url_tag("u:biz|balance#line|"."".""); 
?>" method="post">
				<table>
					<tr>
						<td width=50>日期</td>
						<td width="105" class="select_row">
							<select name="year" class="ui-select filter_select" height=100>
								<?php $_from = $this->_var['year_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'year_0_20803800_1484917133');if (count($_from)):
    foreach ($_from AS $this->_var['year_0_20803800_1484917133']):
?>
								<option value="<?php echo $this->_var['year_0_20803800_1484917133']['year']; ?>" <?php if ($this->_var['year_0_20803800_1484917133']['current']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['year_0_20803800_1484917133']['year']; ?>年</option>
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							</select>
						</td>						
						<td width="105" class="select_row">							
							<select name="month" class="ui-select filter_select" height=100>
								<?php $_from = $this->_var['month_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'month_0_20829200_1484917133');if (count($_from)):
    foreach ($_from AS $this->_var['month_0_20829200_1484917133']):
?>
								<option value="<?php echo $this->_var['month_0_20829200_1484917133']['month']; ?>" <?php if ($this->_var['month_0_20829200_1484917133']['current']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['month_0_20829200_1484917133']['month']; ?>月</option>
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							</select>
						</td>						
						<td width="50">
							<button class="ui-button add_goods_type" rel="white" type="submit">搜索</button>
						</td>
						<td></td>
					</tr>
				</table>
				</form>

				<div class="blank"></div>
			</div>
			
			<div class="blank"></div>
			<table>
				<tr>
					<td width=20></td>
					<td width=768><div id="data_line_chart"></div></td>
					<td width=20></td>
				</tr>
			</table>		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
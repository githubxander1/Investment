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
?>

<?php echo $this->fetch('inc/header.html'); ?>
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
echo parse_url_tag("u:biz|balance#detail|"."".""); 
?>" method="post">
				<table>
					<tr>
						<td width="165"><input class="ui-textbox search_box time_input" name="begin_time" holder="查询起始日期" value="<?php echo $this->_var['begin_time']; ?>" readonly="readonly" /></td>
						<td width="5">-</td>
						<td width="165"><input class="ui-textbox search_box time_input" name="end_time" holder="查询截止日期" value="<?php echo $this->_var['end_time']; ?>" readonly="readonly" /></td>
						<td width="35">类型</td>
						<td width="105" class="select_row">							
							<select name="type" class="ui-select filter_select" height=100>
					
								<option value="1" <?php if ($this->_var['type'] == 1): ?>selected="selected"<?php endif; ?>>销售明细</option>
								<option value="3" <?php if ($this->_var['type'] == 3): ?>selected="selected"<?php endif; ?>>消费明细</option>
								<option value="4" <?php if ($this->_var['type'] == 4): ?>selected="selected"<?php endif; ?>>退款明细</option>
								<option value="5" <?php if ($this->_var['type'] == 5): ?>selected="selected"<?php endif; ?>>打款明细</option>
							
							</select>
						</td>
						<td width="60">
							<input type="hidden" name="method" value="search" />
							<button class="ui-button add_goods_type" rel="white" type="submit">搜索</button>
						</td>
						<td></td>
					</tr>
				</table>
				</form>

				<div class="blank"></div>
			</div>
			
			
			<?php if ($this->_var['list']): ?>
			<div class="info_table">
				<table>
					<tbody>
						<tr>
							<th>日志</th>							
							<th width=100>金额</th>
							<th width=150>发生时间</th>
						</tr>
						<tr class="alt sum">
                               <td class="tr" colspan=3>
                               	本页合计：<span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['page_sum'],
);
echo $k['name']($k['v']);
?></span>&nbsp;&nbsp;
								合计：<span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['sum'],
);
echo $k['name']($k['v']);
?></span>
								</td>                              

                        </tr>
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
						<tr class="alt">
                               <td class="log_info"><?php echo $this->_var['item']['log_info']; ?></td>
                               <td><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['money'],
);
echo $k['name']($k['v']);
?></td>
                               <td><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['create_time'],
);
echo $k['name']($k['v']);
?></td>

                         </tr>
                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                         <tr class="alt sum">
                               <td class="tr" colspan=3>
                               	本页合计：<span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['page_sum'],
);
echo $k['name']($k['v']);
?></span>&nbsp;&nbsp;
								合计：<span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['sum'],
);
echo $k['name']($k['v']);
?></span>
								</td>                              

                         </tr>

					</tbody>
				</table>
				
			</div>	
			
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>			
			<?php else: ?>
			<div class="empty_tip">没有相关明细</div>
			<?php endif; ?>
				

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
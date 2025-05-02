<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/jquery.datetimepicker.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery-1.8.2.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
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
				<h2><?php echo $this->_var['head_title']; ?></h2>
			</div>

			<div class="info_table">
				<div class="blank"></div>
				<form name="search_form" action="<?php
echo parse_url_tag("u:biz|youhuio|"."".""); 
?>" method="post">
				<table>
					<tr>
						<td width="165"><input class="ui-textbox search_box time_input" name="begin_time" holder="下载起始日期" value="<?php echo $this->_var['begin_time']; ?>" readonly="readonly" /></td>
						<td width="5">-</td>
						<td width="165"><input class="ui-textbox search_box time_input" name="end_time" holder="下载截止日期" value="<?php echo $this->_var['end_time']; ?>" readonly="readonly" /></td>
						<td width="50">名称</td>
						<td width="165"><input class="ui-textbox search_box" name="name" holder="优惠券名称" value="<?php echo $this->_var['name']; ?>" /></td>
						<td></td>
						<td width="100">
							<input type="hidden" name="method" value="search" />
							<button class="ui-button add_goods_type" rel="white" type="submit">搜索</button>
						</td>
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
							<th>优惠券名称</th>
							<th>会员</th>
							<th>下载时间</th>
							<th>过期时间</th>
							<th>消费门店</th>
							<th>消费时间</th>
						</tr>
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
						<tr class="alt">
                               <td><a href="<?php echo $this->_var['item']['url']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['item']['youhui_name'],
  'b' => '0',
  'e' => '20',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a></td>
                               <td class="detail"><?php echo $this->_var['item']['user_name']; ?></td>
                               <td><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['create_time'],
);
echo $k['name']($k['v']);
?></td>
                               <td  class="detail"><?php echo $this->_var['item']['expire_time']; ?></td>
                               <td style="border-right: 1px dotted #E5E5E5;"><?php echo $this->_var['item']['location_name']; ?></td>
                               <td><?php if ($this->_var['item']['confirm_time'] == 0): ?>未消费<?php else: ?><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['confirm_time'],
);
echo $k['name']($k['v']);
?><?php endif; ?></td>
                         </tr>
                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                          

					</tbody>
				</table>
				
			</div>	
			
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>			
			<?php else: ?>
			<div class="empty_tip">没有优惠券下载记录</div>
			<?php endif; ?>			
		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
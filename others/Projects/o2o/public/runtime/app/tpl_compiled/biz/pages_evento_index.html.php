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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/evento/evento.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/evento/evento.js";
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
echo parse_url_tag("u:biz|evento|"."".""); 
?>" method="post">
				<table>
					<tr>
						<td width="165"><input class="ui-textbox search_box time_input" name="begin_time"  value="<?php echo $this->_var['begin_time']; ?>" readonly="readonly" /></td>
						<td width="5">-</td>
						<td width="165"><input class="ui-textbox search_box time_input" name="end_time"  value="<?php echo $this->_var['end_time']; ?>" readonly="readonly" /></td>
						<td width="50">名称</td>
						<td width="165"><input class="ui-textbox search_box" name="name" holder="活动名称" value="<?php echo $this->_var['name']; ?>" /></td>
						
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
							<th>活动名称</th>
							<th>会员</th>
							<th>活动详情</th>
							<th>报名详情</th>
							<th>验证门店</th>
							<th>状态</th>
						</tr>
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
						<tr class="alt">
                               <td><a href="<?php echo $this->_var['item']['url']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['item']['event_name'],
  'b' => '0',
  'e' => '20',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a></td>
                               <td class="detail"><?php echo $this->_var['item']['user_name']; ?></td>
                               <td>
                               		   活动开始时间：<?php if ($this->_var['item']['event_begin_time'] == 0): ?>已开始<?php else: ?><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['event_begin_time'],
);
echo $k['name']($k['v']);
?><?php endif; ?><br>
                               		   活动结束时间：<?php if ($this->_var['item']['event_end_time'] == 0): ?>永久有效<?php else: ?><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['event_end_time'],
);
echo $k['name']($k['v']);
?><?php endif; ?><br>
                               </td>
                               <td  class="detail">                              
                               <?php $_from = $this->_var['item']['fields']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'fields');if (count($_from)):
    foreach ($_from AS $this->_var['fields']):
?>
                               		  <?php echo $this->_var['fields']['field_show_name']; ?>：<?php echo $this->_var['fields']['result']; ?><br>
                                <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                                 报名时间：<?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['create_time'],
);
echo $k['name']($k['v']);
?><br>
                               </td>
                               <td style="border-right: 1px dotted #E5E5E5;"><?php echo $this->_var['item']['location_name']; ?></td>
                               <td class="sub_status">
                               	<?php if ($this->_var['item']['is_verify'] == 1): ?>
								已审核
								<?php elseif ($this->_var['item']['is_verify'] == 2): ?>
								已拒绝
								<?php else: ?>
								<a href="javascript:void(0);" url="<?php echo $this->_var['item']['go_url']; ?>" class="approval">通过审核</a>
								<br />
								<a href="javascript:void(0);" url="<?php echo $this->_var['item']['refuse_url']; ?>" class="refuse">拒绝</a>
								<?php endif; ?>
								</td>
                         </tr>
                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                          

					</tbody>
				</table>
				
			</div>	
			
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>			
			<?php else: ?>
			<div class="empty_tip">没有报名记录</div>
			<?php endif; ?>			
		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
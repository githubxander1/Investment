<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/dealo.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/dealo/dealo.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/dealo/dealo.js";
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
echo parse_url_tag("u:biz|dealo|"."".""); 
?>" method="post">
				<table>
					<tr>
						<td width="165"><input class="ui-textbox search_box time_input" name="begin_time" holder="下单起始日期" value="<?php echo $this->_var['begin_time']; ?>" readonly="readonly" /></td>
						<td width="5">-</td>
						<td width="165"><input class="ui-textbox search_box time_input" name="end_time" holder="下单截止日期" value="<?php echo $this->_var['end_time']; ?>" readonly="readonly" /></td>
						<td width="50">名称</td>
						<td width="165"><input class="ui-textbox search_box" name="name" holder="团购商品名称" value="<?php echo $this->_var['name']; ?>" /></td>
						<td></td>
						<td width="100">
							<input type="hidden" name="method" value="search"/>
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
							<th width="50">&nbsp;</th>
							<th>详情</th>
							<th width="80">价格</th>
							<th width="70">数量</th>
							<th width="70">状态</th>
						</tr>
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
?>
						<tr>
							<td colspan=5 class="tl hlight">
								<div class="f_l">
								订单号：<h1><?php echo $this->_var['item']['order_sn']; ?></h1>，交易时间：<h1><?php echo $this->_var['item']['create_time']; ?></h1>
								</div>
							</td>
						</tr>
						<tr class="alt">
                            <td>
                            	<a href="<?php echo $this->_var['item']['url']; ?>" target="_blank">
                            		<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['item']['deal_icon'],
  'w' => '50',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" class="deal_icon" />
								</a>
                            </td>
							<td class="tl">
								<a href="<?php echo $this->_var['item']['url']; ?>" target="_blank" title="<?php echo $this->_var['item']['name']; ?>"><?php echo $this->_var['item']['sub_name']; ?></a>
								<?php if ($this->_var['item']['memo']): ?>
								<br />
								订单备注：<?php echo $this->_var['item']['memo']; ?>
								<?php endif; ?>
								<br />
								下单会员：<?php echo $this->_var['item']['user_name']; ?>
								<br />
								手机号：<?php echo $this->_var['item']['user_mobile']; ?>
							</td>
							<td>
								<h1>结算价：<?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['s_total_price'],
);
echo $k['name']($k['v']);
?></h1>
							</td>
							<td><?php echo $this->_var['item']['number']; ?></td>
							<td>
							
							<?php if ($this->_var['item']['order_status'] == 1): ?>
								订单已完结
								<?php if ($this->_var['item']['dp_id'] > 0): ?>
								<h1>已点评</h1>
								<?php endif; ?>
							<?php else: ?>										
								<?php if ($this->_var['item']['verify_count'] == $this->_var['item']['number']): ?>
									已消费
									<?php if ($this->_var['item']['dp_id'] > 0): ?>
									<br />
									<h1>已点评</h1>
									<?php endif; ?>
								<?php elseif ($this->_var['item']['verify_count'] == 0): ?>
									未消费
								<?php else: ?>
									已消费<h1><?php echo $this->_var['item']['verify_count']; ?></h1>位
									<?php if ($this->_var['item']['dp_id'] > 0): ?>
									<br />
									<h1>已点评</h1>
									<?php endif; ?>								
								<?php endif; ?>	
								
								
								<?php if ($this->_var['item']['refund_status_1'] > 0): ?>
								<br />
								<?php if ($this->_var['allow_refund'] == 1): ?>
									<h1><a href="javascript:void(0);" rel="<?php echo $this->_var['item']['id']; ?>" class="do_refund_coupon"><?php echo $this->_var['item']['refund_status_1']; ?>位退款审核</a></h1><br />
									<h1><a href="javascript:void(0);" rel="<?php echo $this->_var['item']['id']; ?>" class="do_refuse_coupon">拒绝退款</a></h1>
								<?php else: ?>
									<h1><?php echo $this->_var['item']['refund_status_1']; ?></h1>位退款中
								<?php endif; ?>
								<?php elseif ($this->_var['item']['refund_status_2'] > 0): ?>
								<br />
								<h1><?php echo $this->_var['item']['refund_status_2']; ?></h1>已退款	
								<?php endif; ?>
														
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
			<div class="empty_tip">没有团购订单记录</div>
			<?php endif; ?>			
		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
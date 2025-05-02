<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/dcorder.css";
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

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/time_ipt.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/time_ipt.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/search_page.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/search_page.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/dc/dc_order.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/dc/dc_order.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
var ajax_url = '<?php echo $this->_var['ajax_url']; ?>';

</script>
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
			
			<div class="sum_info">
				<div class="blank"></div>
				<form name="search_form" action="<?php
echo parse_url_tag("u:biz|dcorder|"."".""); 
?>" method="post">
					<table>
						<tr>
							<td width="62%">
								<input class="ui-textbox search_box time_input" name="begin_time" holder="下单起始日期" value="<?php echo $this->_var['begin_time']; ?>" readonly="readonly" style="display:inline-block;" />
								<div style="display:inline-block;">至</div>
								<input class="ui-textbox search_box time_input" name="end_time" holder="下单截止日期" value="<?php echo $this->_var['end_time']; ?>" readonly="readonly" style="display:inline-block;" />
							</td>
							<td width="8%">关键字</td>
							<td width="20%"><input class="ui-textbox search_box" name="sn" holder="输入订单号或手机号" value="<?php echo $this->_var['sn']; ?>" /></td>
							<td width="10%">
								<input type="hidden" name="method" value="search"/>
								<button class="ui-button add_goods_type" rel="white" type="submit">搜索</button>
							</td>
						</tr>
					</table>
					<div class="blank20"></div>
					<div class="pp_pay">
						<label class="f_l" style="margin-right:10px">订单状态：</label>
						<div class="f_l">
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="0"  <?php if ($this->_var['order_status'] == 0): ?> checked="checked" <?php endif; ?> name="order_status" />全部
							</label>
						
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="1" name="order_status" <?php if ($this->_var['order_status'] == 1): ?> checked="checked" <?php endif; ?> class="f_l" />未接单
							</label>
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="2" name="order_status"  <?php if ($this->_var['order_status'] == 2): ?> checked="checked" <?php endif; ?> class="f_l" />已接单
							</label>
							
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="3" name="order_status" <?php if ($this->_var['order_status'] == 3): ?> checked="checked" <?php endif; ?> class="f_l" />已完成
							</label>
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="4" name="order_status" <?php if ($this->_var['order_status'] == 4): ?> checked="checked" <?php endif; ?> class="f_l" />交易关闭
							</label>
						</div>
					</div>
					<div class="blank20"></div>
					<div class="pp_pay">
						<label class="f_l" style="margin-right:10px">支付方式：</label>
						<div class="f_l">
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="0" name="pay_type" <?php if ($this->_var['pay_type'] == 0): ?> checked="checked" <?php endif; ?>class="f_l" /><span class="f_l">全部</span>
							</label>
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="1" name="pay_type" <?php if ($this->_var['pay_type'] == 1): ?> checked="checked" <?php endif; ?> class="f_l" /><span class="f_l">在线支付</span>
							</label>
							<label class="ui-radiobox" rel="common_rdo">
								<input type="radio" value="2" name="pay_type" <?php if ($this->_var['pay_type'] == 2): ?> checked="checked" <?php endif; ?> class="f_l" /><span class="f_l">餐到付款</span>
							</label>
						</div>
					</div>
				</form>

				<div class="blank"></div>
			</div>
			<?php if ($this->_var['list']): ?>
			<div class="info_table">
				
						<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'item');$this->_foreach['dc_item'] = array('total' => count($_from), 'iteration' => 0);
if ($this->_foreach['dc_item']['total'] > 0):
    foreach ($_from AS $this->_var['key'] => $this->_var['item']):
        $this->_foreach['dc_item']['iteration']++;
?>
					<div class="dc_info">	
							<div class="dc_tittle">
								<div class="num"><span><?php echo $this->_var['item']['sort']; ?>号</span></div>
								<div class="dc_num">
							<span>	订单号：<?php echo $this->_var['item']['order_sn']; ?>，交易时间：<?php echo $this->_var['item']['create_time']; ?></span>
								</div>
							</div>
							
							<div class="dc_tl">
								<div class="contact_l">
									
										<span>会员id：<?php echo $this->_var['item']['user_name']; ?></span>
										<span>联系人：<?php echo $this->_var['item']['consignee']; ?></span>
										<span>电话：<?php echo $this->_var['item']['mobile']; ?></span>
										<span>地址：<?php echo $this->_var['item']['api_address']; ?><?php echo $this->_var['item']['address']; ?></span>
										<span>送达时间：
										<?php if ($this->_var['item']['order_delivery_time'] == 1): ?>
											立即送达
										<?php else: ?>
											<?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['item']['order_delivery_time'],
);
echo $k['name']($k['v']);
?>
										<?php endif; ?>
										</span>
										
										<span>支付方式：
										
										<?php if ($this->_var['item']['payment_id'] == 0): ?>
											在线支付
										<?php elseif ($this->_var['item']['payment_id'] == 1): ?>
											货到付款
										<?php endif; ?>
										</span>
										<?php if ($this->_var['item']['invoice']): ?>
										<span>发票信息：<?php echo $this->_var['item']['invoice']; ?> </span>
										<?php endif; ?>
										<?php if ($this->_var['item']['dc_comment']): ?>
										<span>备注：<?php echo $this->_var['item']['dc_comment']; ?></span>
										<?php endif; ?>
									
									
								</div>	

								<div class="contact_r">
										<?php if ($this->_var['item']['is_cancel'] == 0): ?>
											<?php if ($this->_var['item']['confirm_status'] == 0): ?>
											<input type="button" value="接单"   onclick="dc_accept(this);" data-id="<?php echo $this->_var['item']['id']; ?>"  class="jd_btn" ><br />
											<?php elseif ($this->_var['item']['confirm_status'] == 1): ?>
													<?php if ($this->_var['item']['now'] > $this->_var['item']['over_time']): ?>
													<input type="button" value="已完成"   onclick="dc_over(this);" data-id="<?php echo $this->_var['item']['id']; ?>"  class="jd_btn" ><br />
													<?php else: ?>
													<span style="padding-right:10px;">已接单</span><br />
													<?php endif; ?>
											<?php endif; ?>	
											<?php if ($this->_var['item']['confirm_status'] == 2): ?>
											消费结束
											<?php else: ?>
											<a href="javascript:void(0)" onclick="close_order(this);" data-id="<?php echo $this->_var['item']['id']; ?>" action="<?php
echo parse_url_tag("u:biz|dcorder#close_tip|"."id=".$this->_var['item']['id']."".""); 
?>" style="padding-right:10px;">关闭交易</a>
											<?php endif; ?>
										<?php else: ?>
											<span>订单已关闭</span>
											<?php if ($this->_var['item']['refuse_memo']): ?>
											<br/><?php echo $this->_var['item']['refuse_memo']; ?>
											<?php endif; ?>
										<?php endif; ?>

								</div>
							
	
							</div>
							
						<div class="table dc_tl">
							
							
							<div class="table_l">
								<table>
									<tbody>
										<tr>
											<th width="55%"><span>菜单</span></th>	
											<th width="15%">单价</th>	
											<th width="15%">数量</th>	
											<th width="15%">金额</th>	
										</tr>
										<?php $_from = $this->_var['item']['m_cart_list']['cart_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'm_item');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['m_item']):
?>
										<tr>
											<td><?php echo $this->_var['m_item']['name']; ?></td>
											<td><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['m_item']['unit_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></td>
											<td><?php echo $this->_var['m_item']['num']; ?></td>
											<td><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['m_item']['total_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></td>
										</tr>
										<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>	
										<tr>
										<td colspan=3>小计</td>	
										<td><span><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['m_cart_list']['total_data']['total_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span></td>	
										</tr>
										 
									</tbody>
								</table>
							</div>
							
							
							<div class="table_r">
								<table>
									<tbody>
										<tr>
											<th width="70%"><span>其他费用</span></th>	
											<th width="30%">金额</th>	
										</tr>
										<tr>
											<td>打包费</td>
											<td><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['package_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></td>
										</tr>
										<tr>
											<td>配送费</td>
											<td><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['delivery_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></td>
										</tr>
										<?php if ($this->_var['item']['order_promote']): ?>
										<?php $_from = $this->_var['item']['order_promote']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'promote');if (count($_from)):
    foreach ($_from AS $this->_var['promote']):
?>
										<tr>
											<td><?php echo $this->_var['promote']['name']; ?></td>
											<td>-<?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['promote']['discount_amount'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></td>
										</tr>
										<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
										<?php endif; ?>
										<?php if ($this->_var['item']['ecv_money'] != 0): ?>
										<tr>
											<td>代金券</td>
											<td>-<?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['ecv_money'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></td>
										</tr>
										<?php endif; ?>
									</tbody>
								</table>
							</div>
							<div class="blank10"></div>
							<div class="tr total_box">总计：<span class="f_red"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['item']['pay_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span></div>
							
						</div>	
							
							
					</div>
                        <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			<?php else: ?>
			<div class="empty_tip">没有外卖订单记录</div>
			<?php endif; ?>
			</div>
			
			<div class="blank"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>			
			
		

		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
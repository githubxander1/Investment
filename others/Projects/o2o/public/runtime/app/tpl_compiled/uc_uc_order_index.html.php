<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_order.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_order.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_order.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>
<?php echo $this->fetch('inc/refuse_delivery_form.html'); ?>
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
		
		<div class="main_box setting_user_info">
			<div class="content">
				<div class="title"><span>我的订单</span></div>
				<div class="blank20"></div>
				
			</div>
			
			<?php if ($this->_var['list']): ?>
			<div class="info_box">
				<div class="info_table order_table">
					<table>
						<tbody>
							<tr>
								<th width="50">&nbsp;</th>
								<th width="auto">详情</th>
								<th width="50">价格</th>
								<th width="70">数量</th>
								<th width="70">状态</th>
								<th width="70">操作</th>
							</tr>
				
							<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'order');if (count($_from)):
    foreach ($_from AS $this->_var['order']):
?>
							<tr>
								<td colspan=6 class="tl order_sum">
									<div class="f_l">
									订单号：<h1><?php echo $this->_var['order']['order_sn']; ?></h1>，交易时间：<h1><?php echo $this->_var['order']['create_time']; ?></h1>，应付总额：<h1><?php echo $this->_var['order']['total_price']; ?></h1>，实付金额：<h1><?php echo $this->_var['order']['pay_amount']; ?></h1>
									</div>
									<div class="f_r">
										<?php if ($this->_var['order']['pay_status'] != 2): ?>
										<a href="<?php
echo parse_url_tag("u:index|cart#order|"."id=".$this->_var['order']['id']."".""); 
?>" class="continue_pay">继续付款</a>
										<?php endif; ?>
									</div>
								</td>
							</tr>
								<?php $_from = $this->_var['order']['deal_order_item']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal');$this->_foreach['deal_loop'] = array('total' => count($_from), 'iteration' => 0);
if ($this->_foreach['deal_loop']['total'] > 0):
    foreach ($_from AS $this->_var['deal']):
        $this->_foreach['deal_loop']['iteration']++;
?>
								<tr class="alt">
									<td>
										<a href="<?php echo $this->_var['deal']['url']; ?>" target="_blank"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['deal']['deal_icon'],
  'w' => '50',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" class="deal_icon" /></a>
									</td>
	                                <td class="tl">
	                                	<a href="<?php echo $this->_var['deal']['url']; ?>" target="_blank"><?php echo $this->_var['deal']['name']; ?></a>
									</td>
	                                <td>
	                                	<?php echo $this->_var['deal']['total_price']; ?>
									</td>
	                                <td><?php echo $this->_var['deal']['number']; ?></td>
									<td>
										<?php if ($this->_var['order']['pay_status'] != 2): ?>
											--
										<?php elseif ($this->_var['order']['order_status'] == 1): ?>
											订单已完结
											<?php if ($this->_var['deal']['dp_id'] == 0 && $this->_var['deal']['consume_count'] > 0): ?>
											<a href="<?php
echo parse_url_tag("u:index|review|"."order_item_id=".$this->_var['deal']['id']."".""); 
?>" target="_blank">我要点评</a>
											<?php elseif ($this->_var['deal']['dp_id'] > 0): ?>
											<h1>已点评</h1>
											<?php endif; ?>
										<?php else: ?>										
											<?php if ($this->_var['deal']['delivery_status'] == 5): ?>										
												<?php if ($this->_var['deal']['is_coupon'] == 1): ?>
												<a href="<?php
echo parse_url_tag("u:index|uc_coupon|"."did=".$this->_var['deal']['id']."".""); 
?>">查看团购券</a>
												<?php else: ?>
												--
												<?php endif; ?>
											<?php else: ?>
												<?php if ($this->_var['deal']['delivery_status'] == 0): ?>
												未发货
												<?php elseif ($this->_var['deal']['delivery_status'] == 1): ?>
													<h1>已发货</h1>
													<br />
													<a  <?php if (app_conf ( "KUAIDI_TYPE" ) != 2): ?>ajax="true" kuaidi_type="<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'KUAIDI_TYPE',
);
echo $k['name']($k['v']);
?>" href="javascript:void(0);" action="<?php
echo parse_url_tag("u:index|uc_order#check_delivery|"."id=".$this->_var['deal']['id']."".""); 
?>"<?php else: ?>href="<?php
echo parse_url_tag("u:index|uc_order#check_delivery|"."id=".$this->_var['deal']['id']."".""); 
?>" target="_blank"<?php endif; ?> rel="<?php echo $this->_var['deal']['id']; ?>" class="check_delivery">查看物流</a>
													<br />
													<?php if ($this->_var['deal']['is_arrival'] == 0): ?>
														<?php if ($this->_var['deal']['refund_status'] != 2): ?>
														<a href="javascript:void(0);" action="<?php
echo parse_url_tag("u:index|uc_order#verify_delivery|"."id=".$this->_var['deal']['id']."".""); 
?>" class="verify_delivery">确认收货</a>
														<br />
														<a href="javascript:void(0);" action="<?php
echo parse_url_tag("u:index|uc_order#refuse_delivery|"."id=".$this->_var['deal']['id']."".""); 
?>" class="refuse_delivery">没收到货</a>
														<?php endif; ?>
													<?php elseif ($this->_var['deal']['is_arrival'] == 2): ?>
													<h1>维权中</h1>
													<?php else: ?>
													<h1>已收货</h1>
													
													<?php if ($this->_var['deal']['dp_id'] == 0): ?>
													<br />
													<a href="<?php
echo parse_url_tag("u:index|review|"."order_item_id=".$this->_var['deal']['id']."".""); 
?>" target="_blank">我要点评</a>
													<?php elseif ($this->_var['deal']['dp_id'] > 0): ?>
													<br />
													<h1>已点评</h1>
													<?php endif; ?>
													
													<?php endif; ?>
												<?php endif; ?>
											<?php endif; ?>											
										<?php endif; ?>
										<?php if ($this->_var['deal']['refund_status'] > 0): ?>
										<br />
											<?php if ($this->_var['deal']['refund_status'] == 1): ?>
											<h1>退款中</h1>
											<?php elseif ($this->_var['deal']['refund_status'] == 2): ?>
											<h1>已退款</h1>
											<?php else: ?>
											<h1>拒绝退款</h1>
											<?php endif; ?>
										<?php endif; ?>
										
									</td>
									<?php if (($this->_foreach['deal_loop']['iteration'] <= 1)): ?>
									<td rowspan="<?php echo $this->_var['order']['c']; ?>" class="op_box">										
										<a href="<?php
echo parse_url_tag("u:index|uc_order#view|"."id=".$this->_var['order']['id']."".""); 
?>">查看</a>											
										<?php if ($this->_var['order']['order_status'] == 1): ?>
										<br />
										<a href="javascript:void(0);" action="<?php
echo parse_url_tag("u:index|uc_order#cancel|"."id=".$this->_var['order']['id']."".""); 
?>" class="del_order">删除订单</a>
										<?php elseif ($this->_var['order']['pay_status'] == 0): ?>
										<br />
										<a href="javascript:void(0);" action="<?php
echo parse_url_tag("u:index|uc_order#cancel|"."id=".$this->_var['order']['id']."".""); 
?>" class="del_order">取消订单</a>
										<?php endif; ?>										
									</td>
									<?php endif; ?>
	                            </tr>
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                   
   
						</tbody>
					</table>
				</div>
				
			</div>

			<div class="blank20"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>
			<?php else: ?>
			<div class="empty_tip">没有订单记录</div>
			<?php endif; ?>
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
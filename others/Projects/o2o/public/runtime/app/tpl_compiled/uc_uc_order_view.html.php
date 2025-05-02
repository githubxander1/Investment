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
			
			<div class="info_box">
				<div class="info_table order_table">
					<table>
								<tr>
									<td colspan=4 class="tl order_sum">
										<div class="f_l">
										订单号：<h1><?php echo $this->_var['order_info']['order_sn']; ?></h1>，交易时间：<h1><?php echo $this->_var['order_info']['create_time']; ?></h1>
										</div>
										<div class="f_r">
											<?php if ($this->_var['order_info']['pay_status'] != 2): ?>
											<a href="<?php
echo parse_url_tag("u:index|cart#order|"."id=".$this->_var['order_info']['id']."".""); 
?>" class="continue_pay">继续付款</a>
											<?php endif; ?>
										</div>
									</td>
								</tr>
								<tr>
									<td class="ltd">付款信息 </td>
									<td  class="rtd" colspan=3>
										应付总额：<h1><?php echo $this->_var['order_info']['total_price_format']; ?></h1>，实付金额：<h1><?php echo $this->_var['order_info']['pay_amount_format']; ?></h1>
										<?php if ($this->_var['order_info']['delivery_fee'] > 0): ?>
										，运费：<h1><?php echo $this->_var['order_info']['delivery_fee_format']; ?></h1>
										<?php endif; ?>
										
									</td>
								</tr>
								<?php if ($this->_var['order_info']['delivery_id'] != 0): ?>
								<tr>
									<td colspan=4 class="tl order_sum">
										配送信息
									</td>
								</tr>
								<tr>
									<td class="ltd">收货人信息</td>
									<td class="rtd" colspan=3>姓名：<?php echo $this->_var['order_info']['consignee']; ?> &nbsp;&nbsp;手机：<?php echo $this->_var['order_info']['mobile']; ?></td>
								</tr>	
								<tr>
									<td class="ltd">地区信息：</td>
									<td  class="rtd" colspan="3">
									<?php echo $this->_var['LANG']['REGION_LV1']; ?>：<?php echo $this->_var['order_info']['region_lv1']['name']; ?>&nbsp;&nbsp;		
									<?php echo $this->_var['LANG']['REGION_LV2']; ?>：<?php echo $this->_var['order_info']['region_lv2']['name']; ?>&nbsp;&nbsp;	
									<?php echo $this->_var['LANG']['REGION_LV3']; ?>：<?php echo $this->_var['order_info']['region_lv3']['name']; ?>&nbsp;&nbsp;	
									<?php echo $this->_var['LANG']['REGION_LV4']; ?>：<?php echo $this->_var['order_info']['region_lv4']['name']; ?>&nbsp;&nbsp;	
									&nbsp;&nbsp;&nbsp;&nbsp;
									邮编：<?php echo $this->_var['order_info']['zip']; ?>
									</td>
								</tr>
								<tr>
									<td class="ltd"><?php echo $this->_var['LANG']['ADDRESS']; ?>：</td>
									<td class="rtd" colspan="3">
									<?php echo $this->_var['order_info']['address']; ?>								
									</td>
								</tr>
								<?php endif; ?>
								

																
								<tr>
									<td class="ltd">
									<?php echo $this->_var['LANG']['ORDER_MEMO']; ?>：									
									</td>									
									<td class="rtd" colspan="3">
									<?php echo $this->_var['order_info']['memo']; ?>
									</td>
								</tr>
								<!--<tr>
									<td class="ltd">
									<?php echo $this->_var['LANG']['AFTER_SALE']; ?>：									
									</td>									
									<td class="rtd" colspan="3">
									<?PHP echo $this->_var['LANG']['AFTER_SALE_'.$this->_var['order_info']['after_sale']];?>
									</td>
								</tr>-->
								<?php if ($this->_var['order_info']['admin_memo']): ?>
								<tr>
									<td  class="ltd">
									<?php echo $this->_var['LANG']['ADMIN_MEMO']; ?>：									
									</td>									
									<td  class="rtd" colspan="3">
									<?php echo $this->_var['order_info']['admin_memo']; ?>
									</td>
								</tr>
								<?php endif; ?>
								<tr>
									<td class="rtd" colspan="4">
										<table>
											<tr>
												<th width="50">&nbsp;</th>
												<th width="auto">详情</th>
												<th width="50">价格</th>
												<th width="70">数量</th>
												<th width="70">状态</th>
												<th width="40">操作</th>
											</tr>
											<?php $_from = $this->_var['order_info']['deal_order_item']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal');$this->_foreach['deal_loop'] = array('total' => count($_from), 'iteration' => 0);
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
													<?php if ($this->_var['order_info']['pay_status'] != 2): ?>
														--
													<?php elseif ($this->_var['order_info']['order_status'] == 1): ?>
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
?>"  href="javascript:void(0);" action="<?php
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
											
												<td class="op_box">									
													<?php if ($this->_var['deal']['delivery_status'] == 0 && $this->_var['order_info']['pay_status'] == 2 && $this->_var['deal']['is_refund'] == 1): ?>
														<?php if ($this->_var['deal']['refund_status'] == 0): ?>
														<a href="javascript:void(0);" class="refund" action="<?php
echo parse_url_tag("u:index|uc_order#refund|"."did=".$this->_var['deal']['id']."".""); 
?>">退款</a>
														<?php elseif ($this->_var['deal']['refund_status'] == 1): ?>
														<h1>退款中</h1>
														<?php elseif ($this->_var['deal']['refund_status'] == 3): ?>
														<h1>退款被拒</h1>
														<?php else: ?>
														--
														<?php endif; ?>
													<?php else: ?>
													--
													<?php endif; ?>		
																	
												</td>
												
				                            </tr>
											<?php if ($this->_var['deal']['is_coupon'] == 1 && $this->_var['deal']['coupon']): ?>
											<tr>
												<td colspan=6>
												<table>
													<tr>
														<th width="100">序列号</th>
														<th width="auto">详情</th>
														<th width="150">有效期</th>
														<th width="120">状态</th>
														<th width="60">操作</th>
													</tr>
													<?php $_from = $this->_var['deal']['coupon']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'coupon');if (count($_from)):
    foreach ($_from AS $this->_var['coupon']):
?>
													<tr>
														<td><?php echo $this->_var['coupon']['password']; ?></td>
														<td>
															<a href="<?php echo $this->_var['deal']['url']; ?>" target="_blank"><?php echo $this->_var['deal']['sub_name']; ?></a>
															&nbsp;&nbsp;<?php if ($this->_var['coupon']['deal_type'] == 1): ?>【可消费 <h1><?php echo $this->_var['deal']['number']; ?></h1> 位】<?php endif; ?>
															
														</td>
														<td>
															<?php if ($this->_var['coupon']['begin_time']): ?><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['coupon']['begin_time'],
  'f' => 'Y-m-d',
);
echo $k['name']($k['v'],$k['f']);
?> 至<?php endif; ?>
															<?php if ($this->_var['coupon']['end_time']): ?><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['coupon']['end_time'],
  'f' => 'Y-m-d',
);
echo $k['name']($k['v'],$k['f']);
?><?php endif; ?>
															<?php if ($this->_var['coupon']['begin_time'] == 0 && $this->_var['coupon']['end_time'] == 0): ?>无限期<?php endif; ?>
														</td>
														<td>
															<?php if ($this->_var['coupon']['confirm_time'] == 0): ?>
																<?php if ($this->_var['coupon']['refund_status'] == 1): ?>
																	<h1>退款中</h1>
																<?php elseif ($this->_var['coupon']['refund_status'] == 2): ?>
																	<h1>已退款</h1>
																<?php elseif ($this->_var['coupon']['refund_status'] == 3): ?>
																	<h1>退款被拒</h1>
																<?php else: ?>
																	<?php if ($this->_var['coupon']['is_valid'] == 1): ?>
																		<?php if ($this->_var['coupon']['end_time'] > 0 && $this->_var['coupon']['end_time'] < $this->_var['NOW_TIME']): ?>
																		<h1>已过期</h1>
																		<?php else: ?>
																		有效
																		<?php endif; ?>
																	<?php else: ?>
																		<h1>作废</h1>
																	<?php endif; ?>
																<?php endif; ?>
															<?php else: ?>
																<h1><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['coupon']['confirm_time'],
  'f' => 'Y-m-d',
);
echo $k['name']($k['v'],$k['f']);
?></h1> 消费
															<?php endif; ?>
															
														</td>
														<td>
															<?php if ($this->_var['coupon']['refund_status'] == 0 && $this->_var['coupon']['confirm_time'] == 0): ?>
																<?php if ($this->_var['coupon']['any_refund'] == 1 || ( $this->_var['coupon']['expire_refund'] == 1 && $this->_var['coupon']['end_time'] > 0 && $this->_var['coupon']['end_time'] < $this->_var['NOW_TIME'] )): ?>
																<a href="javascript:void(0);" class="refund" action="<?php
echo parse_url_tag("u:index|uc_order#refund|"."cid=".$this->_var['coupon']['id']."".""); 
?>">退款</a>
																<?php else: ?>
																--
																<?php endif; ?>
															<?php else: ?>
															--
															<?php endif; ?>
															
															<?php if ($this->_var['coupon']['refund_status'] != 1 && $this->_var['coupon']['refund_status'] != 2 && $this->_var['coupon']['confirm_time'] == 0 && ( $this->_var['coupon']['end_time'] > $this->_var['NOW_TIME'] || $this->_var['coupon']['end_time'] = 0 )): ?> 
															<?php if ($this->_var['deal']['forbid_sms'] == 0 && app_conf ( "SMS_ON" ) == 1 && app_conf ( "SMS_SEND_COUPON" ) == 1 && $this->_var['coupon']['sms_count'] < app_conf ( "SMS_COUPON_LIMIT" )): ?>
															<br />
															<a href="javascript:void(0);" class="send_coupon" action="<?php
echo parse_url_tag("u:index|uc_coupon#send|"."t=sms&id=".$this->_var['coupon']['id']."".""); 
?>">短信发送</a>
															<?php endif; ?>
															
															<?php if (app_conf ( "MAIL_ON" ) == 1 && app_conf ( "MAIL_SEND_COUPON" ) == 1 && $this->_var['coupon']['mail_count'] < app_conf ( "MAIL_COUPON_LIMIT" )): ?>
															<br />
															<a href="javascript:void(0);" class="send_coupon" action="<?php
echo parse_url_tag("u:index|uc_coupon#send|"."t=mail&id=".$this->_var['coupon']['id']."".""); 
?>">邮件发送</a>
															<?php endif; ?>
															<?php endif; ?>
														</td>
													</tr>
													<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
												</table>
												</td>
											</tr>
											<?php endif; ?>
											<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
										</table>
									</td>
								</tr>
								<tr>
									<td class="rtd" colspan="4">
									
									<div id="cart_total_box">
									<div class="order-check-form ">
										<p style="text-align: right; line-height: 24px;">
										<?php echo $this->_var['LANG']['DEAL_TOTAL_PRICE']; ?>：<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['deal_total_price'],
);
echo $k['name']($k['value']);
?> 
										<?php if ($this->_var['order_info']['delivery_fee'] > 0): ?>
										+ <?php echo $this->_var['LANG']['DELIVERY_FEE']; ?>：<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['delivery_fee'],
);
echo $k['name']($k['value']);
?>
										<?php endif; ?>
										<?php if ($this->_var['order_info']['payment_fee'] > 0): ?>
										+ <?php echo $this->_var['LANG']['PAYMENT_FEE']; ?>：<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['payment_fee'],
);
echo $k['name']($k['value']);
?> 
										<?php endif; ?>
										<?php if ($this->_var['order_info']['discount_price'] > 0): ?>
										- <?php echo $this->_var['LANG']['USER_DISCOUNT']; ?>：<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['discount_price'],
);
echo $k['name']($k['value']);
?>
										<?php endif; ?>
										=
										<span class="red"><?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['total_price'],
);
echo $k['name']($k['value']);
?></span>
										</p>
										<p style="text-align: right; line-height: 24px;">
										
										<?php if ($this->_var['order_info']['account_money'] > 0): ?>
										- <?php echo $this->_var['LANG']['ACCOUNT_PAY']; ?>：<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['account_money'],
);
echo $k['name']($k['value']);
?> <br>
										<?php endif; ?>
										
										<?php if ($this->_var['order_info']['ecv_money'] > 0): ?>
										- <?php echo $this->_var['LANG']['ECV_PAY']; ?>：<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['ecv_money'],
);
echo $k['name']($k['value']);
?> <br>
										<?php endif; ?>
										
										= <?php echo $this->_var['LANG']['PAY_TOTAL_PRICE_ORDER']; ?>：<?php if ($this->_var['order_info']['payment_id'] > 0): ?><?php 
$k = array (
  'name' => 'sprintf',
  'value' => $this->_var['LANG']['PAYMENT_BY'],
  'p' => $this->_var['order_info']['payment']['name'],
);
echo $k['name']($k['value'],$k['p']);
?><?php endif; ?>
										<span class="red">
											<?PHP echo format_price($this->_var['order_info']['total_price']-$this->_var['order_info']['account_money']-$this->_var['order_info']['ecv_money']);?>
										</span>&nbsp;
										<br>
										</p>
										<div class="blank"></div>
										<p style="text-align: right; line-height: 24px;">
										<?php if ($this->_var['order_info']['return_total_money'] != 0): ?>
										<?php echo $this->_var['LANG']['RETURN_TOTAL_MONEY']; ?>： <?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['order_info']['return_total_money'],
);
echo $k['name']($k['value']);
?> <br>
										<?php endif; ?>
									
										<?php if ($this->_var['order_info']['return_total_score'] != 0): ?>
										<?php if ($this->_var['deal']['buy_type'] == 1): ?>
										消耗积分：  <?php echo format_score(abs($this->_var['order_info']['return_total_score']));?>
										<?php else: ?>
										<?php echo $this->_var['LANG']['RETURN_TOTAL_SCORE']; ?>：  <?php 
$k = array (
  'name' => 'format_score',
  'value' => $this->_var['order_info']['return_total_score'],
);
echo $k['name']($k['value']);
?>										
										<?php endif; ?>			
										<?php endif; ?>
										</p>
										<div class="blank"></div>
										<?php if ($this->_var['order_info']['promote_description']): ?>
										<div class="promote_title">参与的促销活动</div>
										<div class="tr" style="line-height:22px;">
										<?php echo $this->_var['order_info']['promote_description']; ?>
										</div>
										<div class="blank"></div>
										<?php endif; ?>
										</div>
									</div>
									
									</td>
							</tr>
							<tr>
								<tr>
									<td colspan=4 class="tl order_sum">
										付款记录
									</td>
								</tr>
								<tr>
									<td colspan="4">
										<table>
											<tr>												
												<th width="80">支付金额</th>
												<th width="200">付款单号</th>
												<th width="auto">支付平台</th>
												<th width="150">支付状态</th>
											</tr>
											<?php $_from = $this->_var['payment_notice_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'notice');if (count($_from)):
    foreach ($_from AS $this->_var['notice']):
?>
											<tr>
												<td><h1><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['notice']['money'],
);
echo $k['name']($k['v']);
?></h1></td>
												<td><?php echo $this->_var['notice']['notice_sn']; ?></td>
												<td>
													<?php echo $this->_var['notice']['payment']['name']; ?>
													<?php if ($this->_var['notice']['outer_notice_sn']): ?>
													<br />
													<h1><?php echo $this->_var['notice']['outer_notice_sn']; ?></h1>
													<?php endif; ?>
												</td>
												<td>
													<?php if ($this->_var['notice']['is_paid'] == 1): ?>
													<?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['notice']['pay_time'],
);
echo $k['name']($k['v']);
?>支付
													<?php else: ?>
													未支付
													<?php endif; ?>
												</td>
											</tr>
											<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
											
										</table>
									</td>
								</tr>
							</tr>
							<?php if ($this->_var['order_logs']): ?>
							<tr>
								<tr>
									<td colspan=4 class="tl order_sum">
										订单日志
									</td>
								</tr>
								<tr>
									<td colspan="4">
										<table>
											<tr>	
												<th width="auto">内容</th>
												<th width="150">发生时间</th>
											</tr>
											<?php $_from = $this->_var['order_logs']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'log');if (count($_from)):
    foreach ($_from AS $this->_var['log']):
?>
											<tr>
												<td><?php echo $this->_var['log']['log_info']; ?></td>												
												<td><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['log']['log_time'],
);
echo $k['name']($k['v']);
?></td>
											</tr>
											<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
											
										</table>
									</td>
								</tr>
							</tr>
							<?php endif; ?>
					</table>
				</div>
			</div>
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
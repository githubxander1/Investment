<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_money_incharge.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_money_incharge.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_money_incharge.js";

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
					<li class="cur"><a href="<?php
echo parse_url_tag("u:index|uc_money#incharge|"."".""); 
?>">会员充值</a></li>
					<li><a href="<?php
echo parse_url_tag("u:index|uc_money#withdraw|"."".""); 
?>">会员提现</a></li>
				</ul>
			</div>

			<!-- 资产标题 -->
			<div class="info_box">
				<div class="blank20"></div>
				<h3>我的资产信息</h3>
				<div class="blank10"></div>
				<div class="bg_box growth_content">
					
					<div class="info_items">
						<ul>
							<li><label>我当前的余额是：</label><span class="main_color"><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['user_info']['money'],
);
echo $k['name']($k['v']);
?></span>
							<label>&nbsp;&nbsp;&nbsp;&nbsp;会员等级：</label><span class="level_bg level_<?php echo $this->_var['uc_query_data']['cur_level']; ?>" title="<?php echo $this->_var['uc_query_data']['cur_level_name']; ?>"></span>
							</li>
							<?php if ($this->_var['uc_query_data']['cur_gourp'] > 0): ?>
								<li><label>我当前所在的会员组：</label><span class="main_color"><?php echo $this->_var['uc_query_data']['cur_gourp_name']; ?></span></li>
								<?php if ($this->_var['uc_query']['data']['cur_discount'] < 10): ?>
								<li><label>会员组享受的折扣：</label><span class="main_color"><?php echo $this->_var['uc_query_data']['cur_discount']; ?> 折</span></li>
								<?php endif; ?>
							<?php endif; ?>
						</ul>
					</div>
				</div>
			</div>
			
			
			<div id="cart_payment">
		
					<form name="incharge_form" action="<?php
echo parse_url_tag("u:index|uc_money#incharge_done|"."".""); 
?>" method="post" />	
					<div class="info_table">
					<table>
						<tr>
							<td colspan=2 class="payment_list_td">
								<?php if ($this->_var['bank_paylist']): ?>
								<?php $_from = $this->_var['bank_paylist']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'payment_item');if (count($_from)):
    foreach ($_from AS $this->_var['payment_item']):
?>	
									<?php echo $this->_var['payment_item']['display_code']; ?>											
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>	
								<?php endif; ?>
								<?php if ($this->_var['bank_paylist'] && $this->_var['icon_paylist']): ?><div class="blank"></div><?php endif; ?>
								<?php if ($this->_var['icon_paylist']): ?>
								<?php $_from = $this->_var['icon_paylist']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'payment_item');if (count($_from)):
    foreach ($_from AS $this->_var['payment_item']):
?>	
									<?php echo $this->_var['payment_item']['display_code']; ?>											
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
								<?php endif; ?>
								
							</td>
						</tr>
						<tr>
							<td class="payment_input"><input type="text" class="ui-textbox" name="money" holder="请输入充值金额" /></td>
							<td class="payment_btn"><button class="ui-button orange" rel="orange" type="submit">立即支付</button></td>
						</tr>
					</table>
					</div>
					</form>
					
	
			</div>
			
			<!-- 资产内容 -->
			<div class="blank20"></div>
			<div class="info_box">
				<h3>充值记录</h3>
				<div class="blank10"></div>
				<div class="info_table order_table">
					<table>
						<tbody>
							<tr>
								<th width="120">时间</th>
								<th width="auto">详情</th>
								<th width="100">手续费</th>
								<th width="70">操作</th>
							</tr>
							
							<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
							<tr class="alt">
                                <td>
								<?php 
$k = array (
  'name' => 'to_date',
  'value' => $this->_var['row']['create_time'],
);
echo $k['name']($k['value']);
?>
								</td>
                                <td class="tl">
                                	充值订单号：<h1><?php echo $this->_var['row']['order_sn']; ?></h1><br />
									支付单号：<h1><?php echo $this->_var['row']['payment_notice']['notice_sn']; ?></h1>，支付方式：<h1><?php echo $this->_var['row']['payment']['name']; ?></h1><br />
									<?php if ($this->_var['row']['payment_notice']['outer_notice_sn']): ?>
									支付平台单号：<h1><?php echo $this->_var['row']['payment_notice']['outer_notice_sn']; ?></h1><br />
									<?php endif; ?>
									充值金额：<h1><?PHP echo format_price($this->_var['row']['total_price']-$this->_var['row']['payment_fee']);?></h1>
									<?php if ($this->_var['row']['pay_status'] == 2): ?>
									&nbsp;&nbsp;充值到账时间：<h1><?php 
$k = array (
  'name' => 'to_date',
  'value' => $this->_var['row']['payment_notice']['pay_time'],
);
echo $k['name']($k['value']);
?></h1>
									<?php endif; ?>
                                </td>
                                <td><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['row']['payment_fee'],
);
echo $k['name']($k['v']);
?></td>
								<td class="op_box">
									<?php if ($this->_var['row']['pay_status'] == 0): ?>									
									<a href="<?php
echo parse_url_tag("u:index|payment#pay|"."id=".$this->_var['row']['payment_notice']['id']."".""); 
?>">继续付款</a><br />
									<a href="javascript:void(0);" class="del_order" action="<?php
echo parse_url_tag("u:index|uc_order#cancel|"."id=".$this->_var['row']['id']."".""); 
?>">删除</a>
									<?php endif; ?>
									<?php if ($this->_var['row']['order_status'] == 1): ?>
									<?php if ($this->_var['row']['pay_status'] == 2): ?><br /><?php endif; ?>
									<a href="javascript:void(0);" class="del_order" action="<?php
echo parse_url_tag("u:index|uc_order#cancel|"."id=".$this->_var['row']['id']."".""); 
?>">删除</a>
									<?php endif; ?>
								</td>
                            </tr>
                            <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                           
                            <tr >
                            	<?php if ($this->_var['list']): ?>
                                <td colspan="4"><div class="pages"><?php echo $this->_var['pages']; ?></div></td>
                                <?php else: ?>
                                <td colspan="4"><span>暂时没有充值记录</span></td>
                                <?php endif; ?>
                            </tr>
						</tbody>
					</table>
				</div>
				
			</div>	
			
			
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
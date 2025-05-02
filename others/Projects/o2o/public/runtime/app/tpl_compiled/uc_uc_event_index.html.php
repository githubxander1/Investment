<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_order.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/event.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_event.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_event.js";
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
		
		<div class="main_box setting_user_info">
			<div class="content">
				<div class="title"><span>我的活动报名</span></div>
				<div class="blank20"></div>
				
			</div>
			<?php if ($this->_var['list']): ?>
			<div class="info_box">
				<div class="info_table order_table">
					<table>
						<tbody>							
							<tr>
								<th width="100">序列号</th>
								<th width="auto">详情</th>
								<th width="150">有效期</th>
								<th width="120">状态</th>
								<th width="60">操作</th>
							</tr>
				
							<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'event');if (count($_from)):
    foreach ($_from AS $this->_var['event']):
?>
							<tr>
								<td>
									<?php if ($this->_var['event']['is_verify'] == 1): ?>
									<?php echo $this->_var['event']['sn']; ?>
									<br />
									<a href="javascript:void(0);" event_id="<?php echo $this->_var['event']['event_id']; ?>" class="view_submit" action="<?php
echo parse_url_tag("u:index|uc_event#view_submit|"."id=".$this->_var['event']['id']."".""); 
?>">查看报名资料</a>
									<?php elseif ($this->_var['event']['is_verify'] == 0): ?>
									<h1>未审核</h1>
									<br />
									<a  href="javascript:void(0);" event_id="<?php echo $this->_var['event']['event_id']; ?>" class="modify_submit">修改报名资料</a>
									<?php else: ?>
									<h1>审核不通过</h1>
									<?php endif; ?>	
								</td>
								<td>
									<a href="<?php echo $this->_var['event']['event']['url']; ?>" target="_blank"><?php echo $this->_var['event']['event']['name']; ?></a>		
									<?php if ($this->_var['event']['return_money'] > 0 || $this->_var['event']['return_score'] > 0 || $this->_var['event']['return_point'] > 0): ?>
									<br />
									使用后返还
									<?php if ($this->_var['event']['return_money'] > 0): ?><h1><?php 
$k = array (
  'name' => 'format_price',
  'v' => $this->_var['event']['return_money'],
);
echo $k['name']($k['v']);
?></h1>&nbsp;&nbsp;<?php endif; ?>
									<?php if ($this->_var['event']['return_score'] > 0): ?><h1>+ <?php 
$k = array (
  'name' => 'format_score',
  'v' => $this->_var['event']['return_score'],
);
echo $k['name']($k['v']);
?></h1>&nbsp;&nbsp;<?php endif; ?>
									<?php if ($this->_var['event']['return_point'] > 0): ?><h1>+ <?php echo $this->_var['event']['return_point']; ?>经验值</h1><?php endif; ?>
									<?php endif; ?>							
								</td>
								<td>
									<?php if ($this->_var['event']['event_end_time']): ?><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['event']['event_end_time'],
  'f' => 'Y-m-d',
);
echo $k['name']($k['v'],$k['f']);
?><?php endif; ?>
									<?php if ($this->_var['event']['event_end_time'] == 0): ?>无限期<?php endif; ?>
								</td>
								<td>
									<?php if ($this->_var['event']['confirm_time'] == 0): ?>
										<?php if ($this->_var['event']['event_end_time'] > 0 && $this->_var['event']['event_end_time'] < $this->_var['NOW_TIME']): ?>
										<h1>已过期</h1>
										<?php else: ?>
											<?php if ($this->_var['event']['is_verify'] == 1): ?>
											有效
											<?php else: ?>
											--
											<?php endif; ?>
										<?php endif; ?>
									<?php else: ?>
										<h1><?php 
$k = array (
  'name' => 'to_date',
  'v' => $this->_var['event']['confirm_time'],
  'f' => 'Y-m-d',
);
echo $k['name']($k['v'],$k['f']);
?></h1> 使用
									<?php endif; ?>
									
								</td>
								<td>
									
									<?php if ($this->_var['event']['is_verify'] == 0 || $this->_var['event']['is_verify'] == 2): ?>
									--
									<?php elseif ($this->_var['event']['confirm_time'] == 0 && ( $this->_var['event']['event_end_time'] > $this->_var['NOW_TIME'] || $this->_var['event']['event_end_time'] == 0 )): ?> 						
										<?php if (app_conf ( "SMS_ON" ) == 1 && $this->_var['event']['sms_count'] < app_conf ( "SMS_COUPON_LIMIT" )): ?>
										<a href="javascript:void(0);" class="send_event" action="<?php
echo parse_url_tag("u:index|uc_event#send|"."t=sms&id=".$this->_var['event']['id']."".""); 
?>">短信发送</a>
										<?php endif; ?>		
										<?php if (app_conf ( "SMS_ON" ) == 1 && $this->_var['event']['mail_count'] < app_conf ( "MAIL_COUPON_LIMIT" )): ?>
										<?php if (app_conf ( "SMS_ON" ) == 1 && $this->_var['event']['sms_count'] < app_conf ( "SMS_COUPON_LIMIT" )): ?>
										<br />
										<?php endif; ?>
										<a href="javascript:void(0);" class="send_event" action="<?php
echo parse_url_tag("u:index|uc_event#send|"."t=mail&id=".$this->_var['event']['id']."".""); 
?>">邮件发送</a>
										<?php endif; ?>								
									<?php else: ?>
										<?php if ($this->_var['event']['dp_id'] == 0): ?>
										<a href="<?php
echo parse_url_tag("u:index|review|"."event_submit_id=".$this->_var['event']['id']."".""); 
?>" target="_blank">我要点评</a>
										<?php else: ?>
										<h1>已点评</h1>
										<?php endif; ?>
									<?php endif; ?>
	
								</td>
							</tr>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                   
   
						</tbody>
					</table>
				</div>
				
			</div>

			<div class="blank20"></div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>
			<?php else: ?>
			<div class="empty_tip">没有报名记录</div>
			<?php endif; ?>
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
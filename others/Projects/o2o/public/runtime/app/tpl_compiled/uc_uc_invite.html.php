<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc_invite.css";
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

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_invite.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_invite.js";
?>
<?php echo $this->fetch('inc/header.html'); ?>
<script>
var MEDAL_BOX_URL = '<?php
echo parse_url_tag("u:index|uc_medal#load_medal|"."".""); 
?>';
</script>
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
				<div class="title"><span>我的邀请</span></div>
				<div class="blank20"></div>
				
				<div class="money_box">
						<?php echo $this->_var['LANG']['TOTAL_REFERRALS']; ?>：
						<strong><?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['total_referral_money'],
);
echo $k['name']($k['value']);
?></strong>
						<strong><?php 
$k = array (
  'name' => 'format_score',
  'value' => $this->_var['total_referral_score'],
);
echo $k['name']($k['value']);
?></strong>
				</div>	
				<div class="blank20"></div>		

				<div class="info_table">
				
					<div id="referrals">
								<div class="blk im refers">
									
										<h4><?php echo $this->_var['LANG']['SHARE_LINK']; ?>：</h4>
										<input type="text" onfocus="this.select()" class="ui-textbox" id="share-copy-text" size="40" value="<?php echo $this->_var['share_url']; ?>">
										<input type="button" class="formbutton" id="share-copy-button" value="<?php echo $this->_var['LANG']['COPY']; ?>">
								
								</div>
					</div>
					<div class="blank20"></div>				
					<?php if ($this->_var['list']): ?>
					<table>
						<tbody>
							<tr>
									<th><?php echo $this->_var['LANG']['USER_TITLE_USER_NAME']; ?></th>
									<th><?php echo $this->_var['LANG']['REGISTER_TIME']; ?></th>
									<th><?php echo $this->_var['LANG']['REFERRALS_GEN']; ?></th>
									<th><?php echo $this->_var['LANG']['REFERRALS_PAID']; ?></th>
									<th><?php echo $this->_var['LANG']['REFERRALS_ORDER']; ?></th>
									<th><?php echo $this->_var['LANG']['REFERRALS_GEN_TIME']; ?></th>
									<th><?php echo $this->_var['LANG']['REFERRALS_PAID_TIME']; ?></th>
									<th><?php echo $this->_var['LANG']['REFERRALS_STATUS']; ?></th>
							</tr>
							<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('key', 'invite');if (count($_from)):
    foreach ($_from AS $this->_var['key'] => $this->_var['invite']):
?>
							<tr class="alt">
									<td><?php echo $this->_var['invite']['i_user_name']; ?></td>
									<td class="dashed"><?php 
$k = array (
  'name' => 'to_date',
  'value' => $this->_var['invite']['i_reg_time'],
);
echo $k['name']($k['value']);
?></td>
									<td><?php if ($this->_var['invite']['i_referral_count'] > 0): ?><?php echo $this->_var['LANG']['YES']; ?><?php else: ?><?php echo $this->_var['LANG']['NO']; ?><?php endif; ?></td>
									<td class="dashed"><?php if ($this->_var['invite']['i_pay_time'] > 0): ?><?php echo $this->_var['LANG']['YES']; ?><?php else: ?><?php echo $this->_var['LANG']['NO']; ?><?php endif; ?></td>
									<td><?php echo $this->_var['invite']['i_order_sn']; ?></td>
									<td class="dashed"><?php 
$k = array (
  'name' => 'to_date',
  'value' => $this->_var['invite']['i_referral_time'],
);
echo $k['name']($k['value']);
?></td>
									<td><?php 
$k = array (
  'name' => 'to_date',
  'value' => $this->_var['invite']['i_pay_time'],
);
echo $k['name']($k['value']);
?></td>
									<td class="dashed">
										<?php if ($this->_var['invite']['i_money'] > 0): ?>
											<?php 
$k = array (
  'name' => 'format_price',
  'value' => $this->_var['invite']['i_money'],
);
echo $k['name']($k['value']);
?>
										<?php endif; ?>
										<?php if ($this->_var['invite']['i_score'] > 0): ?>
											<?php 
$k = array (
  'name' => 'format_score',
  'value' => $this->_var['invite']['i_score'],
);
echo $k['name']($k['value']);
?>
										<?php endif; ?>
									</td>
	                         </tr>
	                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
	                          
	
						</tbody>
					</table>
					<div class="blank"></div>
					<div class="pages"><?php echo $this->_var['pages']; ?></div>
					<?php else: ?>
					<div class="empty_tip">没有相关的邀请返利记录</div>
					<?php endif; ?>					
				</div>

			
			
			</div>				
				
				
		</div>

		<div class="blank20"></div>
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
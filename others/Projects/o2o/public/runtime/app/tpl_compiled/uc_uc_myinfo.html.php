<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/uc.css";
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
					<li <?php if ($this->_var['query_type'] == 'point'): ?>class="cur"<?php endif; ?>><a href="<?php
echo parse_url_tag("u:index|uc_myinfo#index|"."query_type=point".""); 
?>">我的成长信息</a></li>
					<li <?php if ($this->_var['query_type'] == 'score'): ?> class="cur"<?php endif; ?>><a href="<?php
echo parse_url_tag("u:index|uc_myinfo#index|"."query_type=score".""); 
?>">我的积分</a></li>
				</ul>
			</div>
			<!--经验-->
			<?php if ($this->_var['query_type'] == 'point'): ?> 
			<div class="info_box">
				<div class="blank20"></div>
				<h3>我的成长信息</h3>
				<div class="blank10"></div>
				<div class="bg_box growth_content">
					
					<div class="info_items">
						<ul>
							<li><label>我当前的等级是：</label><span class="level_bg level_<?php echo $this->_var['uc_query_data']['cur_level']; ?>" title="<?php echo $this->_var['uc_query_data']['cur_level_name']; ?>"></span></li>
							<li><label>我当前的经验值是：</label><span class="main_color"><?php echo $this->_var['uc_query_data']['cur_point']; ?></span></li>
							<?php if ($this->_var['uc_query_data']['next_level'] > 0): ?>
								<li><label>我再增加：</label><span><em class="main_color"><?php echo $this->_var['uc_query_data']['next_point']; ?></em> 经验值，就可以升级为：<em class="lv_name"><?php echo $this->_var['uc_query_data']['next_level_name']; ?></em></span></li>
							<?php endif; ?>
						</ul>
					</div>
				</div>
			</div>

			<div class="blank20"></div>
			<div class="info_box">
				<h3>我的成长记录</h3>
				<div class="blank10"></div>
				<div class="info_table">
					<table>
						<tbody>
							<tr>
								<th width="120">时间</th>
								<th width="auto">详情</th>
								<th width="70">经验值</th>
							</tr>
							<?php $_from = $this->_var['uc_query_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
							<tr class="alt">
                                <td><?php echo $this->_var['row']['log_time']; ?></td>
                                <td class="detail"><?php echo $this->_var['row']['log_info']; ?></td>
                                <td class="value increase" ><span class="growth"><?php if ($this->_var['row']['point'] > 0): ?>+<?php endif; ?><?php echo $this->_var['row']['point']; ?></span></td>
                            </tr>
                            <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                            
                            <tr >
                            	<?php if ($this->_var['uc_query_count'] > 0): ?>
                                <td><a class="more" href="<?php
echo parse_url_tag("u:index|uc_log#point|"."".""); 
?>">更多成长记录</a></td>
                                <?php else: ?>
                                <td colspan="3"><span>暂时没有成长记录，^_^ 去发发文章或者图片，累计经验你就成长了~</span></td>
                                <?php endif; ?>

                            </tr>
						</tbody>
					</table>
				</div>
				
			</div>
			<?php endif; ?>
			<!--积分-->
			<?php if ($this->_var['query_type'] == 'score'): ?> 
			<div class="info_box">
				<div class="blank20"></div>
					<h3>我的积分信息</h3>
				<div class="blank10"></div>
				<div class="bg_box ">
					<div class="info_items">
						<ul>
							<li><label>我当前的积分是：</label><span class="main_color"><?php echo $this->_var['uc_query_data']['cur_score']; ?></span></li>
							<?php if ($this->_var['uc_query_data']['cur_gourp'] > 0): ?>
							<li><label>我当前所在的会员组：</label><span class="main_color"><?php echo $this->_var['uc_query_data']['cur_gourp_name']; ?></span></li>
							<?php if ($this->_var['uc_query']['data']['cur_discount'] >= 10): ?>
							<li><label>会员组享受的折扣：</label><span class="main_color"><?php echo $this->_var['uc_query_data']['cur_discount']; ?> 折</span></li>
							<?php endif; ?>
							<?php endif; ?>
						</ul>
					</div>
				</div>
			</div>
			<div class="blank20"></div>
			<div class="info_box">
				<h3>我的积分记录</h3>
				<div class="blank10"></div>
				<div class="info_table">
					<table>
						<tbody>
							<tr>
								<th width="120">时间</th>
								<th width="auto">详情</th>
								<th width="70">积分值</th>
							</tr>
							<?php $_from = $this->_var['uc_query_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
							<tr class="alt">
                                <td><?php echo $this->_var['row']['log_time']; ?></td>
                                <td class="detail"><?php echo $this->_var['row']['log_info']; ?></td>
                                <td class="value increase" ><span class="growth"><?php if ($this->_var['row']['score'] > 0): ?>+<?php endif; ?><?php echo $this->_var['row']['score']; ?></span></td>
                            </tr>
                            <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
                            <tr >
                            	<?php if ($this->_var['uc_query_count'] > 0): ?>
                                <td ><a class="more" href="<?php
echo parse_url_tag("u:index|uc_log#score|"."".""); 
?>">更多积分记录</a></td>
                                <?php else: ?>
                                <td colspan="3"><span>暂时没有积分记录，^_^ </span></td>
                                <?php endif; ?>
                            </tr>
						</tbody>
					</table>
				</div>
			</div>
			<?php endif; ?>
		</div>
	</div>	
</div>
<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
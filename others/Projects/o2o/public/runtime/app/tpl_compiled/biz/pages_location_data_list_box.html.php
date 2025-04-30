<div class="comments_details">
	<?php if ($this->_var['ACTION_NAME'] == 'index'): ?>
	<table class="table_box ">
					<colgroup>
						<col width="90">
						<col width="420">
						<col width="150">
						<col width="100">
					</colgroup>
					<thead>
						<tr>
							<th>编号</th>
							<th>名称</th>
							<th>分类</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
					<?php if ($this->_var['list']): ?>
					<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
						<tr data-id="<?php echo $this->_var['row']['id']; ?>">
							<td class="rate">
								<?php echo $this->_var['row']['id']; ?>
							</td>
							<td>
								<div>
									<p class="rate" title="<?php echo $this->_var['row']['name']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['row']['name'],
  'l' => '0',
  'e' => '65',
);
echo $k['name']($k['v'],$k['l'],$k['e']);
?></p>
									<?php if ($this->_var['row']['preview']): ?>
										<ul class="photos_box clearfix">
												<li>
													<a href="<?php echo $this->_var['row']['preview']; ?>" target="_blank">
														<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['row']['preview'],
  'h' => '40',
  'w' => '40',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>" lazy="true"/>
													</a>
												</li>
										</ul>
									<?php endif; ?>
									
								</div>
							</td>
							<td >
								<p>【<?php echo $this->_var['row']['cate_name']; ?>】</p>
							</td>
							<td class="operate">
								<a href="<?php echo $this->_var['row']['edit_url']; ?>"><button class="ui-button edit_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">审核修改</button></a>
								<div class="blank5"></div>
								<a href="<?php echo $this->_var['row']['update_url']; ?>"  target="_blank"><button class="ui-button edit_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">资料更新</button></a>
								
								<div class="blank5"></div>
								<button class="ui-button down_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">下架</button>
								<div class="blank5"></div>
										<a href="<?php echo $this->_var['row']['preview_url']; ?>"  target="_blank"><button class="ui-button " rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">预览</button></a>
							</td>
						</tr>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					<?php else: ?>
						<tr data-id="<?php echo $this->_var['row']['id']; ?>">
							<td colspan="5">
								<div class="empty_tip">
									没有相关数据
								</div>
							</td>
						</tr>
					<?php endif; ?>		
					</tbody>
				</table>
	<?php else: ?>
	<table class="table_box ">
					<colgroup>
						<col width="90">
						<col width="420">
						<col width="150">
						<col width="100">
					</colgroup>
					<thead>
						<tr>
							<th>
								编号
							</th>
							<th>
								名称
							</th>
							<th>
								<select name="filter_admin_check" class="ui-select filter_select" >
									<option value="" <?php if ($this->_var['filter_admin_check'] == ''): ?> selected = "selected" <?php endif; ?>>状态</option>
									<option value="0" <?php if ($this->_var['filter_admin_check'] == '0'): ?> selected = "selected" <?php endif; ?>>待审核</option>
									<option value="1" <?php if ($this->_var['filter_admin_check'] == 1): ?> selected = "selected" <?php endif; ?>>通过</option>
									<option value="2" <?php if ($this->_var['filter_admin_check'] == 2): ?> selected = "selected" <?php endif; ?>>拒绝</option>
								</select>
							</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
					<?php if ($this->_var['list']): ?>
					<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
						<tr data-id="<?php echo $this->_var['row']['id']; ?>">
							<td class="rate">
								<?php echo $this->_var['row']['id']; ?>
							</td>
							<td class="review_cnt">
								<div>
									<p class="rate" title="<?php echo $this->_var['row']['name']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['row']['name'],
  'l' => '0',
  'e' => '65',
);
echo $k['name']($k['v'],$k['l'],$k['e']);
?></p>
									<?php if ($this->_var['row']['preview']): ?>
										<ul class="photos_box clearfix">
												<li>
													<a href="<?php echo $this->_var['row']['preview']; ?>" target="_blank">
														<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['row']['preview'],
  'h' => '40',
  'w' => '40',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>" lazy="true"/>
													</a>
												</li>
										</ul>
									<?php endif; ?>
								</div>
							</td>
							<td class="status_p"><?php if ($this->_var['row']['biz_apply_status'] == 2): ?><p>(修改申请)</p><?php elseif ($this->_var['row']['biz_apply_status'] == 3): ?><p>(下架申请)</p><?php else: ?><p>(新增申请)</p><?php endif; ?><?php if ($this->_var['row']['admin_check_status'] == 0): ?>待审核<?php elseif ($this->_var['row']['admin_check_status'] == 1): ?>通过<?php elseif ($this->_var['row']['admin_check_status'] == 2): ?>拒绝<?php endif; ?></td>
							<td class="operate">
								<?php if ($this->_var['row']['admin_check_status'] == 0): ?>
									<?php if ($this->_var['row']['biz_apply_status'] != 3): ?>
										<a href="<?php echo $this->_var['row']['edit_url']; ?>">
											<button class="ui-button edit_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">修改</button>
										</a>
										<div class="blank5"></div>
										<a href="<?php echo $this->_var['row']['preview_url']; ?>"  target="_blank"><button class="ui-button edit_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">预览</button></a>
										<div class="blank5"></div>
										
									<?php endif; ?>
									<button class="ui-button del_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">删除</button>
								<?php elseif ($this->_var['row']['admin_check_status'] == 1 || $this->_var['row']['admin_check_status'] == 2): ?>
									<button class="ui-button del_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">删除</button>
								<?php endif; ?>
							</td>
						</tr>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					<?php else: ?>
						<tr>
							<td colspan="5">
								<div class="empty_tip">
									没有相关数据
								</div>
							</td>
						</tr>
					<?php endif; ?>		
					</tbody>
				</table>
	<?php endif; ?>
	<div class="blank"></div>
	<div class="pages">
		<?php echo $this->_var['pages']; ?>
	</div>
</div>
		
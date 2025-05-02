
<div class="comments_details">
	<table class="review_list_table table_box">
					<colgroup>
						<col width="90">
						<col width="270">
						<col width="150">
						<col width="150">
						<col width="100">
					</colgroup>
					<thead>
						<tr>
							<th>
								<select name="filter_point" class="ui-select filter_select" <?php echo $this->_var['filter_point']; ?>>
									<option value="0" <?php if ($this->_var['filter_point'] == 0): ?> selected = "selected" <?php endif; ?>>全部</option>
									<option value="1" <?php if ($this->_var['filter_point'] == 1): ?> selected = "selected" <?php endif; ?>>好评</option>
									<option value="2" <?php if ($this->_var['filter_point'] == 2): ?> selected = "selected" <?php endif; ?>>中评</option>
									<option value="3" <?php if ($this->_var['filter_point'] == 3): ?> selected = "selected" <?php endif; ?>>差评</option>
								</select>
							</th>
							<th>
								<select name="filter_is_img" class="ui-select filter_select" >
									<option value="0" <?php if ($this->_var['filter_is_img'] == 0): ?> selected = "selected" <?php endif; ?>>评论内容</option>
									<option value="1" <?php if ($this->_var['filter_is_img'] == 1): ?> selected = "selected" <?php endif; ?>>有图</option>
									<option value="2" <?php if ($this->_var['filter_is_img'] == 2): ?> selected = "selected" <?php endif; ?>>无图</option>
								</select>
							</th>
							<th>评论人</th>
							<th>被评论来源</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
					<?php if ($this->_var['dp_list']): ?>
					<?php $_from = $this->_var['dp_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
						<tr data-id="<?php echo $this->_var['row']['id']; ?>">
							<td class="rate">
								<?php if ($this->_var['row']['fpoint'] == 1): ?>
								<i class="iconfont" title="好评">&#xe604;</i>
								<?php elseif ($this->_var['row']['fpoint'] == 2): ?>
								<i class="iconfont" title="中评">&#xe605;</i>
								<?php else: ?>
								<i class="iconfont" title="差评">&#xe603;</i>
								<?php endif; ?>
							</td>
							<td class="review_cnt">
								<div class="review_cnt_bd review_cnt_<?php echo $this->_var['row']['id']; ?>">
									<p class="rate" title="<?php echo $this->_var['row']['content']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['row']['content'],
  'l' => '0',
  'e' => '60',
);
echo $k['name']($k['v'],$k['l'],$k['e']);
?></p>
									<?php if ($this->_var['row']['images']): ?>
										<ul class="photos_box clearfix">
											<?php $_from = $this->_var['row']['images']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'img_row');if (count($_from)):
    foreach ($_from AS $this->_var['img_row']):
?>
												<li>
													<a href="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img_row'],
  'h' => '400',
  'w' => '400',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>" target="_blank"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img_row'],
  'h' => '40',
  'w' => '40',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>"/></a>
												</li>
											<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
										</ul>
									<?php endif; ?>
									<span class="date">[<?php echo $this->_var['row']['create_time_format']; ?>]</span>
									<?php if ($this->_var['row']['reply_content']): ?>
										<p class="exp">[回复]<?php echo $this->_var['row']['reply_content']; ?></p>
									<?php endif; ?>
								</div>
							</td>
							<td class="r_user"><a href="<?php
echo parse_url_tag("u:index|uc_home#index|"."id=".$this->_var['row']['user_id']."".""); 
?>"  target="_blank"><?php echo $this->_var['row']['user_info']['user_name']; ?></a><span class="level_bg level_5"></span></td>
							<td class="s_obj"><a href="<?php echo $this->_var['row']['filter_data']['url']; ?>" target="_blank"><?php echo $this->_var['row']['filter_data']['name']; ?></a></td>
							<td class="operate"><button class="ui-button reply_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>"><?php if ($this->_var['row']['reply_content']): ?>修改<?php else: ?>回复<?php endif; ?></button></td>
						</tr>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					<?php else: ?>
						<tr data-id="<?php echo $this->_var['row']['id']; ?>">
							<td colspan="5">
								<div class="empty_tip">
									没有相关点评数据
								</div>
							</td>
						</tr>
					<?php endif; ?>		
					</tbody>
				</table>
	<div class="blank"></div>
	<div class="pages">
		<?php echo $this->_var['pages']; ?>
	</div>
</div>
		
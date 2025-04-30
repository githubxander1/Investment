<div class="evaluation">
<div class="rating clearfix">
	<table>
		<tr>
			<td class="rate_box noborder">
				<div class="total_group total_num">
					<b><?php echo $this->_var['dp_data']['avg_point']; ?></b><span>分</span>
				</div>
				<div class="total_group">
					<input class="ui-starbar" value="<?php echo $this->_var['dp_data']['avg_point']; ?>" disabled="true"  />
				</div>
				<div class="total_group total_count">
					共
					<strong><?php echo $this->_var['dp_data']['dp_count']; ?></strong>
					人评价
				</div>
			</td>
			<?php if ($this->_var['dp_data']['point_group']): ?>
			<td class="rate_box">
				<?php $_from = $this->_var['dp_data']['point_group']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'point_group');if (count($_from)):
    foreach ($_from AS $this->_var['point_group']):
?>
				<div class="total_g clearfix">
					<div class="this_title"><?php echo $this->_var['point_group']['name']; ?></div>
						<div class="f_l" >							
							<input class="ui-starbar" value="<?php echo $this->_var['point_group']['avg_point']; ?>" disabled="true"  />
						</div>
					<div class="this_num"><?php echo $this->_var['point_group']['avg_point']; ?>分</div>	
				</div>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</td>
			<?php endif; ?>
			<td class="rate_box noborder">
				<div class="count-group">
					<span class="score f_l">5分</span>
					<span class="percent_box f_l">
						<span style=" width:<?php echo $this->_var['dp_data']['avg_point_5_percent']; ?>%;"></span>
					</span>
					<span class="people f_l"><?php echo $this->_var['dp_data']['dp_count_5']; ?>人</span>
				</div>
				<div class="count-group">
					<span class="score f_l">4分</span>
					<span class="percent_box f_l">
						<span style=" width:<?php echo $this->_var['dp_data']['avg_point_4_percent']; ?>%;"></span>
					</span>
					<span class="people f_l"><?php echo $this->_var['dp_data']['dp_count_4']; ?>人</span>
				</div>
				<div class="count-group">
					<span class="score f_l">3分</span>
					<span class="percent_box f_l">
						<span style=" width:<?php echo $this->_var['dp_data']['avg_point_3_percent']; ?>%;"></span>
					</span>
					<span class="people f_l"><?php echo $this->_var['dp_data']['dp_count_3']; ?>人</span>
				</div>
				<div class="count-group">
					<span class="score f_l">2分</span>
					<span class="percent_box f_l">
						<span style=" width:<?php echo $this->_var['dp_data']['avg_point_2_percent']; ?>%;"></span>
					</span>
					<span class="people f_l"><?php echo $this->_var['dp_data']['dp_count_2']; ?>人</span>
				</div>
				<div class="count-group">
					<span class="score f_l">1分</span>
					<span class="percent_box f_l">
						<span style=" width:<?php echo $this->_var['dp_data']['avg_point_1_percent']; ?>%;"></span>
					</span>
					<span class="people f_l"><?php echo $this->_var['dp_data']['dp_count_1']; ?>人</span>
				</div>
			</td>
		</tr>
	</table>
						
		</div>
		<?php $_from = $this->_var['dp_data']['tag_group']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'tag_group');if (count($_from)):
    foreach ($_from AS $this->_var['tag_group']):
?>
		<div class="attitude over clearfix">
			<span class="title f_l"><?php echo $this->_var['tag_group']['name']; ?>:</span>
			<div class="labels f_l active_parent">
				<?php $_from = $this->_var['tag_group']['tags']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'tag');if (count($_from)):
    foreach ($_from AS $this->_var['tag']):
?>
				<a href="javascript:void(0);" gid="<?php echo $this->_var['tag_group']['id']; ?>" class="lab good <?php if ($this->_var['tag'] == $this->_var['filter_tag'] && $this->_var['gid'] == $this->_var['tag_group']['id']): ?>active<?php endif; ?>" <?php if ($this->_var['tag'] != $this->_var['filter_tag'] || $this->_var['gid'] != $this->_var['tag_group']['id']): ?>rel="<?php echo $this->_var['tag']; ?>"<?php endif; ?>><?php echo $this->_var['tag']; ?>(<?php echo $this->_var['tag_group']['tags_count'][$this->_var['tag']]; ?>)</a>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
			</div>			
		</div>
		<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
		<div class="blank"></div>
		
		
		<div class="clearfix">
			<div class="sort_row">
				<ul>
					<li class="anode <?php if ($this->_var['sort_data']['sort_field'] == 0): ?>current<?php endif; ?>"><a href="javascript:void(0);" v="0">默认排序</a></li>
					<li class="anode <?php if ($this->_var['sort_data']['sort_field'] == 1): ?>current<?php endif; ?> <?php if ($this->_var['sort_data']['sort_type'] == 'asc' && $this->_var['sort_data']['sort_field'] == 1): ?>asc<?php else: ?>desc<?php endif; ?>"><a href="javascript:void(0);" v="1" t="<?php if ($this->_var['sort_data']['sort_type'] == 'desc' && $this->_var['sort_data']['sort_field'] == 1): ?>asc<?php else: ?>desc<?php endif; ?>">好评<i class="iconfont"><?php if ($this->_var['sort_data']['sort_type'] == 'asc' && $this->_var['sort_data']['sort_field'] == 1): ?>&#xe61c;<?php else: ?>&#xe61d;<?php endif; ?></i></a></li>
					<li class="anode <?php if ($this->_var['sort_data']['sort_field'] == 2): ?>current<?php endif; ?> <?php if ($this->_var['sort_data']['sort_type'] == 'asc' && $this->_var['sort_data']['sort_field'] == 2): ?>asc<?php else: ?>desc<?php endif; ?>"><a href="javascript:void(0);" v="2" t="<?php if ($this->_var['sort_data']['sort_type'] == 'desc' && $this->_var['sort_data']['sort_field'] == 2): ?>asc<?php else: ?>desc<?php endif; ?>">差评<i class="iconfont"><?php if ($this->_var['sort_data']['sort_type'] == 'asc' && $this->_var['sort_data']['sort_field'] == 2): ?>&#xe61c;<?php else: ?>&#xe61d;<?php endif; ?></i></a></li>
					
		
					
		
					<li class="dnode">
					<select class="ui-drop" name="review_filter">
						
						<option value="0" <?php if ($this->_var['sort_data']['filter'] == 0): ?>selected="selected"<?php endif; ?>>全部点评</option>
						<option value="1" <?php if ($this->_var['sort_data']['filter'] == 1): ?>selected="selected"<?php endif; ?>>好评</option>
						<option value="2" <?php if ($this->_var['sort_data']['filter'] == 2): ?>selected="selected"<?php endif; ?>>中评</option>
						<option value="3" <?php if ($this->_var['sort_data']['filter'] == 3): ?>selected="selected"<?php endif; ?>>差评</option>
			
					</select>
					</li>
		
					
			
					<li class="cnode">
					<label class="ui-checkbox dtag" rel="common_cbo"><input type="checkbox" value="1" name="is_img" <?php if ($this->_var['sort_data']['is_img'] == 1): ?>checked="checked"<?php endif; ?> />有图</label>
					</li>
					<li class="cnode">									
					<label class="ui-checkbox dtag" rel="common_cbo"><input type="checkbox" value="1"  name="is_content" <?php if ($this->_var['sort_data']['is_content'] == 1): ?>checked="checked"<?php endif; ?>  />有内容的评价</label>
					</li>
				
				</ul>
			</div>
		</div>
		
		
		<?php if ($this->_var['dp_list']): ?>
		<div class="comments_details">
			<ul>
				<?php $_from = $this->_var['dp_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'dp_item');if (count($_from)):
    foreach ($_from AS $this->_var['dp_item']):
?>
				<li class="details_li">
					<div class="clearfix">
						<div class="f_l">
							<span class="user_name"><?php 
$k = array (
  'name' => 'get_user_name',
  'value' => $this->_var['dp_item']['user_id'],
  'show_tag' => '0',
);
echo $k['name']($k['value'],$k['show_tag']);
?> </span>
							<span class="date"><?php echo $this->_var['dp_item']['create_time_format']; ?></span>
						</div>
						<div class="f_r">
							<input class="ui-starbar" value="<?php echo $this->_var['dp_item']['point']; ?>" disabled="true"  />
						</div>
					</div>
					<p class="content">
						<?php echo $this->_var['dp_item']['content']; ?>
					</p>
					
					<?php if ($this->_var['dp_item']['images']): ?>
					<div class="review_pic clearfix">
						<div class="over">
							<div  class="pic_box">
							     <ul>
							     	<?php $_from = $this->_var['dp_item']['images']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'img');if (count($_from)):
    foreach ($_from AS $this->_var['img']):
?>
							     	<li>
							     		<a href="javascript:void(0);" rel="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img'],
  'w' => '670',
  'h' => '0',
);
echo $k['name']($k['v'],$k['w'],$k['h']);
?>"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img'],
  'w' => '100',
  'h' => '100',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" /></a>
							     	</li>
									<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>									
									
								 </ul>
							</div>
							
							<?php if (count ( $this->_var['dp_item']['images'] ) > 6): ?>
							<a href="javascript:void(0);" class="pre hide_tag"></a>
							<a href="javascript:void(0);" class="next hide_tag"></a>
							<?php endif; ?>
						</div>
						<div class="blank"></div>
						<div class="big_img">
							<a href="javascript:void(0);" class="bprev"></a>
							<a href="javascript:void(0);" class="bnext"></a>
							<img src="" />							
							<div class="blank"></div>
						</div>
					</div>
					<?php endif; ?>
					<?php if ($this->_var['dp_item']['reply_content']): ?>
					<div class="supplier_reply"><span class="reply_title">掌柜回复：</span><?php echo $this->_var['dp_item']['reply_content']; ?></div>
					<?php endif; ?>
				</li>
				<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>				
			</ul>
			<div class="blank"></div>
			<div class="pages">
				<?php echo $this->_var['pages']; ?>
			</div>
		</div>
		<?php else: ?>
		<div class="empty_tip">
			没有相关点评数据
		</div>
		<?php endif; ?>			
</div>
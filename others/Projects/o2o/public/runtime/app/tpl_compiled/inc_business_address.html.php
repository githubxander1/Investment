<div class="business_adress clearfix">
		<div class="content">
				<div class="content_left">
					<?php if ($this->_var['location_list']): ?>
					<div id="supplier_map"></div>
					<?php endif; ?>
				</div>
				<div class="content_right f_r">
					<div class="position">
						<span class="title">位置筛选</span>
						<div class="select_list">
								<select name="city_id" class="ui-select search_type f_l" height=100>
									<?php $_from = $this->_var['city_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'city');if (count($_from)):
    foreach ($_from AS $this->_var['city']):
?>
									<?php if ($this->_var['city']['current']): ?>
									<option value="<?php echo $this->_var['city']['id']; ?>" <?php if ($this->_var['city']['current']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['city']['name']; ?></option>
									<?php endif; ?>
									<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
								</select>
								<select name="aid" class="ui-select search_type f_l" height=100>											
									<option value="0">全部城区</option>
									<?php $_from = $this->_var['area_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'area');if (count($_from)):
    foreach ($_from AS $this->_var['area']):
?>
									<option value="<?php echo $this->_var['area']['id']; ?>" <?php if ($this->_var['area']['current']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['area']['name']; ?></option>
									<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
								</select>
								<select name="qid" class="ui-select search_type f_l" height=100>
									<option value="0">全部商圈</option>
									<?php $_from = $this->_var['quan_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'quan');if (count($_from)):
    foreach ($_from AS $this->_var['quan']):
?>
									<option value="<?php echo $this->_var['quan']['id']; ?>" <?php if ($this->_var['quan']['current']): ?>selected="selected"<?php endif; ?>><?php echo $this->_var['quan']['name']; ?></option>
									<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
								</select>
						</div>
					</div>
					<?php if ($this->_var['location_list']): ?>
					<div class="details_address">
						
						<ul>
							<?php $_from = $this->_var['location_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'location');if (count($_from)):
    foreach ($_from AS $this->_var['location']):
?>
							<li class="details_address_li show_hide">
								<h5 class="title">
									<a href="<?php echo $this->_var['location']['url']; ?>" class="f_l" title="<?php echo $this->_var['location']['name']; ?>"  target="_blank"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['location']['name'],
  'b' => '0',
  'e' => '15',
);
echo $k['name']($k['v'],$k['b'],$k['e']);
?></a>
									<i class="f_r none"></i>
									</h5>
								<div class=" info show_hide_child">
									<div class="how_num">
										<span class="tit">评价:</span>
										<a href="<?php echo $this->_var['location']['url']; ?>" target="_blank">
											<?php if ($this->_var['location']['dp_count'] > 0): ?>
											<span class="yes"><?php echo $this->_var['location']['dp_count']; ?>人评价</span>
											<?php else: ?>
											<span class="no">暂无评价</span>
											<?php endif; ?>
											
										</a>
									</div>
									<div class="ress clearfix">
										<span class="public_title f_l">地址:</span>
										<div class="f_r p">
											<p>
											<?php echo $this->_var['location']['address']; ?>
											</p>
											<div class="see">
												<a href="javascript:void(0);" class='map_data' store_name="<?php echo $this->_var['location']['name']; ?>" xpoint="<?php echo $this->_var['location']['xpoint']; ?>" ypoint="<?php echo $this->_var['location']['ypoint']; ?>" store_url="<?php echo $this->_var['location']['url']; ?>" store_tel="<?php echo $this->_var['location']['tel']; ?>" store_address="<?php echo $this->_var['location']['address']; ?>">查看地图</a>
											</div>
										</div>
									</div>
									<div class="ress clearfix">
										<span class="public_title f_l">电话:</span>
										<p><?php echo $this->_var['location']['tel']; ?></p>
									</div>
								</div>
							</li>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							
							
							
						</ul>
						
					</div>
					<div class="clearfix ress_bottom">
						<div class="fy f_l clearfix">
						<div class="pages"><?php echo $this->_var['pages']; ?></div>
					</div>
						<a href="<?php echo $this->_var['sellall']; ?>"  class="see_all font_hover f_r underline" target="_blank">查看所有分店»</a>
					</div>
					<?php else: ?>
					<div class="empty_tip">没有门店信息</div>
					<?php endif; ?>
				</div>
			</div>
</div>
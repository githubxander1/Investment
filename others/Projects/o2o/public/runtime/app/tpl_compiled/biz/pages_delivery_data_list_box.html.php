<div class="comments_details">
	<table class="table_box ">
		<colgroup>
			<col width="90">
			<col width="570">

			<col width="100">
		</colgroup>
		<thead>
			<tr>
				<th>编号</th>
				<th>名称</th>
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
				
				<td class="operate">
					<a href="<?php echo $this->_var['row']['edit_url']; ?>"><button class="ui-button edit_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>">设置</button></a>

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
	
	<div class="blank"></div>
	<div class="pages">
		<?php echo $this->_var['pages']; ?>
	</div>
</div>
		
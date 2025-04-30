		<div class="info_table relate_deal">						
						<table>						
								<tr>
									<th style="width:10px;"></th>
									<th style="width:120px;">缩略图</th>
									<th>名称</th>
								</tr>
								<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'item');if (count($_from)):
    foreach ($_from AS $this->_var['item']):
?>	
								<tr class="alt" rel="<?php echo $this->_var['item']['id']; ?>">
		                               <td class="add_relate">+</td>
		                               <td class="detail"><img  src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['item']['icon'],
  'w' => '70',
  'h' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" style="width:70px;height:50px;"></td>
		                               <td class="relate_name"><?php echo $this->_var['item']['name']; ?></td>                               
		                         </tr>
		                         <?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>	
				
						</table>
						
			</div>
			<div class="pages"><?php echo $this->_var['pages']; ?></div>
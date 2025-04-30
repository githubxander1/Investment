<div class="publish_goods_info_page">
	<form name="publish_edit_form" action="<?php
echo parse_url_tag("u:index|ajax#publish_save|"."".""); 
?>" method="post">
	<div class="pub_g_info_item_box">
		<div class="g_item_info">
			<div class="g_i_pic">
				<div class="b112">
					<div class="pic s120">
						<?php if ($this->_var['result_data']['images'] && count ( $this->_var['result_data']['images'] ) > 0): ?>
						<a href="javascript:void(0);"><img src="<?php echo $this->_var['result_data']['images']['0']['url']; ?>"/><i class=""></i></a>
						<?php endif; ?>
					</div>
				</div>
			</div>
		</div>
		<div class="g_item_edit_area f_l">
			<?php echo $this->fetch('inc/publish_edit_box.html'); ?>
		</div>
		<div class="pub_g_info_btn">
			<input type="hidden" name="jump" value="<?php
echo parse_url_tag("u:index|uc_home#index|"."".""); 
?>">
			<input type="hidden" name="ajax" value="1">
			<?php if ($this->_var['result_data']['images'] && count ( $this->_var['result_data']['images'] ) > 0): ?>
			<input type="hidden" name="topic_image_idx[1]" value="1">
			<input type="hidden" name="topic_image_id[1]" value="<?php echo $this->_var['result_data']['images']['0']['id']; ?>">
			<input type="hidden" name="topic_image_url[1]" value="<?php echo $this->_var['result_data']['images']['0']['url']; ?>">
			<?php endif; ?>
			<input type="hidden" name="type" value="<?php echo $this->_var['result_data']['type']; ?>"/>
			<input type="hidden" name="group" value="<?php echo $this->_var['result_data']['group']; ?>"/>
			<input type="hidden" name="group_data" value="<?php echo $this->_var['result_data']['group_data']; ?>"/>
			<div class="publish_btn_box">
				<button class="ui-button" rel="orange"> 提 交 </button>
			</div>
		</div>
	</div>
	</form>
</div>
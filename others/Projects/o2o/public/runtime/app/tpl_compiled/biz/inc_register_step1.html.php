<div class="con_box">
	<form name="user_register_1" action="<?php
echo parse_url_tag("u:biz|user#register|"."step=2".""); 
?>" method="post" bindsubmit="true">
		<div class="agree_title"><?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'SHOP_TITLE',
);
echo $k['name']($k['v']);
?>服务协议</div>

					    <div class="bd">					
							<div class="agree_content" style="height: 296px;line-height:28px;">
								<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'BIZ_AGREEMENT',
);
echo $k['name']($k['v']);
?>
							</div>					
						</div>
						<div class="blank20"></div>
						<div class="tc pd10">
							<input type="hidden" name="base_data" value="<?php echo $this->_var['base_data']; ?>" />
							<button class="ui-button " rel="orange" type="submit">同意</button>&nbsp;&nbsp;&nbsp;&nbsp;
						</div>
			
	</form>
	<div class="blank20"></div>
</div>
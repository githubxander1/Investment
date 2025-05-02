<form method="post" action='<?php
echo parse_url_tag("u:index|uc_order#do_refund|"."".""); 
?>' name="refund_form">
	<textarea class="refund_textarea ui-textbox" holder="请输入退款申请的理由" name="content"></textarea>
	<input type="hidden" name="did" value="<?php echo $this->_var['did']; ?>" />
	<input type="hidden" name="cid" value="<?php echo $this->_var['cid']; ?>" />
</form>
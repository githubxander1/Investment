<?php if (!defined('THINK_PATH')) exit();?><form name="refund_form" method="post">
<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>
	<tr>
		<td colspan=2>
			<table>
				<tr>
					<td style="border:none;">
					<img src="<?php echo ($data["deal_icon"]); ?>" width=50 />
					</td>
					<td style="border:none;">
					<?php echo ($data["name"]); ?>
					</td>
				</tr>
			</table>
			
		</td>
	</tr>
	<tr>
		<td class="item_title">退款金额：</td>
		<td class="item_input">退还 <input type="text" name="price" value="<?php echo (floatval($data["price"])); ?>" style="width:50px;" /> 元到 <?php echo ($order_info["user_name"]); ?> 的账户余额</td>
	</tr>
	<tr>
		<td class="item_title">商户结算退款：</td>
		<td class="item_input"><input type="text" name="balance_price" value="<?php echo (floatval($data["balance_price"])); ?>" style="width:50px;" /> 元</td>
	</tr>
	<tr>
		<td class="item_title">备注：</td>
		<td class="item_input">
			<textarea class="text" name="content"></textarea>
		</td>
	</tr>
	<tr>
		<td colspan=2 style="text-align:center;">
			<input type="hidden" name="<?php echo ($data["key"]); ?>" value="<?php echo ($data["id"]); ?>" />
			<input type="button" class="button" id="confirm" value="确认退款" action="<?php echo u("DealOrder/do_refund");?>" />
			<input type="button" class="button" id="refuse" value="拒绝退款" action="<?php echo u("DealOrder/do_refuse");?>" />
		</td>
	</tr>
	<tr>
		<td colspan=2 class="bottomTd"></td>
	</tr>
</table>
</form>
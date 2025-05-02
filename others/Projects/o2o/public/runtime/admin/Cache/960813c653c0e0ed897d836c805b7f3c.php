<?php if (!defined('THINK_PATH')) exit();?>
<script type="text/javascript">
	function check_incharge_form()
	{

		if($("input[name='money']").val()!=''&&isNaN($("input[name='money']").val()))
		{
			alert(LANG['MONEY_FORMAT_ERROR']);
			return false;
		}

		return true;
	}
</script>
<div class="main">
<?php if($type == 1): ?><div class="main_title"><?php echo ($charge_info["supplier_name"]); ?> 可提现总余额:<?php echo (format_price($charge_info["supplier_money"])); ?></div>
<?php else: ?>
<div class="main_title"><?php echo ($supplier_info["name"]); ?> 可提现总余额:<?php echo (format_price($supplier_info["money"])); ?></div><?php endif; ?>
<div class="blank5"></div>
<form name="edit" action="__APP__" method="post" enctype="multipart/form-data" onsubmit="return check_incharge_form();">
<table class="form" cellpadding=0 cellspacing=0>
	<tr>
		<td colspan=2 class="topTd"></td>
	</tr>
	<tr>
		<td class="item_title">本次<?php if($type == 1): ?>提现<?php else: ?>打款<?php endif; ?>金额:</td>
		<td class="item_input"><input type="text" class="textbox require" name="money" value="<?php if($type == 1): ?><?php echo ($charge_info["money"]); ?><?php endif; ?>"/>
		<span class='tip_span'>[实际打款给商户的金额，单位（元）]</span>
		</td>
	</tr>

	<tr>
		<td class="item_title"><?php echo L("INCHARGE_MSG");?>:</td>
		<td class="item_input"><input type="text" class="textbox" name="log" style="width:400px;" />
		</td>
	</tr>
	<tr>
		<td class="item_title">&nbsp;</td>
		<td class="item_input">
			<!--隐藏元素-->
			<?php if($type == 1): ?><input type="hidden" name="charge_id" value="<?php echo ($charge_info["id"]); ?>" />
			<?php else: ?>
			<input type="hidden" name="supplier_id" value="<?php echo ($supplier_info["id"]); ?>" /><?php endif; ?>
			<input type="hidden" name="<?php echo conf("VAR_MODULE");?>" value="Supplier" />
			<input type="hidden" name="<?php echo conf("VAR_ACTION");?>" value="docharge" />
			<!--隐藏元素-->
			<input type="submit" class="button" value="<?php echo L("OK");?>" />
			<input type="reset" class="button" value="<?php echo L("RESET");?>" />
		</td>
	</tr>
	<tr>
		<td colspan=2 class="bottomTd"></td>
	</tr>
</table>	 
</form>
</div>
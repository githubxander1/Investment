<?php if (!defined('THINK_PATH')) exit();?><style type="text/css">
	table.noborder td{ border:0px;}
</style>
<table class="noborder">
<?php if(is_array($group_list)): foreach($group_list as $key=>$group): ?><tr>
	<td><?php echo ($group["name"]); ?> </td>
	<td>
		标签显示：<input type="text"  class="textbox" name="show_group_id[<?php echo ($group["id"]); ?>]" value="<?php echo ($group["show_value"]); ?>" size="30" /> 		
	</td>
	<!--<td>
		<?php if($group['allow_dp'] == 1): ?>预设点评：<input type="text"  class="textbox" name="group_id[<?php echo ($group["id"]); ?>]" value="<?php echo ($group["value"]); ?>" size="30" /><?php endif; ?>		
	</td>-->
	
	</tr><?php endforeach; endif; ?>
	<tr>
		<td colspan=2>
			<span class="tip_span">[以空格分隔标签，标签显示中以|分隔显示数量(该数量默认为点评数据统计，不填为0)]</span>
		</td>
	</tr>
</table>
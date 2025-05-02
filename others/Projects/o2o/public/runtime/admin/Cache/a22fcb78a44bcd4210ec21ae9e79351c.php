<?php if (!defined('THINK_PATH')) exit();?><select name="pid">
	<option value="0"><?php echo L("TOP_AREA");?></option>
	<?php if(is_array($area_list)): foreach($area_list as $key=>$area): ?><option value="<?php echo ($area["id"]); ?>" <?php if($vo['pid'] == $area['id']): ?>selected="selected"<?php endif; ?>><?php echo ($area["name"]); ?></option><?php endforeach; endif; ?>
</select>
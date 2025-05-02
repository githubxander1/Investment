<?php if (!defined('THINK_PATH')) exit();?><?php if($area_list): ?><?php if(is_array($area_list)): foreach($area_list as $key=>$area): ?><?php if($area['pid'] == 0): ?><div class="area_big_box" style="float:left">
	<label><input type="checkbox" name="area_id[]" value="<?php echo ($area["id"]); ?>" <?php if($area['checked']): ?>checked="checked"<?php endif; ?> /><?php echo ($area["name"]); ?>：</label>
	</div>
	<div class="area_small_box_<?php echo ($area["id"]); ?>" style="float:left">
		<?php if(is_array($area_list)): foreach($area_list as $key=>$areas): ?><?php if($areas['pid'] == $area['id']): ?><label><input type="checkbox" name="area_id[]" value="<?php echo ($areas["id"]); ?>" <?php if($areas['checked'] > 0){echo 'checked="checked"';} ?> /><?php echo ($areas["name"]); ?></label><?php endif; ?><?php endforeach; endif; ?>
	</div>
	<div class="blank5"></div>
	<div style="border-bottom:solid 1px #ccc;"></div><?php endif; ?><?php endforeach; endif; ?>
<script language="JavaScript">
	$(".area_big_box input").click(function(){
		if($(this).attr("checked")==true){
			$(".area_small_box_"+$(this).val()+" input").each(function(){
				$(this).attr("checked",true);
			});
		}
		else
		{
			$(".area_small_box_"+$(this).val()+" input").each(function(){
				$(this).attr("checked",false);
			});
		}
	});
</script>
<?php else: ?>
<?php echo L("NO_AREALIST");?><?php endif; ?>
<?php if (!defined('THINK_PATH')) exit();?>
<?php if(is_array($filter_group)): foreach($filter_group as $key=>$filter_item): ?><div>
		<span id="title_<?php echo ($filter_item["id"]); ?>"><?php echo ($filter_item["name"]); ?></span>：
		<input type="text" class="textbox" name="filter[<?php echo ($filter_item["id"]); ?>]" value="<?php echo ($filter_item["value"]); ?>" />
		<div class="blank5"></div>
	</div><?php endforeach; endif; ?>
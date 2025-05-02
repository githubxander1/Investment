<?php if ($this->_var['area_list']): ?>
<div class="sub_table_box">
	<table cellspacing="0" cellpadding="0" border="0" class="standard-table">
		<tbody>
			<?php $_from = $this->_var['area_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('area_key', 'area');if (count($_from)):
    foreach ($_from AS $this->_var['area_key'] => $this->_var['area']):
?> 
				<?php if ($this->_var['area']['pid'] == 0): ?>
					<tr>
						<td width="20%" class="r_border"><label class="ui-checkbox" rel="common_cbo" module_name="<?php echo $this->_var['area_key']; ?>" is_main="1"> 
							<input type="checkbox" <?php if ($this->_var['area']['checked'] == 1): ?>checked="true" <?php endif; ?> name="area_id[]" value="<?php echo $this->_var['area']['id']; ?>"/><?php echo $this->_var['area']['name']; ?></label>
						</td>
						<td width="80%">
						<?php $_from = $this->_var['area_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('sub_area_key', 'sub_area');if (count($_from)):
    foreach ($_from AS $this->_var['sub_area_key'] => $this->_var['sub_area']):
?> 
							<?php if ($this->_var['sub_area']['pid'] == $this->_var['area']['id']): ?> 
							<span class="t_item"> <label class="ui-checkbox" rel="common_cbo"is_sub="1"> 
								<input type="checkbox" name="area_id[]" value="<?php echo $this->_var['sub_area']['id']; ?>" module_name="<?php echo $this->_var['area_key']; ?>" <?php if ($this->_var['sub_area']['checked'] == 1): ?>checked="true" <?php endif; ?> /><?php echo $this->_var['sub_area']['name']; ?></label>
							</span> 
							<?php endif; ?>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
						</td>
					</tr>
				<?php endif; ?> 
			<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>

		</tbody>
	</table>
</div>
<?php else: ?> 
没有相关地区 
<?php endif; ?>

<script>
$(function() {
	init_ui_checkbox();
	$("label.ui-checkbox[is_main='1'] input").bind("checkon", function() {
		var module_name = $(this).parent().attr("module_name");
		$(".ui-checkbox input[module_name='" + module_name + "']").each(function(i, o) {
			$(this).attr("checked", true);
			$(this).parent().ui_checkbox({
				refresh : true
			});
		});
	});
	$("label.ui-checkbox[is_main='1'] input").bind("checkoff", function() {
		var module_name = $(this).parent().attr("module_name");
		$(".ui-checkbox input[module_name='" + module_name + "']").each(function(i, o) {
			$(this).attr("checked", false);
			$(this).parent().ui_checkbox({
				refresh : true
			});
		});
	});

	$("label.ui-checkbox[is_sub='1'] input").bind("checkon", function() {
		var module_name = $(this).attr("module_name");
		var total_count = $(".ui-checkbox input[module_name='" + module_name + "']").length;
		var count = 0;
		$(".ui-checkbox input[module_name='" + module_name + "']").each(function(i, o) {
			if($(this).attr("checked")) {
				count++;
			}
		});
		if(total_count == count) {
			$("label.ui-checkbox[module_name='" + module_name + "'] input").attr("checked", true);
			$("label.ui-checkbox[module_name='" + module_name + "']").ui_checkbox({
				refresh : true
			});
		}

	});
	
	$("label.ui-checkbox[is_sub='1'] input").bind("checkoff", function() {
		var module_name = $(this).attr("module_name");
		var total_count = $(".ui-checkbox input[module_name='" + module_name + "']").length;
		var count = 0;
		$(".ui-checkbox input[module_name='" + module_name + "']").each(function(i, o) {
			if($(this).attr("checked")) {
				count++;
			}
		});
		if(count < total_count) {
			$("label.ui-checkbox[module_name='" + module_name + "'] input").attr("checked", false);
			$("label.ui-checkbox[module_name='" + module_name + "']").ui_checkbox({
				refresh : true
			});
		}
	});
	
	$.Refresh_mainstatus = function(){
		$("label.ui-checkbox[is_main='1'] input").each(function(i,o){
			var module_name = $(this).val();
			var total_count = $(".ui-checkbox input[module_name='" + module_name + "']").length;
			var count = 0;
			$(".ui-checkbox input[module_name='" + module_name + "']").each(function(i, o) {
				if($(this).attr("checked")) {
					count++;
				}
			});
			if(total_count == count) {
				$("label.ui-checkbox[module_name='" + module_name + "'] input").attr("checked", true);
				$("label.ui-checkbox[module_name='" + module_name + "']").ui_checkbox({
					refresh : true
				});
			}
		});
	};
	$.Refresh_mainstatus();

});

</script>
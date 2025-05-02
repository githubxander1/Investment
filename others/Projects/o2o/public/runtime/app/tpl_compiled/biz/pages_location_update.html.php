<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/project.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/location.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/kindeditor.css";



$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery-1.8.2.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/kindeditor.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/plupload.full.min.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/location/update.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/location/update.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'BAIDU_MAP_APPKEY',
);
echo $k['name']($k['v']);
?>"></script> 
<script type="text/javascript" src="<?php echo $this->_var['TMPL']; ?>/js/utils/biz.location.map.js"></script> 
<script>
var ajax_url = '<?php echo $this->_var['ajax_url']; ?>';
var blue_point = "<?php echo $this->_var['APP_ROOT']; ?>/system/blue_point.png";
var red_point = "<?php echo $this->_var['APP_ROOT']; ?>/system/red_point.png";
</script>
<div class="blank20"></div>
<div class="page wrap_full">
	<div class="left_box">
		<?php echo $this->fetch('inc/biz_nav_list.html'); ?>
	</div>
	<div class="right_box">
		<div class="content">
			<div class="head_box clearfix">
				<h2 class="f_l"><?php echo $this->_var['page_title']; ?></h2>
				<div class="publish_project_btn f_r"><a href="<?php echo $this->_var['go_list_url']; ?>"><button class="ui-button " rel="white" type="button">返回列表</button></a></div>
			</div>
			<div class="blank20"></div>
			<div class="form_box">
				
				<form name="location_update_form" action="<?php
echo parse_url_tag("u:biz|location#do_update|"."".""); 
?>" method="post">
				<div class="publish_box ">

						<table class="form_teble_box add_border">
									<colgroup>
										<col width="120">
										<col width="570">
									</colgroup>
									<tbody>
										
										<tr>
											<td class="t_field_name">供应商标志图片:</td>
											<td class="t_field_value">
												<div class="preview_upbtn upload_btn_box">
													<button id="preview" class="ui-button preview_btn" rel="orange" type="button">图片上传</button>
												</div>
												<div class="preview_upload_box pub_upload_img_box">
													<?php if ($this->_var['vo']['preview']): ?>
													<span>
														<a href="javascript:void(0);"></a><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['vo']['preview'],
  'h' => '50',
  'w' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>">
														<input type="hidden" name="preview" value="<?php echo $this->_var['vo']['preview']; ?>">
													</span>
													<?php endif; ?>
												</div>
											</td>
										</tr>
										<tr >
											<td class="t_field_name">门店图库:</td>
											<td class="t_field_value">
												<div class="location_images_upbtn upload_btn_box">
												<button id="location_images" class="ui-button location_images_btn" rel="orange" type="button">图片上传</button>
												</div>
												<div class="location_images_upload_box pub_upload_img_box">
													<?php if ($this->_var['location_images']): ?>
														<?php $_from = $this->_var['location_images']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'img');if (count($_from)):
    foreach ($_from AS $this->_var['img']):
?>
															<span>
																<a href="javascript:void(0);" ></a><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img'],
  'h' => '50',
  'w' => '50',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>">
																<input type="hidden" name="location_images[]" value="<?php echo $this->_var['img']; ?>">
															</span>
														<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
													<?php endif; ?>
												</div>
											</td>
										</tr>
									
										<tr  >
											<td class="t_field_name ">地址:</td>
											<td class="t_field_value"><input class="ui-textbox long_input" name="address" value="<?php echo $this->_var['vo']['address']; ?>"/></td>
										</tr>	
										<tr >
											<td class="t_field_name">交通路线:</td>
											<td class="t_field_value">
												<textarea id="route" name="route" class="t_textarea"><?php echo $this->_var['vo']['route']; ?></textarea>
											</td>
										</tr>
										<tr >
											<td class="t_field_name ">联系电话:</td>
											<td class="t_field_value"><input class="ui-textbox " name="tel" value="<?php echo $this->_var['vo']['tel']; ?>"/></td>
										</tr>
										<tr >
											<td class="t_field_name ">联系人:</td>
											<td class="t_field_value"><input class="ui-textbox " name="contact" value="<?php echo $this->_var['vo']['contact']; ?>"/></td>
										</tr>	
										<tr >
											<td class="t_field_name ">营业时间:</td>
											<td class="t_field_value"><input class="ui-textbox " name="open_time" value="<?php echo $this->_var['vo']['open_time']; ?>"/></td>
										</tr>	
										<tr class="biz_map" >
									            <td class="t_field_name">地图定位</td>
									            <td class="t_field_value">            	
									            	<span class="f_l map_search_label">地图关键词：</span><input type="text" class="ui-textbox map_keyword f_l" name="api_address" value="<?php echo $this->_var['vo']['api_address']; ?>" /> 
													<button type="button"  class="ui-button f_l"  rel="white" name="search_api" id="search_api" >查找</button>
													<div style="height:10px; clear:both;"></div>
									                <div id="container"></div>
													<div style="height:10px; clear:both;"></div>
									                
									                <button type="button" class=" f_l"  rel="white" name="chang_api" id="chang_api">手动进行更精确定位</button>
									                <div style="position:relative; top:-400px;">
									                    <div  id="container_front">
									                        <a href="javascript:void(0);" id="cancel_btn">关闭&nbsp</a>
									                        <div id="container_m"></div>
									                        <span class="prompt">鼠标拖动蓝色标识进行定位</span>
									                    </div>
									                </div>
													<input type="hidden" name="xpoint" value="<?php echo $this->_var['vo']['xpoint']; ?>"/>
													<input type="hidden" name="ypoint" value="<?php echo $this->_var['vo']['ypoint']; ?>" />
									            </td>
									    </tr>
									    <tr >
											<td class="t_field_name">部门简介:</td>
											<td class="t_field_value">
												<textarea id="brief" name="brief"><?php echo $this->_var['vo']['brief']; ?></textarea>
											</td>
										</tr>
										<tr >
											<td class="t_field_name">门店顶部广告位:</td>
											<td class="t_field_value">
												<textarea id="adv_img_1" name="adv_img_1"><?php echo $this->_var['vo']['adv_img_1']; ?></textarea>
											</td>
										</tr>
										<tr >
											<td class="t_field_name">门店侧边广告位:</td>
											<td class="t_field_value">
												<textarea id="adv_img_2" name="adv_img_2"><?php echo $this->_var['vo']['adv_img_2']; ?></textarea>
											</td>
										</tr>
										<tr >
											<td class="t_field_name">客服QQ:</td>
											<td class="t_field_value"><input class="ui-textbox " name="location_qq" value="<?php echo $this->_var['vo']['location_qq']; ?>"/></td>
										</tr>
									    
									</tbody>
								</table>
						<div class="blank10"></div>
					</div>
					<div class="confirm_form_btn">
					<input type="hidden" name="id" value="<?php echo $this->_var['vo']['id']; ?>"/>
						<div class="sub_form_btn">
							<button class="ui-button " rel="orange" type="submit">确认提交</button>
						</div>
							
					</div>
				</form>
				<div class="blank10"></div>
			</div>
			<div class="blank10"></div>
		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/project.css";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.bgiframe.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.weebox.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.pngfix.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.animateToClass.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/utils/jquery.timer.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/fanwe_utils/fanweUI.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/script.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/pages/dc/dc_index.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/pages/dc/dc_index.js";
?>

<?php echo $this->fetch('inc/header.html'); ?>
<script>
var ajax_url = '<?php echo $this->_var['ajax_url']; ?>';
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

			</div>
			<div class="common_tip">
		               <span>注意：可以点击以上【宝贝分类】或【宝贝】可以进行添加和修改</span>
	            	</div>
			<div class="blank50"></div>
			<div class="form_box  content_hastab">
			
				<form name="project_form" action="<?php echo $this->_var['form_url']; ?>" method="post">
					<div class="comments_details">
	<table class="table_box ">
					<colgroup>
						<col width="90">
						<col width="320">
						<col width="250">
						<col width="100">
					</colgroup>
					<thead>
						<tr>
							<th>编号</th>
							<th>名称</th>
							<th>宝贝分类/宝贝设置</th>
							<th>操作</th>
						</tr>
					</thead>
					
					<tbody>
					<?php if ($this->_var['list']): ?>
					<?php $_from = $this->_var['list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
						<tr data-id="<?php echo $this->_var['row']['id']; ?>">
							<td class="rate">
								<?php echo $this->_var['row']['id']; ?>
							</td>
							<td>
								<div>
									<p class="rate" title="<?php echo $this->_var['row']['name']; ?>"><?php 
$k = array (
  'name' => 'msubstr',
  'v' => $this->_var['row']['name'],
  'l' => '0',
  'e' => '65',
);
echo $k['name']($k['v'],$k['l'],$k['e']);
?></p>
									<?php if ($this->_var['row']['preview']): ?>
										<ul class="photos_box clearfix">
												<li>
													<a href="<?php echo $this->_var['row']['preview']; ?>" target="_blank">
														<img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['row']['preview'],
  'h' => '40',
  'w' => '40',
  'g' => '1',
);
echo $k['name']($k['v'],$k['h'],$k['w'],$k['g']);
?>" lazy="true"/>
													</a>
												</li>
										</ul>
									<?php endif; ?>
									
								</div>
							</td>
							<td>
								<a href="<?php echo $this->_var['row']['menu_cate_url']; ?>">宝贝分类(<?php echo $this->_var['row']['menu_cate_count']; ?>)</a> &nbsp;&nbsp;
								<a href="<?php echo $this->_var['row']['menu_url']; ?>">宝贝(<?php echo $this->_var['row']['menu_count']; ?>)</a>
							</td>
							<td class="operate">
								<a href="<?php
echo parse_url_tag("u:biz|dc#dc_set|"."id=".$this->_var['row']['id']."".""); 
?>"><button class="ui-button down_btn" rel="white" type="button" >外卖预约设置</button></a>
								<div class="blank10"></div>
								<a href="<?php
echo parse_url_tag("u:biz|dc#dc_rsitem_index|"."id=".$this->_var['row']['id']."".""); 
?>"><button class="ui-button down_btn" rel="white" type="button" >预约项目设置</button></a>
								<div class="blank10"></div>
								<div class="is_close_box"><button class="ui-button is_close_btn" rel="white" type="button" data-id="<?php echo $this->_var['row']['id']; ?>" is_close="<?php echo $this->_var['row']['is_close']; ?>"><?php if ($this->_var['row']['is_close'] == 1): ?>恢复营业<?php else: ?>暂停营业<?php endif; ?></button></div>
								
							</td>
						</tr>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					<?php endif; ?>
					</tbody>
				</table>
	<div class="blank"></div>
	<div class="pages">
		<?php echo $this->_var['pages']; ?>
	</div>
</div>
		
				</form>
			</div>
		</div>
	</div>	
</div>

<div class="blank20"></div>
<?php echo $this->fetch('inc/footer.html'); ?>
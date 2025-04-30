<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/link.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
?>
<?php echo $this->fetch('inc/header.html'); ?> 
<script type="text/javascript" >
$(document).ready(function(){	
	$(".flink").find("a").bind("click",function(){
		var click_url='<?php echo $this->_var['click_url']; ?>';
		var query= new Object();
		query.url=$(this).attr('click_url');		
		$.ajax({ 
			url: click_url,
			data:query,
			type: "POST",
			success: function(html){
				
			}
		});			
	});
});
</script>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?>">
	<div class="blank"></div>	
	<div class="inc">
		<div class="article_top"><h3><span><?php echo $this->_var['page_title']; ?></span></h3></div>		
		<div class="blank20"></div>
		<div class="inc_main pd10">
				<div class="flink">
							<?php $_from = $this->_var['p_link_data']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'link_group');if (count($_from)):
    foreach ($_from AS $this->_var['link_group']):
?>			
								<h2><?php echo $this->_var['link_group']['name']; ?></h2>
								<?php $_from = $this->_var['link_group']['links']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'link');if (count($_from)):
    foreach ($_from AS $this->_var['link']):
?>
									<a href="http://<?php echo $this->_var['link']['url']; ?>" target="_blank" title="<?php if ($this->_var['link']['description']): ?><?php echo $this->_var['link']['description']; ?><?php else: ?><?php echo $this->_var['link']['name']; ?><?php endif; ?>" click_url="<?php echo $this->_var['link']['url']; ?>"><?php if ($this->_var['link']['img'] != ''): ?><img src='<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['link']['img'],
  'w' => '100',
  'h' => '36',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>' alt="<?php if ($this->_var['link']['description']): ?><?php echo $this->_var['link']['description']; ?><?php else: ?><?php echo $this->_var['link']['name']; ?><?php endif; ?>" /><?php else: ?><?php echo $this->_var['link']['name']; ?><?php endif; ?></a>
								<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
								<div class="blank"></div>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
				</div>
				<div class="blank"></div>

		</div><!--end inc_main-->		
		
	</div>
	<div class="blank"></div>
</div>
<?php echo $this->fetch('inc/footer.html'); ?>
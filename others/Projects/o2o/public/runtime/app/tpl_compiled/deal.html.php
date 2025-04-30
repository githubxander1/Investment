<?php
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/style.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/weebox.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/utils/fanweUI.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/deal.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/side_deal_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/business_address.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/sort_row.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/review_list.css";
$this->_var['pagecss'][] = $this->_var['TMPL_REAL']."/css/relate_goods.css";

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
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/login_panel.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/cart.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/cart.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/user.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/business_address.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/business_address.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/side_deal_list.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/side_deal_list.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/review_list.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/review_list.js";
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/deal.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/deal.js";

$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/relate_goods.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/relate_goods.js";

if(defined("FX_LEVEL"))
{
$this->_var['pagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_fx_deal_fx.js";
$this->_var['cpagejs'][] = $this->_var['TMPL_REAL']."/js/page_js/uc/uc_fx_deal_fx.js";
}

?>
<?php echo $this->fetch('inc/header.html'); ?>
<?php if(defined("FX_LEVEL")){ ?>
<script>
    var ajax_url = '<?php
echo parse_url_tag("u:index|uc_fx|"."".""); 
?>';
</script>
<?php }?>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=<?php 
$k = array (
  'name' => 'app_conf',
  'v' => 'BAIDU_MAP_APPKEY',
);
echo $k['name']($k['v']);
?>"></script> 
<div class="blank"></div>
<div class="<?php 
$k = array (
  'name' => 'load_wrap',
  't' => $this->_var['wrap_type'],
);
echo $k['name']($k['t']);
?> clearfix">
	<div class="deal_introduce clearfix border">
	    	<h1 class="title"><?php echo $this->_var['deal']['sub_name']; ?></h1>
	    	<p class="details ">
				<?php echo $this->_var['deal']['name']; ?>
				
			</p>
			<div class="kf_qq_box">
			<?php if ($this->_var['deal']['location_qqs']): ?>
				<div class="s_kf_qq">
					<ul>
						<?php $_from = $this->_var['deal']['location_qqs']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'row');if (count($_from)):
    foreach ($_from AS $this->_var['row']):
?>
						<?php if ($this->_var['row']['location_qq']): ?>
							<li><a href="http://wpa.qq.com/msgrd?v=3&uin=<?php echo $this->_var['row']['location_qq']; ?>&site=qq&menu=yes" title="<?php echo $this->_var['row']['name']; ?>"><i class="iconfont">&#xe64a;</i>客服QQ</a></li>
						<?php endif; ?>
						<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					</ul>
				</div>
				<?php endif; ?>
			</div>
			<div class="component clearfix">
				<div class="component_left f_l">
					<div class="big_pic">
						<div class="tags">					
							<?php $_from = $this->_var['deal']['deal_tags']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'tag');if (count($_from)):
    foreach ($_from AS $this->_var['tag']):
?>				
							<h2 class="tag<?php echo $this->_var['tag']; ?>"></h2>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							<?php if ($this->_var['deal']['buyin_app'] == 1): ?>
							<h2 class="tag_buyinapp"></h2>
							<?php endif; ?>
						</div>
						<img id="big_pic" src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['deal']['icon'],
  'w' => '460',
  'h' => '280',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" alt="<?php echo $this->_var['deal']['sub_name']; ?>" origin="<?php echo $this->_var['deal']['icon']; ?>" width="460" height="280">
					</div>
					<?php if ($this->_var['deal']['image_list']): ?>
					<div class="pic_hidden">
						<div class="small_pic word" id="small_pic">
							<?php $_from = $this->_var['deal']['image_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'img');if (count($_from)):
    foreach ($_from AS $this->_var['img']):
?>
							<a href="javascript:void(0);" <?php if ($this->_var['img']['current'] == 1): ?>class="active"<?php endif; ?>><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img']['img'],
  'w' => '78',
  'h' => '45',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" big_pic="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['img']['img'],
  'w' => '460',
  'h' => '280',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" origin="<?php echo $this->_var['img']['img']; ?>" lazy="true" width="78" height="45"></a>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
							<!--当前用active标示-->
					    </div>
						<?php if (count ( $this->_var['deal']['image_list'] ) > 5): ?>
					    <a href="javascript:void(0);" class="pre hide_tag"></a> 
						<a href="javascript:void(0);" class="next hide_tag"></a> 
						<?php endif; ?>
					</div>
					<?php endif; ?>
					
				</div>
				<div class="component_rigth f_r" id="main_package_choose">
					<div class="component_price clearfix">
						<div class="base_info f_l">
							<h2><?php if ($this->_var['deal']['buy_type'] != 1): ?>¥<?php else: ?><span>所需积分</span><?php endif; ?><strong id="deal_price"><?php if ($this->_var['deal']['buy_type'] != 1): ?><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['current_price'],
  'p' => '2',
);
echo $k['name']($k['v'],$k['p']);
?><?php else: ?><?php 
$k = array (
  'name' => 'abs',
  'v' => $this->_var['deal']['return_score'],
);
echo $k['name']($k['v']);
?><?php endif; ?></strong></h2>
							<?php if ($this->_var['deal']['buy_type'] != 1): ?>
							<div class="f_l">
							<span class="discount"><?php echo $this->_var['deal']['discount']; ?>折</span>
							<del class="item">¥ <?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['origin_price'],
  'p' => '2',
);
echo $k['name']($k['v'],$k['p']);
?></del>
							</div>
							<?php endif; ?>
						</div>
						<?php if (( $this->_var['deal']['begin_time'] != 0 && $this->_var['deal']['time_status'] == 3 ) || ( $this->_var['deal']['end_time'] != 0 && $this->_var['deal']['time_status'] == 1 )): ?>						
						<div 
							class="countdown f_r" 
							id="countdown" 
							nowtime="<?php echo $this->_var['NOW_TIME']; ?>000" 
							<?php if ($this->_var['deal']['begin_time'] != 0 && $this->_var['deal']['time_status'] == 3): ?>
							endtime="<?php echo $this->_var['deal']['begin_time']; ?>000" showtitle="距离开始：" 
							<?php endif; ?>
							<?php if ($this->_var['deal']['end_time'] != 0 && $this->_var['deal']['time_status'] == 1): ?>
							endtime="<?php echo $this->_var['deal']['end_time']; ?>000" showtitle="距离结束：" 
							<?php endif; ?>
						></div><!--倒计时-->
						<?php endif; ?>
					</div>
					<div class="component_rating clearfix" >
					     <ul>
					     	<li class="first f_l">
					     		<span>已售</span>
								<strong><?php echo $this->_var['deal']['buy_count']; ?></strong>
					     	</li>
							<li class="f_l">
								<strong><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['deal']['avg_point'],
  'p' => '1',
);
echo $k['name']($k['v'],$k['p']);
?></strong>
					     		<span>分</span>
							</li>
							<li class="f_r last">
					     		<strong><?php echo $this->_var['deal']['dp_count']; ?></strong>
					     		<span>人评价</span>
					     	</li>
							</ul>
					</div>
					<div class="hangtag">
						<ul>
							<?php if ($this->_var['deal']['supplier_info']): ?>
							<li class="clearfix">
								<span class="tag f_l">商家</span>
								<div class="width f_l">
									<a href="<?php echo $this->_var['deal']['supplier_info']['url']; ?>"><?php echo $this->_var['deal']['supplier_info']['name']; ?></a>
									<?php if ($this->_var['deal']['supplier_location_count'] > 0 && $this->_var['deal']['is_shop'] == 0): ?>
									<span class="cross">|</span>
									<a href="javascript:void(0);" id="show_store"><?php echo $this->_var['deal']['supplier_location_count']; ?>店通用</a>
									<?php endif; ?>
								</div>
							</li>
							<?php endif; ?>
							<?php if ($this->_var['deal']['brand_info']): ?>
							<li class="clearfix">
								<span class="tag f_l">品牌</span>
								<div class="width f_l">
									<a href="<?php
echo parse_url_tag("u:index|cate|"."cid=".$this->_var['deal']['shop_cate_id']."&bid=".$this->_var['deal']['brand_info']['id']."".""); 
?>"><?php echo $this->_var['deal']['brand_info']['name']; ?></a>
								</div>
							</li>
							<?php endif; ?>
							<?php if ($this->_var['deal']['is_coupon'] == 1): ?>
							<li class="clearfix">
								<span class="tag f_l">团购券</span>
								<div class="width f_l">
								    <span>
								    <?php if ($this->_var['deal']['coupon_time_type'] == 0): ?>
									
									<?php if ($this->_var['deal']['coupon_begin_time'] > 0 && $this->_var['NOW_TIME'] < $this->_var['deal']['coupon_begin_time'] && $this->_var['deal']['coupon_end_time'] > 0): ?>
									<?php echo $this->_var['deal']['coupon_begin_time_format']; ?>至<?php echo $this->_var['deal']['coupon_end_time_format']; ?>有效
									<?php endif; ?>
									<?php if ($this->_var['deal']['coupon_begin_time'] > 0 && $this->_var['NOW_TIME'] < $this->_var['deal']['coupon_begin_time'] && $this->_var['deal']['coupon_end_time'] == 0): ?>
									<?php echo $this->_var['deal']['coupon_begin_time_format']; ?>后有效
									<?php endif; ?>
									<?php if ($this->_var['NOW_TIME'] > $this->_var['deal']['coupon_begin_time'] && $this->_var['deal']['coupon_end_time'] > 0): ?>
									<?php echo $this->_var['deal']['coupon_end_time_format']; ?>前有效
									<?php endif; ?>
									<?php if ($this->_var['NOW_TIME'] > $this->_var['deal']['coupon_begin_time'] && $this->_var['deal']['coupon_end_time'] == 0): ?>
									永久有效
									<?php endif; ?>
									
									<?php else: ?>
									<?php echo $this->_var['deal']['coupon_day']; ?>天内有效
									<?php endif; ?>
									
									</span>
								</div>
							</li>
							<?php endif; ?>
						</ul>
					</div>
					<?php if ($this->_var['deal']['deal_attr']): ?>
					<?php $_from = $this->_var['deal']['deal_attr']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'deal_attr_type');if (count($_from)):
    foreach ($_from AS $this->_var['deal_attr_type']):
?>
					<?php if ($this->_var['deal_attr_type']['attr_list']): ?>
					<div class="package_choose clearfix " rel="<?php echo $this->_var['deal_attr_type']['id']; ?>">
						<span class="info_title f_l"><?php echo $this->_var['deal_attr_type']['name']; ?></span>
						<div class="choose f_r clearfix active_parent">
							<?php $_from = $this->_var['deal_attr_type']['attr_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'attr_item');if (count($_from)):
    foreach ($_from AS $this->_var['attr_item']):
?>
							<a href="javascript:void(0);" rel="<?php echo $this->_var['attr_item']['id']; ?>" price="<?php echo $this->_var['attr_item']['price']; ?>">
								<?php echo $this->_var['attr_item']['name']; ?>
								<i class="iconfont">&#xe620;</i>
							</a>
							<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>							
						</div>
					</div>
					<?php endif; ?>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					<?php endif; ?>
					<script type="text/javascript">
						var deal_price = <?php echo $this->_var['deal']['current_price']; ?>;  //商品的基础价格
						var deal_stock = <?php echo $this->_var['deal']['max_bought']; ?>;   //原始库存
						var deal_buy_count = <?php echo $this->_var['deal']['buy_count']; ?>;  //销量						
						var deal_user_min_bought = <?php echo $this->_var['deal']['user_min_bought']; ?>;  //会员最小购买
						var deal_user_max_bought = <?php echo $this->_var['deal']['user_max_bought']; ?>;	 //会员最大购买						
						var deal_attr_stock_json = <?php echo $this->_var['deal']['deal_attr_stock_json']; ?>;						
						var buy_type = <?php echo $this->_var['deal']['buy_type']; ?>;  //购物类型
						var deal_id = <?php echo $this->_var['deal']['id']; ?>;
					</script>
					<?php if ($this->_var['deal']['time_status'] == 1): ?>
					<div class="num_choose clearfix">
						      <span class="info_title f_l">数量</span>
							  <div class="f_l">
							  	  <a href="javascript:void(0);" class="less">−</a>
								  <input type="text"  name="q" value="1" maxlength="9" class="change_box" id="deal_num" />
								  <a href="javascript:void(0);" class="increase">+</a>
							  </div>
							  <span class="total f_l" id="stock_span">
							  	<div>还剩<span class="inventory">0</span>份</div>
							  </span>
							  <span class="tips f_l none" id="stock_tips"></span><!--当数量超出库存时，此项显示-->
                    </div>
					<?php endif; ?>
					<?php if (! $this->_var['preview']): ?>
					<div class="roduct_button clearfix">
						<?php if ($this->_var['deal']['time_status'] == 3): ?>
						<button class="ui-button disabled f_l" rel="disabled" type="button">未开始</button><!--disabled-->
						<?php endif; ?>
						<?php if ($this->_var['deal']['time_status'] == 1): ?>							
						<button <?php if ($this->_var['deal']['buyin_app'] == 1): ?>style="display:none;"<?php endif; ?> class="ui-button disabled f_l" rel="disabled" type="button" id="buy_btn"><?php if ($this->_var['deal']['buy_type'] == 1): ?>立即兑换<?php else: ?>立即购买<?php endif; ?></button><!--disabled-->
						<?php endif; ?>
						<?php if ($this->_var['deal']['time_status'] == 2): ?>
						<button class="ui-button disabled f_l" rel="disabled" type="button">已过期</button><!--disabled-->
						<?php endif; ?>
						
						<?php if(defined("FX_LEVEL")){ ?>
						<?php if ($this->_var['deal']['is_fx'] == 2): ?>
						<button class="ui-button blue f_l" rel="blue" type="button" onclick="add_user_deal_fx(<?php echo $this->_var['deal']['id']; ?>)">我要分销</button>
						<a class="f_l collect_ico" id="add_collect" href="javascript:void(0);">
							<i class="iconfont">&#xe649;</i>
							<span>收藏</span>
						</a>
						<?php else: ?>
						<button class="ui-button blue f_l" rel="blue" type="button"  id="add_collect">收藏本单</button>
						<?php endif; ?>
						<?php }else{ ?>
						<button class="ui-button blue f_l" rel="blue" type="button"  id="add_collect">收藏本单</button>
						<?php }?>
							
						<div class="f_r share_to">
						<!-- JiaThis Button BEGIN -->
						<div class="jiathis_style">
							<span class="jiathis_txt">分享到：</span>
							<a href="http://www.jiathis.com/share" class="jiathis jiathis_txt jtico jtico_jiathis" target="_blank"></a>
							<a class="jiathis_counter_style"></a>
						</div>
						<script type="text/javascript">
							 var jiathis_config = {
							 	title:"<?php echo $this->_var['deal']['name']; ?>",
							    url:"<?php echo $this->_var['deal']['share_url']; ?>"
							    
							};
						</script>
						<script type="text/javascript" src="http://v3.jiathis.com/code/jia.js" charset="utf-8"></script>
						
						<!-- JiaThis Button END -->
						
						</div>	
					</div>
					<?php endif; ?>

					<?php if ($this->_var['promote']): ?>
					<div class="blank"></div>
					<div class="promote_list">
					<?php $_from = $this->_var['promote']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'promote_item');if (count($_from)):
    foreach ($_from AS $this->_var['promote_item']):
?>
					<div class="item"><?php echo $this->_var['promote_item']['description']; ?></div>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					</div>
					<?php endif; ?>
					
					<?php if ($this->_var['deal']['buyin_app'] == 1): ?>
					<div class="blank"></div>
					<span class="app_tip">
					本单仅限移动APP端下单购买  &nbsp;&nbsp;
					<span class="ios"><a href="javascript:void(0);"  down_url="<?php
echo parse_url_tag("u:index|ajax#app_download|"."t=ios".""); 
?>" ><i class="iconfont">&#xe614;</i>IOS应用下载</a></span>
					&nbsp;
					<span class="android"><a href="javascript:void(0);"  down_url="<?php
echo parse_url_tag("u:index|ajax#app_download|"."t=android".""); 
?>" ><i class="iconfont">&#xe613;</i>安卓应用下载</a></span>
					</span>
					<?php endif; ?>
				</div>
			</div>
		</div><!--end deal_introduce-->
		<div class="blank"></div>
		
		<div class="clearfix">
        	
            <!--合并购买-->
			<div id="relate_goods" deal_id="<?php echo $this->_var['deal']['id']; ?>" supplier_id="<?php echo $this->_var['deal']['supplier_id']; ?>" supplier_name="<?php echo $this->_var['deal']['supplier_info']['name']; ?>"></div>
            
			<div class="wrap_m2 f_l">
            
			<?php if ($this->_var['deal']['is_shop'] == 0 && ! $this->_var['preview']): ?>
			<div id="supplier_deal" deal_id="<?php echo $this->_var['deal']['id']; ?>" supplier_id="<?php echo $this->_var['deal']['supplier_id']; ?>" supplier_name="<?php echo $this->_var['deal']['supplier_info']['name']; ?>">
			</div>
			<?php endif; ?>
			
			<!--详情导航-->
			<div class="show-nav" id="rel_nav">
			<!--{start: 详情导航 -->
			<ul>
				<?php if ($this->_var['deal']['is_shop'] == 0 && $this->_var['deal']['supplier_info'] && $this->_var['deal']['supplier_location_count'] > 0): ?>
				<li rel="n0">商家位置</li>
				<?php endif; ?>
				<?php if ($this->_var['deal']['notes']): ?>
				<li rel="n1">购买需知</li>
				<?php endif; ?>
				<?php if ($this->_var['deal']['description']): ?>
				<li rel="n2">本单详细</li>
				<?php endif; ?>
				<?php if (! $this->_var['preview']): ?>
				<li rel="n3">消费评价</li>
				<?php endif; ?>
			
			</ul>
			<!--}end: 详情导航 -->
			</div>
			<div style="display:none;" class="fix-nav wrap_m2">
				<!--{start: 浮动导航 -->
				<div class="show-nav">
					<!--{start: 详情导航 -->
					<ul class="f_l">
						<?php if ($this->_var['deal']['is_shop'] == 0 && $this->_var['deal']['supplier_info'] && $this->_var['deal']['supplier_location_count'] > 0): ?>
						<li rel="n0">商家位置</li>
						<?php endif; ?>
						<?php if ($this->_var['deal']['notes']): ?>
						<li rel="n1">购买需知</li>
						<?php endif; ?>
						<?php if ($this->_var['deal']['description']): ?>
						<li rel="n2">本单详细</li>
						<?php endif; ?>
						<?php if (! $this->_var['preview']): ?>
						<li rel="n3">消费评价</li>
						<?php endif; ?>
					</ul>
					<?php if (! $this->_var['preview']): ?>
					<button class="ui-button flow_btn" id="flow_btn" rel="white"><?php if ($this->_var['deal']['buy_type'] == 1): ?>立即兑换<?php else: ?>立即购买<?php endif; ?></button>
					<?php endif; ?>
					<!--}end: 详情导航 -->
				</div>
				<!--}end: 浮动导航 -->
			</div>
			<!--end 详情导航-->
			<div class="show-content">
				<?php if ($this->_var['deal']['is_shop'] == 0 && $this->_var['deal']['supplier_info'] && $this->_var['deal']['supplier_location_count'] > 0): ?>
				<div rel="n0" class="content_box">
					<div class="box_title nomargin">商家位置</div>
					<div class="box_content nopadding">
 						<div id="business_address" deal_id="<?php echo $this->_var['deal']['id']; ?>" supplier_id="<?php echo $this->_var['deal']['supplier_id']; ?>">
						
						</div>
					</div>
				</div>
				<?php endif; ?>
				<?php if ($this->_var['deal']['notes']): ?>
				<div rel="n1" class="content_box">
					<div class="box_title">购买需知</div>
					<div class="box_content">
						<?php echo $this->_var['deal']['notes']; ?>
					</div>
				</div>
				<?php endif; ?>
				<?php if ($this->_var['deal']['description']): ?>
				<div rel="n2" class="content_box">
					<div class="box_title">本单详细</div>
					<div class="box_content">
						<?php echo $this->_var['deal']['description']; ?>
					</div>
				</div>
				<?php endif; ?>
				<?php if (! $this->_var['preview']): ?>
				<div rel="n3" class="content_box">
					<div class="box_title">
						<div class="box_title_text">消费评价</div>
						<div class="box_title_more">我买过本单，<a href="<?php
echo parse_url_tag("u:index|review|"."deal_id=".$this->_var['deal']['id']."".""); 
?>" target="_blank">我要评价</a></div>
					</div>
					<div class="box_content">
						<div id="review_list" deal_id="<?php echo $this->_var['deal']['id']; ?>">
						</div>
					</div>
				</div>
				<?php endif; ?>
				<div class="content_box"></div>
			</div>
		</div><!--end wrap_m2-->
		<div class="wrap_s2 f_r">
			<?php if ($this->_var['side_deal_list']): ?>
			<div class="side_deal_box">
			<div class="title_row">
				<span>您可能喜欢的</span>
				<a href="javascript:void(0);" class="change_favdeal" deal_id="<?php echo $this->_var['deal']['id']; ?>"><i class="iconfont">&#xe624;</i>换一批</a>
			</div>
			<div class="content_row" id="favdeal_list">
				<?php echo $this->fetch('inc/side_favdeal_list.html'); ?>
			</div>
			</div>
			<div class="blank"></div>
			<?php endif; ?>
			
			<?php if ($this->_var['history_deal_list']): ?>
			<div class="side_deal_box">
			<div class="title_row">
				<span>浏览历史</span>
				<a href="javascript:void(0);" class="clear_history" <?php if ($this->_var['deal']['is_shop'] == 0): ?>type="deal"<?php else: ?>type="shop"<?php endif; ?>>清空</a>
			</div>
			<div class="content_row">
				<ul class="side_deal_list">
					<?php $_from = $this->_var['history_deal_list']; if (!is_array($_from) && !is_object($_from)) { settype($_from, 'array'); }; $this->push_vars('', 'side_deal');if (count($_from)):
    foreach ($_from AS $this->_var['side_deal']):
?>
					<li>
						<a href="<?php echo $this->_var['side_deal']['url']; ?>" class="deal_img"><img src="<?php 
$k = array (
  'name' => 'get_spec_image',
  'v' => $this->_var['side_deal']['icon'],
  'w' => '198',
  'h' => '134',
  'g' => '1',
);
echo $k['name']($k['v'],$k['w'],$k['h'],$k['g']);
?>" lazy="true" /></a>
						<a href="<?php echo $this->_var['side_deal']['url']; ?>"  class="deal_title"><?php echo $this->_var['side_deal']['sub_name']; ?></a>
						<div class="deal_info">
							<span class="deal_price f_l">
								<span class="current_price"><i>&yen;</i><?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['side_deal']['current_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
								<span class="origin_price">&yen;<?php 
$k = array (
  'name' => 'round',
  'v' => $this->_var['side_deal']['origin_price'],
  'l' => '2',
);
echo $k['name']($k['v'],$k['l']);
?></span>
							</span>
							<span class="sale_count f_r">
								已售<span><?php echo $this->_var['side_deal']['buy_count']; ?></span>
							</span>
						</div>
					</li>
					<?php endforeach; endif; unset($_from); ?><?php $this->pop_vars();; ?>
					
				</ul>
			</div>
			</div>
			<?php endif; ?>
		</div>
		</div>

</div>
<div class="blank20"></div>

<?php echo $this->fetch('inc/footer.html'); ?>
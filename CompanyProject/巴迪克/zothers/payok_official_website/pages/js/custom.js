(function ($) {

  "use strict";
  let wy_https_root = window.location.origin+'/api-email/'
  // let wy_https_root = "http://192.168.0.171:9875/api-email/"
  let iti = '';

    // PRE LOADER
    $(window).load(function(){
      const input = document.querySelector("#phone");

      try {
        iti = window.intlTelInput(input, {
          initialCountry: "auto",

          formatOnDisplay: true,
          geoIpLookup: function(callback) {
            $.get('https://ipinfo.io', function() {}, "jsonp").always(function(resp) {
              var countryCode = (resp && resp.country) ? resp.country : "ID";
              callback(countryCode);
            });
          },
          utilsScript: "utils.js" // just for formatting/placeholders etc
        });
      }catch (e) {

      }

      
      // 轮播图动画控制
      let currentSlide = 0;
      const slides = $('.banner-slide');
      const indicators = $('.indicator');
      const totalSlides = slides.length;
      
      // 初始化显示第一个轮播
      slides.eq(0).addClass('active');
      
      // 点击指示器切换轮播
      indicators.on('click', function() {
        const index = $(this).index();
        if (index !== currentSlide) {
          goToSlide(index);
        }
      });
      
      // 切换到指定轮播
      function goToSlide(index) {
        // 移除当前轮播的active类
        slides.eq(currentSlide).removeClass('active');
        indicators.eq(currentSlide).removeClass('active');
        
        // 添加新轮播的active类
        slides.eq(index).addClass('active');
        indicators.eq(index).addClass('active');
        
        // 重置动画
        resetAnimations(index);
        
        // 更新当前轮播索引
        currentSlide = index;
      }
      
      // 重置动画
      function resetAnimations(index) {
        // 获取当前轮播中的元素
        const currentSlideElements = slides.eq(index).find('.banner-image-ipad, .banner-image-phone, .decoration-left, .decoration-right');
        
        // 移除并重新添加动画类以重新触发动画
        currentSlideElements.each(function() {
          const element = $(this);
          const animationName = element.css('animation-name');
          const animationDuration = element.css('animation-duration');
          const animationDelay = element.css('animation-delay');
          
          element.css('animation', 'none');
          
          // 强制重绘
          element[0].offsetHeight;
          
          // 恢复动画
          element.css('animation', '');
        });
      }
      
      // 自动轮播（可选）
      // setInterval(function() {
      //   const nextSlide = (currentSlide + 1) % totalSlides;
      //   goToSlide(nextSlide);
      // }, 5000);
      
      /*const lang = {
        en: 'English',
        id: 'Bahasa',
        os: 'Türkçe ',
        in: 'हिन्दी',
        vn: 'Tiếng Việt'
      }*/
      const lang = {
        en: 'EN',
        tr: 'TR ',
        id: 'ID',
        br: 'BR',
        vn: 'VN',
        bd: 'BD',
        th: 'TH',
        in: 'IN'
      }
      $('.preloader').fadeOut(1000); // set duration in brackets

      // $("#header").load("../src/partials/header.html","",function(){
      //   $('.custom-navbar .navbar-toggle').on('click',function(){
      //     $(".js_mainBody").toggleClass("frame_mainBody_Open")
      //     // $('.custom-navbar').toggleClass('bg-white')
      //   })

      //   $("#langChange").on('click', function() {
      //     $(".navbar-right .sub-menu").attr('opacity', '1')
      //     $(".m-country-select").show()
      //   })

      //   //change lang
      //   $(".lang").on('change', function () {
      //       sessionStorage.setItem("lang", $(this).val());
      //       loadProperties($(this).val());
      //   });
      //   // mobile
      //   $("#langLiM").on('click', function () {
      //     $(this).find('.sub-menu').toggleClass('m-show-country')
      //   })
      //   $("#langLiM .sub-menu li").on('click', function () {
      //     let langShort = $(this).attr('langval')
      //     $(".langText").text(lang[langShort]);
      //     sessionStorage.setItem("lang", $(this).attr('langval'));
      //     loadProperties($(this).attr('langval'));
      //     $(this).addClass('active').siblings().removeClass('active')
      //   });
      //   // pc
      //   $("#langLi .sub-menu li").on('click', function () {
      //     let langShort = $(this).attr('langval')
      //     $(".langText").text(lang[langShort]);
      //     sessionStorage.setItem("lang", $(this).attr('langval'));
      //     loadProperties($(this).attr('langval'));
      //   });
      //   // let langShort = sessionStorage.getItem("lang");
      //   // $("#langLi .sub-menu li[langval='"+langShort+"']").addClass('active').siblings().removeClass('active')

      //   var currPage= $("#header").attr("pg-name");
      //   $(".main-menu li[id='"+currPage+"']").addClass("menu-active");
      //   $("#header [data-locale]").addClass("v-visible");
      //   // $(".main-menu li").click(function () {
      //   //     $(this).addClass("active")
      //   // })
        
      // })

      // import mobile menu
      $("#mobileMenu").load("../src/partials/menu.html","",function(){
        
        // mobile menu
        var closeMenu = $(".js_offCanvas_close, .js_offCanvas_mask");
        var i = $(".js_mainBody");
        closeMenu.on("click",(function(e){
          i.toggleClass("frame_mainBody_Open")
        })),
        $(".frame_offCanvas_multiNav_item_link, .frame_offCanvas_multiNav_sub_item").on("click",(function(e){i.toggleClass("frame_mainBody_Open")}))

        $(".m-country-text").on('click', function() {
          $("#mobileMenu .m-country .sub-menu").toggleClass('m-show-country')
        })
        
        $("#langLi .sub-menu li").on('click', function () {
          let langShort = $(this).attr('langval')
          $(".langText").text(lang[langShort]);
          sessionStorage.setItem("lang", $(this).attr('langval'));
          loadProperties($(this).attr('langval'));
          $("#mobileMenu .m-country .sub-menu").toggleClass('m-show-country')
          $(this).addClass('active').siblings().removeClass('active')
          $(".js_mainBody").toggleClass("frame_mainBody_Open")
          loadProperties($(this).attr('langval'));
        });
        let langShort = sessionStorage.getItem("lang");
        var currLang=  $("#langLi .sub-menu li[langval='"+langShort+"']");
        $("#langLi .langText").text(lang[langShort]);
        currLang.addClass('active').siblings().removeClass('active')

        $("#mobileMenu [data-locale]").addClass("v-visible");
      })

      // import footer
      $("#pcFooter").load("../src/partials/footerNew.html","",function () {
        $("#faTG").on('mouseenter', function () {
          $(".social-tg-qr").removeClass("social-d-none");
        }).on('mouseleave', function () {
          $(".social-tg-qr").addClass("social-d-none");
        });
        $("#pcFooter [data-locale]").addClass("v-visible");
      })

      // add
      $("#mobileFooter").load("../src/partials/m-footer.html")
      $("#mobileFooter [data-locale]").addClass("v-visible");

    //  $("#meetFooter").load("../src/partials/meet.html","",function () {
    //      $("#closeMeet").click(function () {
    //        $("#bookMeet").removeClass("fade-show-in");
    //        $("#bookMeet").addClass("fade-close-out");
    //      })
    //      $("#btnBookMeet").click(function () {
    //        $("#meetModal").modal({ backdrop: "static", keyboard: false });
    //      })

    //     $("#dateItem button").click(function () {
    //          $(this).siblings().removeClass("active");
    //          $(this).addClass("active");
    //     })

    //     $("#timeItem button").click(function () {
    //       $(this).siblings().removeClass("active");
    //       $(this).addClass("active");
    //     })

    //     $("#btnModalBack").click(function () {
    //       $("#meetModal1").removeClass("d-none");
    //       $("#meetModal2").addClass("d-none");
    //     })

    //     $("#btnModalNext").click(function () {
    //       $("#meetModal1").addClass("d-none");
    //       $("#meetModal2").removeClass("d-none");
    //     })

    //     // 切换模式
    //     $("#meetModal .modal-tabs button").click(function () {
    //       $(this).addClass("active").siblings().removeClass("active");
    //       if($(this).attr("data-event") == "IFX") {
    //         $(".ifx-info").removeClass("d-none");
    //         $(".ice-info").addClass("d-none");
    //         $("#dateItem .btn-d-item").removeClass("active");
    //         $("#dateItem .ifx-info .btn-d-item").eq(0).addClass("active");
    //       } else {
    //         $(".ifx-info").addClass("d-none");
    //         $(".ice-info").removeClass("d-none");
    //         $("#dateItem .btn-d-item").removeClass("active");
    //         $("#dateItem .ice-info .btn-d-item").eq(0).addClass("active");
    //       }
    //     })

    //     let modalValidCode= "";
    //     /**
    //      * Modal Send Email
    //      * @returns
    //      */
    //     function getInputParamByModal(){
    //       var name= $("#modalName").val()
    //       var email= $("#modalEmail").val()
    //       var phone= $("#modalPhone").val()
    //       var message= $("#modalMessage").val()
    //       var date= $("#dateItem button[class*='active']").attr("data-value");
    //       var time= $("#timeItem button[class*='active']").attr("data-value");
    //       var subject = $("#meetModal .modal-tabs button[class*='active']").attr("name");
    //       var contactType = ''
    //       let arr = []
    //       $('input[name="modalPrefer"]:checked').each(function(index, element) {
    //         arr.push($(this).val())
    //       })
    //       contactType = arr.join(',')
    //       var params={
    //         name: name,
    //         email: email,
    //         phone: phone,
    //         message: message,
    //         validCode: modalValidCode,
    //         contactType: contactType,
    //         date: date,
    //         time: time,
    //         subject: subject//"PAYOK"
    //       }

    //       return params
    //     }

    //     function validEmptyByModal() {
    //       var dom= $("#send-form");
    //       var flag = true
    //       for (let index = 0; index < dom.find('.require').length; index++) {
    //         let val = dom.find('.require').eq(index).val()
    //         if (val.trim() == '') {
    //           flag = false
    //           alert('Please fill out the form.')
    //           return
    //         }
    //       }
    //       return flag
    //     }

    //     function emptyFormByModal() {
    //       $("#send-form").find('input[type="text"]').val('')
    //       $("#send-form").find('input[type="tel"]').val('')
    //       $("#send-form").find('input[type="email"]').val('')
    //       $("#send-form").find('input[type="checkbox"]').prop('checked',false)
    //       $("#send-form").find('textarea').val('')
    //       // $(".prefer")
    //     }
    //     /**
    //      * Easy event listener function
    //      */
    //     sendEmailByModal();
    //     function sendEmailByModal(){
    //       $("#btnModalSubmit").click(function () {
    //         // if(validCode == "") return;
    //         if(!validEmptyByModal()) {
    //           // alert('Please fill out the form.')
    //           return
    //         };
    //         $("#btnModalSubmit").prop("disabled",true)
    //         var reqParam= getInputParamByModal()
    //         reqParam.validCode= modalValidCode

    //         $.ajax({
    //           type: "post",
    //           contentType: 'application/x-www-form-urlencoded',
    //           url: wy_https_root + "email/send",
    //           datatype: "json",
    //           data: reqParam,
    //           success: function (res) {
    //             if(res.code == 0){
    //               // emptyFormByModal();
    //               alert('Send successfully!')
    //               // window.location.reload()
    //             }else{
    //               alert('Sending failed. Please try again later!')
    //               // window.location.reload()
    //             }
    //           },complete: function () {
    //             setTimeout(function () {
    //               emptyFormByModal();
    //               swipeVerifyCodeByModal();
    //               $("#btnModalSubmit").prop("disabled",false)
    //             },2000)
    //           }
    //         });
    //       })

    //       swipeVerifyCodeByModal();
    //       /**
    //        * verify code
    //        */
    //       function swipeVerifyCodeByModal(){
    //         modalValidCode=""
    //         $('#mpanel3').html('')
    //         $('#mpanel3').slideVerify({
    //           type : 1,       //type
    //           vOffset : 5,
    //           currTab: "btnLogin",
    //           barText: $.i18n.prop("slidetoright"),//'Slide right to unlock',
    //           successText: "verifysuccess",
    //           barSize : {
    //             width : '100%',
    //             height : '40px',
    //           },
    //           ready : function() {
    //             // verifyModeLang()
    //             // multilang.displaylang()
    //           },
    //           success : function() {
    //             // isValidCode = true;
    //             //verifyModeLang()
    //             if(!validEmptyByModal()){
    //               swipeVerifyCodeByModal()
    //               return;
    //             }
    //             let preferLen = $("input[name='modalPrefer']:checked").length
    //             if(!preferLen){
    //               swipeVerifyCodeByModal()
    //               alert('Please tick one or both option!')
    //               return;
    //             }
    //             getSwipeCodeByModal()
    //           },
    //           error : function() {

    //           }
    //         });
    //       }

    //       function getSwipeCodeByModal() {
    //         var reqParam= getInputParamByModal()
    //         $.ajax({
    //           type: "post",
    //           contentType: 'application/x-www-form-urlencoded',
    //           url: wy_https_root + "email/getSendEmailCode",
    //           datatype: "json",
    //           data: reqParam,
    //           success: function (res) {
    //             if(res.code == 0){
    //               modalValidCode= res.message
    //             }else{
    //               $("#btnModalSubmit").prop("disabled",true)
    //               setTimeout(function () {
    //                 $("#btnModalSubmit").prop("disabled",false)
    //                 $(".tip-message").text('')
    //                 $(".tip-message").removeClass("text-danger")
    //                 swipeVerifyCodeByModal()
    //               },3000)
    //             }
    //           }
    //         });
    //       }


    //       function emptyTipMsg(){
    //         setTimeout(function () {
    //           $(".tip-message").text('')
    //         },3000)
    //       }
    //     }
    });

    // MENU
    // $('.navbar-collapse a').on('click',function(){
    //   $(".navbar-collapse").collapse('hide');
    // });
      
    $(window).scroll(function() {
      if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
          } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
          }
    });

    // click product
    $('.has-submenu').on('click',function(){
      event.stopPropagation();
      $('.main-menu li .sub-menu').toggleClass('showList')
    })


    // PARALLAX EFFECT
    $.stellar({
      horizontalScrolling: false,
    }); 

    // MAGNIFIC POPUP
    $('.image-popup').magnificPopup({
        type: 'image',
        removalDelay: 300,
        mainClass: 'mfp-with-zoom',
        gallery:{
          enabled:true
        },
        zoom: {
        enabled: true, // By default it's false, so don't forget to enable it

        duration: 300, // duration of the effect, in milliseconds
        easing: 'ease-in-out', // CSS transition easing function

        // The "opener" function should return the element from which popup will be zoomed in
        // and to which popup will be scaled down
        // By defailt it looks for an image tag:
        opener: function(openerElement) {
        // openerElement is the element on which popup was initialized, in this case its <a> tag
        // you don't need to add "opener" option if this code matches your needs, it's defailt one.
        return openerElement.is('img') ? openerElement : openerElement.find('img');
        }
      }
    });

    // SMOOTH SCROLL
    // $(function() {
    //   $('.custom-navbar a, #home a').on('click', function(event) {
    //     var $anchor = $(this);
    //       $('html, body').stop().animate({
    //         scrollTop: $($anchor.attr('href')).offset().top - 49
    //       }, 1000);
    //         event.preventDefault();
    //   });
    // });

  $("#wePartner .partner-box li").mouseenter(function(){
    let country = $(this).attr("data-id");
    $(this).parent().find('li').removeClass('active');
    $(this).addClass('active');
    $(".partner-items-box").hide();
    $(".partner-"+country.toLowerCase()).show();
  })

  $("#wePartner #countryChange").on('click', function () {
    $(this).parent().find('.drop-menu').toggleClass('drop-menu-show');
  })

  $("#wePartner .drop-menu li").on('click', function () {
    let country = $(this).attr("data-id");
    let countryName = $(this).text();
    $(this).parent().find('li').removeClass('active');
    $(this).addClass('active');
    $(".partner-items-box").hide();
    $(".partner-"+country.toLowerCase()).show();
    $("#wePartner .countryText").text(countryName);
    $(this).parent().removeClass('drop-menu-show')
  });

    $("#partner .tab li").click(function(){
      let country = $(this).text()
      $(this).parent().find('li').removeClass('active')
      $(this).addClass('active')
      $("#partner .main-box").css('background',`url(/images/${country}_payment.png) no-repeat center`)
      $("#partner .main-box").css('background-size','auto 100%')
      if(country == 'Indonesia') {
        $("#partner .main-box").css('background-size','100% 100%')
      }
      // mobile
      $(".partner-box").hide();
      $(".partner-"+country.toLowerCase()).show();
    })

    // send email (contact us)
    // let wy_https_root = window.location.origin+'/api-email/'

    // contact form
    $(document).on('click', '.contactForm', function(){
      // 加载partials/contact.html 全屏插入body,fixed全屏
      $("#contactFormModal").remove();
      // 
      $("body").append("<div id='contactFormModal'></div>");
      $("#contactFormModal").load("../src/partials/contact.html","",function(){
      $("#contactFormModal").css({
        "width": "100vw",
        "height": "100vh",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "background": "rgba(0,0,0,0.5)",
        "z-index": "9999"
      });

    let validCode=""

    // 初始化 intlTelInput
    const phoneInput = document.querySelector("#phone");
    let contactIti = window.intlTelInput(phoneInput, {
      initialCountry: "auto",
      formatOnDisplay: true,
      geoIpLookup: function(callback) {
        $.get('https://ipinfo.io', function() {}, "jsonp").always(function(resp) {
          var countryCode = (resp && resp.country) ? resp.country : "ID";
          callback(countryCode);
        });
      },
      utilsScript: "utils.js"
    });

    function getInputParam(){
      var name = $("#name").val();
      var email = $("#email").val();
      var phone = $("#phone").val();
      var country = '';
      var dialCode = '';
      
      // 使用 try-catch 来处理可能的错误
      try {
        if(contactIti) {
          country = contactIti.getSelectedCountryData().name;
          dialCode = contactIti.getSelectedCountryData().dialCode;
        }
      } catch(e) {
        console.warn('无法获取国家数据:', e);
        country = '';
        dialCode = '';
      }
      
      var message = $("#message").val();
      var contactType = '';
      let arr = [];
      $('input[name="prefer"]:checked').each(function(index, element) {
        arr.push($(this).val());
      });
      contactType = arr.join(',');
      
      var params = {
        name: name,
        email: email,
        phone: dialCode ? (dialCode + ' ' + phone) : phone,
        country: country,
        message: message,
        validCode: validCode,
        contactType: contactType,
        subject: "PAYOK"
      };

      return params;
    }

    function validEmpty() {
      var dom= $("#contact-form");
      var flag = true
      for (let index = 0; index < dom.find('.require').length; index++) {
        let val = dom.find('.require').eq(index).val()
        // if (!val){
        //   val = dom.find('.require').eq(index).text()
        // }
        if (val.trim() == '') {
          // dom.find('.require').eq(index).css({
          //   borderColor: '#ff0844'
          // })
          flag = false
          alert('Please fill out the form.')
          return
        }
      }
      return flag
      // if(flag == false){
      //   return false
      // }
    }

    function emptyForm() {
      $("#contact-form").find('input,textarea').val('')
      // $(".prefer")
    }
    /**
     * Easy event listener function
     */
    setTimeout(function(){
      sendEmail();
    },1000)
    function sendEmail(){
      $("#btnSubmit").click(function () {
        // if(validCode == "") return;
        if(!validEmpty()) {
          alert('Please fill out the form.')
          return
        };
        $(".loading").addClass("d-block")
        $("#btnSubmit").prop("disabled",true)
        var reqParam= getInputParam()
        reqParam.validCode= validCode
  
        $.ajax({
          type: "post",
          contentType: 'application/x-www-form-urlencoded',
          url: wy_https_root + "email/send",
          datatype: "json",
          data: reqParam,
          success: function (res) {
            if(res.code == 0){
              emptyForm();
              $(".loading").removeClass("d-block")
              alert('Send successfully!')
              window.location.reload()
            }else{
              $(".loading").removeClass("d-block")
              alert('Sending failed. Please try again later!')
              window.location.reload()
            }
          },complete: function () {
            setTimeout(function () {
              $('.php-email-form')[0].reset();
              $(".tip-message").text('')
              swipeVerifyCode();
              $("#btnSubmit").prop("disabled",false)
            },2000)
          }
        });
      })

      try {
        swipeVerifyCode();
      }catch (e) {

      }

      /**
       * verify code
       */
      function swipeVerifyCode(){
        validCode=""
        $('#mpanel2').html('')
        $('#mpanel2').slideVerify({
          type : 1,       //type
          vOffset : 5,
          currTab: "btnLogin",
          barText: $.i18n.prop("slidetoright"),//'Slide right to unlock',
          successText: "verifysuccess",
          barSize : {
            width : '100%',
            height : '40px',
          },
          ready : function() {
           // verifyModeLang()
            // multilang.displaylang()
          },
          success : function() {
           // isValidCode = true;
            //verifyModeLang()
            if(!validEmpty()){
              swipeVerifyCode()
              return;
            }
            let preferLen = $("input[class='prefer']:checked").length
            if(!preferLen){
              swipeVerifyCode()
              alert('Please tick one or both option!')
              return;
            }
            $("#loginInfoMode").removeClass("d-none")
            getSwipeCode()
          },
          error : function() {
  
          }
        });
      }
  
      function getSwipeCode() {
        var reqParam= getInputParam()
        $.ajax({
          type: "post",
          contentType: 'application/x-www-form-urlencoded',
          url: wy_https_root + "email/getSendEmailCode",
          datatype: "json",
          data: reqParam,
          success: function (res) {
            if(res.code == 0){
              validCode= res.message
            }else{
              $("#btnSubmit").prop("disabled",true)
              $(".loading").removeClass("d-block")
              $(".tip-message").text("Total Email maksimal yang dapat dikirim pada hari itu telah tercapai")
              $(".tip-message").addClass("text-danger")
              setTimeout(function () {
                $("#btnSubmit").prop("disabled",false)
                $('.php-email-form')[0].reset();
                $(".tip-message").text('')
                $(".tip-message").removeClass("text-danger")
                swipeVerifyCode()
              },3000)
            }
          }
        });
      }
  
  
      function emptyTipMsg(){
        setTimeout(function () {
          $(".tip-message").text('')
        },3000)
      }
    }

  var isValidEmail= function (str) {
      var reg = /^[a-zA-Z0-9]+([-_.][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([-_.][a-zA-Z0-9]+)*\.[a-z]{2,}$/
      return reg.test(str)
    }

    checkPrefer();
    // Check at least one preference
    function checkPrefer() {
      $(".prefer").change(function (e) {
        let len = $("input[class='prefer']:checked").length;
        $("#btnSubmit").attr('disabled',true)
        if(len) {
          $("#btnSubmit").attr('disabled',false)
        }
      });
    }

  })
  })
    
    // integrationNew
    // 初始化显示第一个slide和对应指示器
    $('.banner-slide:first').addClass('active');
    $('.indicator:first').addClass('active');
    
    // 点击指示器切换幻灯片
    $('.indicator').click(function() {
        if($(this).hasClass('active')) return;
        
        const index = $(this).index();
        const currentIndex = $('.indicator.active').index();
        const direction = index > currentIndex ? 'right' : 'left';
        
        // Get current and target slides
        const $currentSlide = $('.banner-slide.active');
        const $targetSlide = $('.banner-slide').eq(index);
        
        // Set different animation classes based on direction
        if(direction === 'right') {
            // Current slide slides out to the left
            $currentSlide.removeClass('active').addClass('slide-out-left');
            // Target slide slides in from the right
            $targetSlide.addClass('slide-in-right');
            
            // Wait a short time before starting the animation
            setTimeout(function() {
                $targetSlide.removeClass('slide-in-right').addClass('active');
                
                // Clear temporary classes after animation
                setTimeout(function() {
                    $currentSlide.removeClass('slide-out-left');
                }, 500);
            }, 50);
        } else {
            // Current slide slides out to the right
            $currentSlide.removeClass('active').addClass('slide-out-right');
            // Target slide slides in from the left
            $targetSlide.addClass('slide-in-left');
            
            // Wait a short time before starting the animation
            setTimeout(function() {
                $targetSlide.removeClass('slide-in-left').addClass('active');
                
                // Clear temporary classes after animation
                setTimeout(function() {
                    $currentSlide.removeClass('slide-out-right');
                }, 500);
            }, 50);
        }
        
        // Update indicator status
        $('.indicator.active').removeClass('active');
        $(this).addClass('active');
    });


  // 添加关闭联系表单的函数
  window.closeContactForm = function() {
    // 阻止点击到下一层
    event.stopPropagation();
    $('#contactFormModal').hide();
  }

   // 获取当前页面的URL路径
   var currentPath = window.location.pathname;
   // 获取文件名
   var currentPage = currentPath.substring(currentPath.lastIndexOf('/') + 1);
   
   // Solution子菜单处理
   setTimeout(function() {
    $('#pgSolutionMenu li a').each(function() {
        var menuHref = $(this).attr('href');
        if (menuHref === currentPage) {
            $('#pgSolutionMenu li').removeClass('active');
            $(this).parent('li').addClass('active');
            // 确保父级Solution菜单也显示为激活状态
            //  $('#pgSolution').addClass('active');
        }
    });
   }, 1000);

  // 检查是否在首页
  document.addEventListener('DOMContentLoaded', function() {
     $(document).on("mouseenter", "#langLi", function() {
      console.log($("#header").attr("pg-name"));
      if ($("#header").attr("pg-name") === "pgIndex") {
        // 如果是首页，隐藏越南语选项
        // $(".vn-lang,.tr-lang").hide();
      }
      // url 含/blog 隐藏印尼语选项
      if (window.location.pathname.includes("/blog")) {
        $(".tr-lang,.vn-lang").hide(); 
      }

    });
  });

})(jQuery);

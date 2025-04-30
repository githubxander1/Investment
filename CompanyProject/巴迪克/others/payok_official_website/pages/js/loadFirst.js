
      $("#header").load("../src/partials/header.html","",function(){
        $('.custom-navbar .navbar-toggle').on('click',function(){
          $(".js_mainBody").toggleClass("frame_mainBody_Open")
          // $('.custom-navbar').toggleClass('bg-white')
        })

        $("#langChange").on('click', function() {
          $(".navbar-right .sub-menu").attr('opacity', '1')
          $(".m-country-select").show()
        })

        //change lang
        $(".lang").on('change', function () {
            sessionStorage.setItem("lang", $(this).val());
            loadProperties($(this).val());
        });
        // mobile
        $("#langLiM").on('click', function () {
          $(this).find('.sub-menu').toggleClass('m-show-country')
        })
        $("#langLiM .sub-menu li").on('click', function () {
          let langShort = $(this).attr('langval')
          $(".langText").text(lang[langShort]);
          sessionStorage.setItem("lang", $(this).attr('langval'));
          loadProperties($(this).attr('langval'));
          $(this).addClass('active').siblings().removeClass('active')
        });
        // pc
        $("#langLi .sub-menu li").on('click', function () {
          let langShort = $(this).attr('langval')
          $(".langText").text(lang[langShort]);
          sessionStorage.setItem("lang", $(this).attr('langval'));
          loadProperties($(this).attr('langval'));
        });
        // let langShort = sessionStorage.getItem("lang");
        // $("#langLi .sub-menu li[langval='"+langShort+"']").addClass('active').siblings().removeClass('active')

        var currPage= $("#header").attr("pg-name");
        $(".main-menu li[id='"+currPage+"']").addClass("menu-active");
        $("#header [data-locale]").addClass("v-visible");
        // $(".main-menu li").click(function () {
        //     $(this).addClass("active")
        // })
        
      })
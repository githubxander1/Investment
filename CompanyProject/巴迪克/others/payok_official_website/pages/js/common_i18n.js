"use strict";
/*const langObj = {
    en: 'English',
    id: 'Bahasa',
    os: 'Türkçe ',
    in: 'हिन्दी',
    vn: 'Tiếng Việt'
}*/
const langObj = {
    en: 'EN',
    tr: 'TR ',
    id: 'ID',
    br: 'BR',
    vn: 'VN',
    bd: 'BD',
    th: 'TH',
    in: 'IN'
}
var lang = sessionStorage.getItem("lang");
if (lang === null) {
    lang = "en";
    sessionStorage.setItem("lang",lang);
}
// loadProperties(lang);
setTimeout(function () {
    loadProperties(lang);
    $("#lang").val(lang);
    $(".langText").text(langObj[lang])
},300);

function loadProperties(types) {
    try {
        $.i18n.properties({
            name: 'strings', 
            path: '/i18n/', 
            mode: 'map',
            language: types, 
            callback: function () {
            $("[data-locale]").each(function () {
                $(this).addClass("v-visible");
                $(this).html($.i18n.prop($(this).data("locale")));
            });
            $("[data-placeholder]").each(function () {
                $(this).attr('placeholder', $.i18n.prop($(this).data("placeholder")));
            });

            var insertInputEle = $(".i18n-input");
            insertInputEle.each(function() {
            var selectAttr = $(this).attr('selectattr');
                if (!selectAttr) {
                    selectAttr = "value";
                };
                $(this).attr(selectAttr, $.i18n.prop($(this).attr('selectname')));
            });

            // term-conditions page only show english
            // if(window.location.href.indexOf("term-conditions") > -1){
            //      $(".terms").hide();
            //      $(".terms.lang-"+sessionStorage.getItem("lang")).show();
            // }
        }
    });
    } catch (e) {
        console.log(e);
    }
}


$(function() {
    "use strict";


    $.sidebarMenu = function(menu) {
        var animationSpeed = 300,
            subMenuSelector = '.sidebar-submenu';
        $(menu).on('click', 'li a', function(e) {
            var $this = $(this);
            var checkElement = $this.next();
            if (checkElement.is(subMenuSelector) && checkElement.is(':visible')) {
                checkElement.slideUp(animationSpeed, function() {
                    checkElement.removeClass('menu-open');
                });
                checkElement.parent("li").removeClass("active");
            }
            //If the menu is not visible
            else if ((checkElement.is(subMenuSelector)) && (!checkElement.is(':visible'))) {
                //Get the parent menu
                var parent = $this.parents('ul').first();
                //Close all open menus within the parent
                var ul = parent.find('ul:visible').slideUp(animationSpeed);
                //Remove the menu-open class from the parent
                ul.removeClass('menu-open');
                //Get the parent li
                var parent_li = $this.parent("li");
                //Open the target menu and add the menu-open class
                checkElement.slideDown(animationSpeed, function() {
                    //Add the class active to the parent li
                    checkElement.addClass('menu-open');
                    parent.find('li.active').removeClass('active');
                    parent_li.addClass('active');
                });
            }
            //if this isn't a link, prevent the page from being redirected
            if (checkElement.is(subMenuSelector)) {
                e.preventDefault();
            }
        });
    }


});


$(function() {
    "use strict";


    //sidebar menu js
    $.sidebarMenu($('.sidebar-menu'));

    // === toggle-menu js

    $(".toggle-menu").on("click", function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });


    // === sidebar menu activation js

    $(function() {
            for (var i = window.location, o = $(".sidebar-menu a").filter(function() {
                    return this.href == i;
                }).addClass("active").parent().addClass("active");;) {
                if (!o.is("li")) break;
                o = o.parent().addClass("in").parent().addClass("active");
            }
        }),

        /* Back To Top */

        $(document).ready(function() {
            $(window).on("scroll", function() {
                if ($(this).scrollTop() > 300) {
                    $('.back-to-top').fadeIn();
                } else {
                    $('.back-to-top').fadeOut();
                }
            });
            $('.back-to-top').on("click", function() {
                $("html, body").animate({
                    scrollTop: 0
                }, 600);
                return false;
            });
        });

    $(function() {
        $('[data-toggle="popover"]').popover()
    })


    $(function() {
        $('[data-toggle="tooltip"]').tooltip()
    })



});
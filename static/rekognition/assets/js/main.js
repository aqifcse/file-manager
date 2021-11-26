// Show password in login Register Form
$('.show_pass').click(function() {

    var hel = $(this)[0];

    if ($(hel).hasClass("fa-eye")) {
        $(this).prev()[0].type = "text";
        $(this).removeClass(" fa-eye");
        $(this).addClass(" fa-eye-slash");
    } else {
        $(this).prev()[0].type = "password";
        $(this).removeClass(" fa-eye-slash");
        $(this).addClass(" fa-eye");
    }

});

/* Login page slider js */
$(document).ready(function() {

    $(".custom_alert").fadeTo(2000, 500).slideUp(500, function() {
        $(".custom_alert").slideUp(500);
    });


    var checkVal = $('input[type=radio][name=show_in_home]:checked').val();
    if (checkVal == 'yes') {
        $('.show_hide').slideDown(500);
    } else if (checkVal == 'no') {
        $('.show_hide').slideUp(500);
    }
});


$('input[type=radio][name=show_in_home]').change(function() {
    if (this.value == 'yes') {
        $('.show_hide').slideDown(500);
    } else if (this.value == 'no') {
        $('.show_hide').slideUp(500);
    }
});


$('input[type=radio][name=access_control]').change(function() {
    if (this.value == 'yes') {
        $('.show_hide2').slideDown(500);
    } else if (this.value == 'no') {
        $('.show_hide2').slideUp(500);
    }
});

$('input[name=rbnNumber]:checked').val();

$(document).on('click', '.dropdown-menu.dropdown-menu-right.animated.fadeIn.show', function(e) {
    e.stopPropagation();
})
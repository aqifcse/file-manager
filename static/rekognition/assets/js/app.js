$(document).on("click", ".preview_click_btn_orginal", function() {
    console.log(this)
    console.log('image');
    $('#preview_img').attr('src', $(this).attr('code')).fadeIn(1000);
    $('#preview_vd').attr('src', $(this).attr('code')).fadeIn(1000);
});
$(document).on("click", ".pause_video", function() {
    $('#preview_vd').attr('src', '');
});
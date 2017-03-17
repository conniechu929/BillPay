function isEmpty( el ){
    return !$.trim(el.html())
};

$(document).ready(function() {
    var error = document.getElementById("error");

    $(window).scroll(function(){
      if ($(this).scrollTop()>1){
        $("nav").addClass('opacity');
      }
      else {
        $("nav").removeClass('opacity');
      }
    });


    if($('#error_message').html() != undefined){
      $("#navLogin").trigger('click');
    };

    $('.signin-toggle').click(function() {
      $("#registration").slideUp("slow", function() {
        $("#signin").slideDown("slow");
      });
    });

    $('.register-toggle').click(function() {
      $("#signin").slideUp("slow", function() {
        $("#registration").slideDown("slow");
      });
    });

    $("#navLogin").click(function() {
      $("nav").removeClass('opacity');
    });

});

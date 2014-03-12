$(function () {
  $("#dev-subscribe").click(function (e) {
    e.preventDefault();
    $('#dev-subscribe').addClass('disabled');

    $.ajax({
        type: "POST",
        url: "http://api.moodsy.com/beta/signup",
        data: {
            "email": $('#email').val()
        },
        success: function() {
            $('#dev-subscribe').html('Thank You!');
            $('#dev-subscribe').removeClass('disabled');
        }
        // TODO: What about errors?
    });
  });
});
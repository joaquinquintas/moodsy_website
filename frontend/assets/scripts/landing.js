$(function () {
  $("#dev-subscribe").click(function (e) {
    e.preventDefault();
    $('#dev-subscribe').addClass('disabled');

    $.ajax({
        type: "POST",
        url: "http://wapi.moodsy.me/subscribers/signup",
        data: {
            "email": $('#email').val()
        },
        success: function() {
            console.log("Submission successful.");
            $('#dev-subscribe').html('Thank You!');
            $('#dev-subscribe').removeClass('disabled');
        },
        error: function() {
            console.error("Submission failure!");
        }
        // TODO: What about errors?
    });
  });
});

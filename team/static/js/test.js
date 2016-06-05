/**
 * Created by cwh on 16-6-4.
 */
$(function () {
    $('#check').click(function () {
        $('#check').src = "http://127.0.0.1:8000/team/valid_code";
        var a = $.ajax({
            url: "http://127.0.0.1:8000/team/valid_code",
            processData: false
        }).always(function (data) {
                console.log('test');
                $("#check").attr('src', "data:image/gif;base64," + data);
            }
        );
    });
});
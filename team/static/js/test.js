/**
 * Created by cwh on 16-6-4.
 */
$(function () {
    $('#check').click(function () {
        $('#check').src = "http://110.64.69.66:8081/team/valid_code";
        var a = $.ajax({
            url: "../../team/valid_code",
            processData: false
        }).always(function (data) {
                console.log('test');
                $("#check").attr('src', "data:image/gif;base64," + data);
            }
        );
    });
});
$(document).ready(function () {
    $('#check').src = "http://110.64.69.66:8081/team/valid_code";
        var a = $.ajax({
            url: "../../team/valid_code",
            processData: false
        }).always(function (data) {
                console.log('test');
                $("#check").attr('src', "data:image/gif;base64," + data);
            }
        );
});
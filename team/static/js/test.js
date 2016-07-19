/**
 * Created by cwh on 16-6-4.
 */
function loadValidCode(id) {
    $.ajax({
            url: "http://110.64.69.66:8081/team/valid_code",
            processData: false
        }).always(function (data) {
                console.log('test');
                $(id).attr('src', "data:image/gif;base64," + data);
            }
        );

}

$(document).ready(function () {
    $('#check').click(function () {
        loadValidCode('#check');
    });
    $('#check2').click(function () {
        loadValidCode('#check2');
    });
    loadValidCode('#check');
    loadValidCode('#check2');
});
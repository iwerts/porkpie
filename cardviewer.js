$(function(){
    var data = [
    {
        "id":"1",
        "name":"Test 1"
    },
    {
        "id":"2",
        "name":"Test 2"
    }
    ];
    $.each(data, function(i, option){
        $('#sel').append($('<option/>').attr("value", option.id).text(option.name));
    });
})
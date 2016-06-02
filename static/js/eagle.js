$(document).ready(function(){
    $(".sub_btn").click(function(){
        $.ajax({
            url: "/create_instance",
            type: "POST",
            data: $('.create-instance').serialize(),
        });
    });

});

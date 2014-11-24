$('.downbutton').on('click', function (e) {
    var id = this.id;
    id = id.replace("downbutton", "");

    slidervalue = $("#"+id).slider( "value" );
    console.log(slidervalue);
    $("#"+id).slider('value', slidervalue - 1 );
});

$('.offButton').on('click', function (e) {
    var id = this.id;
    id = id.replace("offButton", "");

    $("#"+id).slider('value', 0);
});

$('.onButton').on('click', function (e) {
    var id = this.id;
    id = id.replace("onButton", "");

    $("#"+id).slider('value', 100 );
});

$('.nightButton').on('click', function (e) {
    var id = this.id;
    id = id.replace("nightButton", "");

    $("#"+id).slider('value', 5 );
});

$('.upbutton').on('click', function (e) {
    var id = this.id;
    id = id.replace("upbutton", "");

    slidervalue = $("#"+id).slider( "value" );
    console.log(slidervalue);
    $("#"+id).slider('value', slidervalue + 1 );
});

$(".slider").each(function(){
    var datavalue = $(this).data('value');
    var callback = $(this).data('callback');
    var deviceid = $(this).data('id');
    console.log(datavalue);
    console.log(deviceid);
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "positionClass": "toast-top-right",
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
        }
    $(this).slider({
        value: datavalue,
        min: 0,
        max: 100,
        step: 1,
        animate: true,
        create: function(event, ui) {
        $("span." + callback).html($(this).slider('value'));
        },
        change: function(event, ui) {
            var curVal = ui.value;
            $("span." + callback).html($(this).slider('value'));
            $.ajax({
                dataType: "json",
                contentType: "application/json",
                type: 'POST',
                url: "https://mattlovett.com/homer/setbrightness",
                data: {
                    "id":deviceid,
                    "brightness":Math.round((curVal/100)*255)
                },
                error: function(e, errorText, httpDescription) {
                    console.log("post failed");
                    console.log(errorText);
                        if (errorText  == "error") {
                            console.log(httpDescription);
                        }
                    toastr.error("failed to communicate with device")
                },
                success: function(data) {
                    toastr.success("Brightness set to " + data.brightness, data.name)
                }
            });
        },
        stop: function(event, ui) {
            var curVal = ui.value;
            $("span." + callback).html($(this).slider('value'));
            $.ajax({
                dataType: "json",
                contentType: "application/json",
                type: 'POST',
                url: "https://mattlovett.com/homer/setbrightness",
                data: {
                    "id":deviceid,
                    "brightness":Math.round((curVal/100)*255)
                },
                success: function(data) {
                    toastr.success("Brightness set to " + data.brightness, data.name)
                },
                error: function(e, errorText, httpDescription) {
                    console.log("post failed");
                    console.log(errorText);
                        if (errorText  == "error") {
                            console.log(httpDescription);
                        }
                    toastr.error("failed to communicate with device")
                },
            });
        }
    })
});





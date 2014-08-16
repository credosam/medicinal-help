function showResponse(response) {
    result = JSON.parse(response);
    $('#response').html('');
    // console.log(result);
    // console.log(result.items.length);
    for (var i = 0; i < result.items.length; i++) {
        var snipobj = result.items[i];
        var divItem1 = $('<div></div>');
        divItem1.addClass('span12');
        var divItem2 = $('<div></div>');
        divItem2.addClass('span12');
        // MSApp.execUnsafeLocalFunction(function () {
        divItem1.html("<br><a href=" + snipobj.url + "target='_blank'><b>" + snipobj.nam + "</b></a>");
        divItem2.html(snipobj.desc);
        var result1 = $('<div></div>').addClass('row-fluid').append(divItem1);
        var result2 = $('<div></div>').addClass('row-fluid').append(divItem2);
        $('#response').append(result1).append(result2);
        // });
    }
}

function search() {
    var url = document.getElementById('query').value;
    console.log(url);
    $.ajax('http://medicinal-help.appspot.com/scrape/?url=' + url, {
        type: "GET",
        contentType: 'application/jsonp',
        dataType: 'jsonp',
        crossDomain: true,
        success: function (data) {
            // alert(JSON.stringify(data));
            // console.log(JSON.stringify(data));
            showResponse(JSON.stringify(data));
        },
        error: function (req, errType, errMessage) {
            console.log(errType + " " + errMessage);
        }
    });
}


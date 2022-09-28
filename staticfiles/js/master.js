




$(document).ready(function(){
    console.log("ready to go")

    let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    // GET
    $("#testing-ajax").click(function(){
        console.log("click registered")
        $.ajax({
            url: '',
            type: 'get',
            data: {
                button_text: $(this).text()
            },
            success: function(response){
                $("#testing-ajax").text(response.users)
                $("#seconds").append(`<li>` + response.users + `</li>`)
            }
        })
    });

    // POST
    $("#seconds").on('click', `li`, function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                text: $(this).text(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response){
                $("#ajax-success").append("<li>" + response.data +  "</li>")
            }
        })
    })

});   


 function send(){
        const input_message = $('#type-message').val()
        console.log(input_message)
        // return if the user does not enter any text
        if (!input_message) {
          return
        }

        $('#messages').append(`
            <div class="chat-message col-md-5 human-message pull-left" id="person-message">
                ${input_message}
            </div>
        `)

        // loading
        $('#messages').append(`
            <div class="chat-message text-center col-md-2 offset-md-10 bot-message pull-right" id="loading">
                <b>...</b>
            </div>
        `)

        // clear the text input 
        $('#type-message').val('')

        // send the message
        submit_message(input_message)
    }

 function submit_message(message) {
     console.log(message)
    $.post( "/input", {
        "content-type" : "application/json",
        "my-message": message
        }, handle_response);

    function handle_response(data) {
        // append the bot response to the div
        console.log(data)
        $('#messages').append(`
            <div class="chat-message col-md-5 offset-md-7 bot-message pull-right" id="reply">
                ${data}
            </div>
        `)
        // remove the loading indicator
        $( "#loading" ).remove()
    }
}

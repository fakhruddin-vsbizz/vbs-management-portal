function fillAndPopAgentEditModal(id, first_name, last_name, email) {
    document.getElementById('edit_first_name').setAttribute('value',first_name)
    document.getElementById('edit_last_name').setAttribute('value',last_name);
    document.getElementById('edit_email').setAttribute('value', email);
    document.getElementById('id_employee').setAttribute('value', id);

    modal_instance = document.getElementById('modal-close-default');
    UIkit.modal(modal_instance).show();
}

function editNames(csrf_token) {
    
    first_name = document.getElementById('first_name').value;
    last_name = document.getElementById('last_name').value;
    id = document.getElementById('id_employee').value;

    var is_api_go = false;

    if(validateField(first_name) && validateField(last_name)){
        is_api_go = true;
    }else{
        is_api_go = false;
        alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
    }

    if(is_api_go){
        $.ajax({
            url: 'http://localhost:8000/travel/api/edit_travel_agent_details',
            type: 'PUT',
            data: {
                csrfmiddlewaretoken: csrf_token,
                "id": parseInt(id),
                "first_name": first_name,
                "last_name": last_name,
            },
            success: function(data){
                console.log('succes sdata', data)
                alertbox.innerHTML = data['response_message'];
                // window.location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },        
        });
    }else{
        alertbox.innerHTML = "Some server error has occured. Please contact developer@vsbizz.com for more info.";
    }


}
function transferDeactivatingID(id) {
    document.getElementById('deactivate_id_employee').setAttribute('value', id);
    modal_instance = document.getElementById('travel-agent-remove');
    UIkit.modal(modal_instance).show();
}

function deactivateAgents(csrf_token, activation_status) {
    
    var deactivating_id = document.getElementById('deactivate_id_employee').value;
    var alertbox = document.getElementById('deactivate_alertbox');

    is_api_go = false;
    console.log(activation_status);

    if(validateField(deactivating_id)){
        is_api_go = true;
    }else{
        is_api_go = false;
        alertbox.innerHTML = 'It seems like a processing issue. Please try again or contact developer@vsbizz.com';
    }

    if(is_api_go){
        $.ajax({
            url: 'http://localhost:8000/travel/api/edit_travel_agent_details',
            type: 'PUT',
            data: {
                csrfmiddlewaretoken: csrf_token,
                "id": parseInt(deactivating_id),
                "is_active":false
            },
            success: function(data){
                console.log('api run response')
                alertbox.innerHTML = "Deactivation successful";
                // window.location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },        
        });
    }
}

function validateField(variant){
    if(variant != "" && variant != null && variant != " "){
        return true
    }else{
        return false
    }
}
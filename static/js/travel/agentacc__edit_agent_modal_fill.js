function fillAndPopAgentEditModal(id, first_name, last_name, email) {
    document.getElementById('edit_first_name').setAttribute('value',first_name)
    document.getElementById('edit_last_name').setAttribute('value',last_name);
    document.getElementById('edit_email').setAttribute('value', email);
    document.getElementById('id_employee').setAttribute('value', id);

    modal_instance = document.getElementById('modal-close-default');
    UIkit.modal(modal_instance).show();
}

function dummyAlert(){
    alert('console chala mast')
}

function editTravelAgent(csrf_token, tag) {

    var pushable_data = null;

    // form values fetched
    first_name = document.getElementById('edit_first_name').value;
    last_name = document.getElementById('edit_last_name').value;
    email = document.getElementById('edit_email').value;
    password = document.getElementById('edit_password').value;
    conf_password = document.getElementById('conf_password').value;

    // primary key of the employee
    id = document.getElementById('id_employee').value;

    // api gate switch to allow to run API
    var is_api_go = false;

    // switcher for the data to be returned
    switch (tag) {
        case "names":
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "id": parseInt(id),
                "first_name": first_name,
                "last_name": last_name,
            }

            if(validateField(first_name) && validateField(last_name)){
                is_api_go = true;
            }else{
                is_api_go = false;
                alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
            }

            break;
        
        case "email":
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "id": parseInt(id),
                "email": email
            }

            if(validateField(email)){
                is_api_go = true;
            }else{
                is_api_go = false;
                alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
            }

            break;
        
        case "password":
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "id": parseInt(id),
                "password": password
            }

            if(validateField(password) && validateField(conf_password) && arePasswordSame(password, conf_password)){
                is_api_go = true;
            }else{
                is_api_go = false;
                alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
                
            }

            break;

        default:
            break;
    }

    // alertbox for showing alerts
    alertbox = document.getElementById('edit_alertbox');
    
 
    // if variable true, api runs
    if(is_api_go){
        console.log('api run mast')
        $.ajax({
            url: 'http://localhost:8000/travel/api/edit_travel_agent_details',
            type: 'PUT',
            data: pushable_data,
            success: function(data){
                console.log('api run response')
                alertbox.innerHTML = data['message'];
                window.location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },        
        });
    }else{
        alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
    }
}

// validate null, empty and space-only values
function validateField(variant){
    if(variant != "" && variant != null && variant != " "){
        return true
    }else{
        return false
    }
}

function arePasswordSame(pass, confpass) {
    return pass == confpass;
}

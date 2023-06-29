
function createNewClient(csrf_token) {

    console.log('HITTING')
    
    // status to hit the API if all client side validation persist without fail
    is_api_go = false;
    
    // getting all fields value
    first_name = document.getElementById('first_name').value;
    last_name = document.getElementById('last_name').value;
    organization = document.getElementById('organization').value;
    contact_number = document.getElementById('contact_number').value;
    email = document.getElementById('email').value;

    
    auth_user_ref = document.getElementById('referrer_id').value;

    console.log(auth_user_ref)

    //alert box DOM
    alertbox = document.getElementById('alertbox');

    // field validation
    if(validateField(first_name) && validateField(last_name) && validateField(organization) && validateField(contact_number) && validateField(email)){
        is_api_go = true;
    }else{
        is_api_go = false;
        alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
    }

    if(is_api_go){
        $.ajax({
            url: 'http://localhost:8000/travel/api/create_new_client',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrf_token,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "organization": organization,
                "contact_number": contact_number,
                "admin_auth_user_ref": parseInt(auth_user_ref)
            },
            success: function(data){
                console.log('succes sdata', data)
                alertbox.innerHTML = data['message'];
                location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },        
        });
    }else{
        alertbox.innerHTML = "Validation issues have occured. Please check format of the data properly";
    }
    

}

function validateField(variant){
    if(variant != "" && variant != null && variant != " "){
        return true
    }else{
        return false
    }
}

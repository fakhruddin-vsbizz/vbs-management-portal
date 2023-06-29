
function createNewAgent(csrf_token) {

    console.log('HITTING')
    
    // status to hit the API if all client side validation persist without fail
    is_api_go = false;

    // 
    email = document.getElementById('email').value;
    password = document.getElementById('password').value;
    conf_password = document.getElementById('conf_password').value;

    employee_id = document.getElementById('employee_id').value;

    //alert box DOM
    alertbox = document.getElementById('alertbox');

    // field validation
    if(validateField(email) && validateField(password) && validateField(conf_password) && validateField(first_name) && validateField(last_name)){
        is_api_go = true;
    }else{
        is_api_go = false;
        alertbox.innerHTML = "Seems either of the field is empty or null. Please check the fields and try again";
    }


    first_name = document.getElementById('first_name').value;
    last_name = document.getElementById('last_name').value;
    user_group = 'travel_agent';


    $.ajax({
        url: 'http://localhost:8000/travel/api/create_new_agent',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrf_token,
            "email": email,
            "password":password,
            "user_group": user_group,
            "first_name": first_name,
            "last_name": last_name,
            "employee_id": employee_id
        },
        success: function(data){
            console.log('succes sdata', data)
            alertbox.innerHTML = data['response_message'];
            location.reload();
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },        
    });

}

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

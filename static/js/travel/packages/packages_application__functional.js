
var package_selection = {
    employee_ref: null,
    travel_client_ref: null,
    package_name: null,
    quantity_of_packages: null,
    package_type: null,
    boarding: null,
    destination: null,
    departure_date: null,
    arrival_date: null
}


var customer_invoicing = {
    gross_amount: null,
    service_fees: null,
    net_amount: null,
    discount: null,
    invoice_status: null,
    tentative_payment_date: null,
    passport_no: null,
    no_of_days: null
}


var vendor_management = {
    
}

function selectedClientIDForPackage(id, client_name) {
    package_selection['travel_client_ref'] = id;
    client_name_store = client_name
}

function clientDetailAutofillForPackage() {
    document.getElementById('client_name').innerHTML = client_name_store;
}

function getSelectedPackageType(obj) {
    package_selection['package_type'] = obj.value
}

function selectBoarding(obj) {
    package_selection['boarding'] = obj.id
}

function selectDestination(obj) {
    package_selection['destination'] = obj.id
}

function createPackageApplication(csrf_token, id, stage_change, app_id) {
    package_selection['arrival_date'] = document.getElementById('arrival_date').value;
    package_selection['departure_date'] = document.getElementById('departure_date').value;
    package_selection['package_name'] = document.getElementById('package_name').value;
    package_selection['quantity_of_packages'] = document.getElementById('no_of_packages').value;
    package_selection['employee_ref'] = id
    package_selection['id'] = app_id
    package_selection['csrfmiddlewaretoken'] = csrf_token

    $.ajax({
        url: 'http://localhost:8000/travel/api/travel_packages_crud',
        type: 'POST',
        data: package_selection,
        success: function(data){
            
            alertbox.innerHTML = data.message;
            // if(stage_change){

            //     window.location.href = '/travel/visa/application/'+data.id+'/document_processing'
            // }
            // window.location.reload();
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side error has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },        
    });
}
var package_selection = {
    employee_ref: null,
    travel_client_ref: null,
    package_name: null,
    quantity_of_packages: null,
    package_type: null,
    boarding: null,
    destination: null,
    departure_date: null,
    arrival_date: null,
    stage:"package_selection",
    status: 'pending'
}


var customer_invoicing = {
    gross_amount: null,
    service_fees: null,
    net_amount: null,
    discount: null,
    invoice_status: null,
    tentative_payment_date: null,
    passport_no: null,
    no_of_days: null,
    stage:"customer_invoicing",
    status: 'pending'
}


var vendor_management = {
    vendor_name: null,
    total_vendor_payment: null,
    first_installment: null,
    second_installment: null,
    third_installment: null,
    less_taxes: null,
    stage:'vendor_management',
    status:'pending'
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

function createPackageApplication(csrf_token, id, stage_change, app_id, client_id) {
    package_selection['arrival_date'] = document.getElementById('arrival_date').value;
    package_selection['departure_date'] = document.getElementById('departure_date').value;

    if(package_selection['package_type'] == null){
        package_selection['package_type'] = document.getElementById('form-horizontal-select').value;
    }
    
    if(client_id != ''){
        package_selection['travel_client_ref'] = Number(client_id)
    }

    package_selection['arrival_date'] = new Date(package_selection['arrival_date']).toString()
    package_selection['departure_date'] = new Date(package_selection['departure_date']).toString()

    if(Number(app_id) != ''){
        package_selection['boarding'] = document.querySelector('input[name="boarding"]:checked').value;

        package_selection['destination'] = document.querySelector('input[name="destination"]:checked').value;
    }
    
    package_selection['package_name'] = document.getElementById('package_name').value;
    package_selection['quantity_of_packages'] = document.getElementById('no_of_packages').value;

    package_selection['employee_ref'] = id
    package_selection['id'] = app_id
    package_selection['csrfmiddlewaretoken'] = csrf_token


    console.log(package_selection)

    $.ajax({
        url: 'http://localhost:8000/travel/api/travel_packages_crud',
        type: 'POST',
        data: package_selection,
        success: function(data){
            
            alertbox.innerHTML = data.message;
            if(stage_change){

                window.location.href = '/travel/packages/application/'+data.id+'/customer_invoicing'
            }
            
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side error has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },        
    });
}


function setInvoiceStatus(bool_status) {
    customer_invoicing['invoice_status'] = bool_status;
}

function resetTotal() {
    gross_amount = document.getElementById('gross_amount').value;
    service_fees = document.getElementById('service_fees').value;
    discount = document.getElementById('discount').value;

    net_total = Number(gross_amount)+Number(service_fees)

    net_total = Number(net_total+net_total*0.18)

    total_amount = net_total - Number(discount).toPrecision(6)

    customer_invoicing['gross_amount'] = gross_amount;
    customer_invoicing['service_fees'] = service_fees
    customer_invoicing['net_amount'] = net_total
    customer_invoicing['discount'] = discount

    document.getElementById('net_amount').innerHTML = net_total;
    document.getElementById('total_amount').innerHTML = total_amount;

}


function changePaymentTotal(client_paid_total_amount) {
    
    gross_profit = client_paid_total_amount - Number(document.getElementById('total_vendor_payment').value)

    total_profit = gross_profit - Number(document.getElementById('less_taxes').value);

    document.getElementById('gross_total').innerHTML = gross_profit;
    document.getElementById('overall_total').innerHTML = total_profit;
}


function updatePackageApplication(csrf_token, id, stage_change, stage_name) {

    console.log(stage_name)

    
    pushable_data = {};

    switch (stage_name) {
        case 'customer_invoicing':

            customer_invoicing['csrfmiddlewaretoken'] = csrf_token
            customer_invoicing['no_of_days'] = document.getElementById('no_of_days').value;
            customer_invoicing['passport_no'] = document.getElementById('passport_no').value;
            customer_invoicing['tentative_payment_date'] = new Date(document.getElementById('tentative_payment_date').value);
            customer_invoicing['app_id'] = id;

            //assign to main data
            pushable_data = customer_invoicing
            break;

        case 'vendor_management':

            vendor_management['csrfmiddlewaretoken'] = csrf_token
            vendor_management['vendor_name'] = document.getElementById('vendor_name').value;
            vendor_management['total_vendor_payment'] = Number(document.getElementById('total_vendor_payment').value).toPrecision(5)
            vendor_management['first_installment'] = document.getElementById('first_installment').value;
            vendor_management['second_installment'] = document.getElementById('second_installment').value;
            vendor_management['third_installment'] = document.getElementById('third_installment').value;
            vendor_management['less_taxes'] = Number(document.getElementById('less_taxes').value).toPrecision(4);
            vendor_management['app_id'] = id;

            vendor_management['status'] = stage_change ? "completed" : "pending"

            //assign to main data
            pushable_data = vendor_management
            break;

        case 'unblock_application':

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "app_id": id,
                "status": "open"
            }
            break;

        default:
            break;
    }
    
    console.log(pushable_data)

    $.ajax({
        url: 'http://localhost:8000/travel/api/travel_packages_crud',
        type: 'PUT',
        data: pushable_data,
        success: function(data){
            console.log(data)
            alertbox.innerHTML = data.message;
            page_url = ['package_selection','customer_invoicing','vendor_management']

            if(stage_change){
                if(page_url.indexOf(stage_name) == page_url.length-1){
                    window.location.href = '/travel/packages/application';
                }else{
                    window.location.href = '/travel/packages/application/'+data.id+'/'+page_url[page_url.indexOf(stage_name)+1]
                }
            }else{
                window.location.reload();
            }  
            
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


function createFollowUpForPackages(csrf_token, emp_id, app_id) {

    console.log(emp_id, app_id)
    
    followup_data = {
        csrfmiddlewaretoken: csrf_token,
        employee_id: emp_id,
        appl_id: app_id,
        application_type: "packages",
        followup_stage:"in_followups",
        time_for_followups: document.getElementById('followup_time').value,
        date_for_followups: document.getElementById('followup_date').value,
        remarks: document.getElementById('followup_remarks').value
    }

    if(validateField(followup_data['time_for_followups']) && validateField(followup_data['date_for_followups']) && validateField(followup_data['remarks'])){

        $.ajax({
            url: 'http://localhost:8000/travel/api/travel_followup_crud',
            type: 'POST',
            data: followup_data,
            success: function(data){
                alertbox.innerHTML = data.message;
                if(data.status == 200){

                    window.location.reload()
                }else{
                    console.log(data);
                }
                window.location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },
        });

    }

}
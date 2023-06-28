var id_for_selection = 0;
var org_store = "";
var client_name_store = "";
var contact_number_store = "";
var selected_country = null;

var processing_dates = {
    collection_date: null,
    courier_out_date: null,
    courier_in_date: null,
    handover_date: null
}

var payment_fees = {
    visa_fees: null,
    authority_service_fees: null,
    express_fees: null,
    vbs_fees: null,
    cgst_fees: null,
    sgst_fees: null
}

function selectedClientID(id, org, client_name, contact_number) {
    id_for_selection = id;
    org_store = org;
    client_name_store = client_name
    contact_number_store = contact_number
}

function clientDetailAutofill() {
    document.getElementById('client_name').innerHTML = client_name_store;
    document.getElementById('applicant_name').setAttribute('value',org_store);
    document.getElementById('contact_number').setAttribute('value',contact_number_store);
}

function setSelectedCountry(obj) {
    selected_country = obj.id;
    console.log(selected_country);
}

function createVisaApplication(csrf_token, id, stage_change) {
    console.log(id);

    passport_number = document.getElementById('passport_number').value;
    sub_location = document.getElementById('sub_location').value;

    alertbox = document.getElementById('alertbox');

    data = {
        csrfmiddlewaretoken: csrf_token,
        "travel_client_ref": parseInt(id_for_selection),
        "employee_ref":parseInt(id),
        "applicants_name": org_store,
        "passport_no":passport_number,
        "contact_number": contact_number,
        "visiting_country":selected_country,
        "sub_location": sub_location
    }

    if(validateField(id_for_selection) && validateField(org_store) && validateField(client_name_store) && validateField(contact_number_store) && validateField(selected_country) && validateField(passport_number)){

        $.ajax({
            url: 'http://localhost:8000/travel/api/travel_visa_stage_1',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrf_token,
                "travel_client_ref": parseInt(id_for_selection),
                "employee_ref":parseInt(id),
                "applicants_name": org_store,
                "passport_no":passport_number,
                "contact_number": contact_number_store,
                "visiting_country":selected_country,
                "sub_location": sub_location
            },
            success: function(data){
                
                alertbox.innerHTML = data.message;
                if(stage_change){
                    window.location.href = '/travel/visa/application/'+data.id+'/document_processing'
                }
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

function markDates(tag, obj) {
    switch (tag) {
        case "collection_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleString();

            obj.style.display = 'none'
            break;
        
        case "courier_out_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleString();

            obj.style.display = 'none'
            break;

        case "courier_in_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleString();

            obj.style.display = 'none'
            break;
        
        case "handover_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleString();

            obj.style.display = 'none'
            break;

        default:
            break;
    }
}


function addToTotal(obj) {

    if(obj.value == ""){
        obj.setAttribute('value',0);
    }

    console.log(obj.value);

    document.getElementById('total_value').innerHTML = parseInt(document.getElementById('total_value').innerHTML) + parseInt(obj.value);

    
}


function name(params) {
    
}


function updateDocumentProcessing(csrf_token, id, stage_change, stage_name) {
    
    vendor_name = document.getElementById('vendor_name').value;
    total_value = document.getElementById('total_value').innerHTML;

    pushable_data = null;
    switch (stage_name) {
        case 'document_processing':
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "vendor_name": vendor_name,
                "document_collection_date":processing_dates['collection_date'],
                "courier_out_date": processing_dates['courier_out_date'],
                "courier_in_date":processing_dates['courier_in_date'],
                "handover_date": processing_dates['handover_date'],
                "app_id": id,
                "stage":stage_name
            }
            break;
        
        case 'payment_processing':
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "visa_fee": payment_fees['visa_fees'],
                "authority_fee":payment_fees['authority_service_fees'],
                "express_charges": payment_fees['express_fees'],
                "vbs_charges":payment_fees['vbs_fees'],
                "total_charges": id,
                "invoice_status":id,
                "app_id": id,
                "stage":stage_name
            }
            break;
    
        default:
            break;
    }

    if(validateField(vendor_name)){
        $.ajax({
            url: 'http://localhost:8000/travel/api/travel_visa_stage_1',
            type: 'PUT',
            data: pushable_data,
            success: function(data){

                
                alertbox.innerHTML = data.message;
                if(stage_change){
                    window.location.href = '/travel/visa/application/'+data.id+'/payment_processing'
                    // console.log(data)
                }
                // window.location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },        
        });
    }

}



 
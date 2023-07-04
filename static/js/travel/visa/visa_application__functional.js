var id_for_selection = 0;
var org_store = null;
var client_name_store = null;
var contact_number_store = null;
var selected_country = null;

var processing_dates = {
    document_collection_date: null,
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

var invoice_status = false;

var visa_status = "pending";


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

function createVisaApplication(csrf_token, id, stage_change, app_id) {
    
    console.log('Entered')

    id_for_selection = id;
    org_store = document.getElementById('applicant_name').value;
    client_name_store = document.getElementById('client_name').innerHTML;
    contact_number_store = document.getElementById('contact_number').value;

    if(Number(app_id) != 0){
        selected_country = document.querySelector('input[name="radio1"]:checked').value;
    }

    console.log(selected_country)
    

    passport_number = document.getElementById('passport_number').value;
    sub_location = document.getElementById('sub_location').value;

    alertbox = document.getElementById('alertbox');


    if(validateField(id_for_selection) && validateField(org_store) && validateField(client_name_store) && validateField(contact_number_store) && validateField(selected_country) && validateField(passport_number)){

        console.log(Number(app_id))

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
                "sub_location": sub_location,
                "stage":"document_processing",
                "id": Number(app_id),
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
                alertbox.innerHTML = "It seems server side error has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },        
        });
    }else{
        alertbox.innerHTML = "org:"+org_store+" clientname: "+client_name_store+" contactno: "+contact_number_store+" selectcntr: "+selected_country+" passportno: "+passport_number;
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
        case "document_collection_date":
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

    payment_fees[obj.id] = obj.value

    prev_total = parseFloat(document.getElementById('total_value').innerHTML) + parseFloat(obj.value);

    payment_fees['cgst_fees'] = prev_total * 0.09

    payment_fees['sgst_fees'] = prev_total * 0.09

    document.getElementById('cgst_fees').value = payment_fees['cgst_fees']

    document.getElementById('sgst_fees').value = payment_fees['sgst_fees']

    document.getElementById('total_value').innerHTML = prev_total + payment_fees['cgst_fees'] + payment_fees['sgst_fees']

    console.log(payment_fees)

    

}


function invoiceStatus(status) {
    invoice_status = status;
}

function visaStatus(status) {
    visa_status = status;
}


function updateDocumentProcessing(csrf_token, id, stage_change, stage_name) {

    var vendor_name = null;
    var total_value = null;

    pushable_data = null;
    switch (stage_name) {
        case 'document_processing':

            vendor_name = document.getElementById('vendor_name').value;

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "vendor_name": vendor_name,
                "app_id": id,
                "stage":stage_name
            }

            for (const [key, value] of Object.entries(processing_dates)) {
                if(value == null){
                    delete (processing_dates[key])
                }
            }

            pushable_data = {...pushable_data, ...processing_dates}
            break;
        
        case 'payment_processing':

            total_value = Number(document.getElementById('total_value').innerHTML);

            console.log(Number(payment_fees['authority_service_fees']).toPrecision(6))
            
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "visa_fee": Number(payment_fees['visa_fees']).toPrecision(5),
                "authority_fee":Number(payment_fees['authority_service_fees']).toPrecision(5),
                "express_charges": Number(payment_fees['express_fees']).toPrecision(5),
                "vbs_charges":Number(payment_fees['vbs_fees']).toPrecision(5),
                "total_charges": Number(total_value).toPrecision(5),
                "invoice_status":invoice_status,
                "app_id": id,
                "stage":stage_name,
                "status": visa_status
            }
            break;
    
        default:
            break;
    }

    if(validateField(vendor_name) || total_value > 0 || validateField(total_value)){
        $.ajax({
            url: 'http://localhost:8000/travel/api/travel_visa_stage_1',
            type: 'PUT',
            data: pushable_data,
            success: function(data){
                alertbox.innerHTML = data.message;
                if(stage_change){
                    if(stage_name == 'payment_processing'){
                        window.location.href = '/travel/visa/application'
                    }else{
                        window.location.href = '/travel/visa/application/'+data.id+'/payment_processing'
                    }
                    
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



 
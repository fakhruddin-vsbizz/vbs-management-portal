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
    visa_fees: 0,
    authority_service_fees: 0,
    express_fees: 0,
    vbs_fees: 0,
    cgst_fees: 0,
    sgst_fees: 0
}

var invoice_status = false;

var visa_status = "pending";


function selectedClientID(id, org, client_name, contact_number) {
    console.log(id)
    id_for_selection = id;
    org_store = org;
    client_name_store = client_name
    contact_number_store = contact_number
}

function clientDetailAutofill() {
    document.getElementById('client_name').innerHTML = client_name_store;
    // document.getElementById('applicant_name').setAttribute('value',org_store);
    document.getElementById('contact_number').setAttribute('value',contact_number_store);
    $(".uk-modal-close").trigger('click');
}

function setSelectedCountry(obj) {
    console.log("obj.id",  obj.id);
    selected_country = obj.id;
    console.log(selected_country);
}

function createVisaApplication(csrf_token, id, stage_change, app_id, client_id, country_visiting) {
    
    console.log('Entered')

    if(client_id != ''){
        id_for_selection = Number(client_id)
    }

    org_store = document.getElementById('applicant_name').value;
    client_name_store = document.getElementById('client_name').innerHTML;
    contact_number_store = document.getElementById('contact_number').value;

    // console.log(document.querySelector('input[name="radio1"]:checked').value);
    // console.log(document.querySelector('input[name="radio1"]').value);

    // if(Number(app_id) != 0){
    //     selected_country = document.querySelector('input[name="radio1"]:checked').value;
    // }

    if (country_visiting !== "") {
        selected_country = country_visiting
    }

    console.log(selected_country)

    passport_number = document.getElementById('passport_number').value;
    sub_location = document.getElementById('sub_location').value;

    alertbox = document.getElementById('alertbox');

    let newStage = "detail processing"

    if(stage_change){

        newStage = "processing documents"

    }

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
                "stage": newStage,
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
        alertbox.innerHTML = "org:"+org_store+" clientname: "+client_name_store+" contactno: "+contact_number_store+" selectcntr: "+selected_country+" passportno: "+passport_number+" id_for_selection"+id_for_selection;
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

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleDateString();

            obj.style.display = 'none'
            break;
        
        case "courier_out_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleDateString();

            obj.style.display = 'none'
            break;

        case "courier_in_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleDateString();

            obj.style.display = 'none'
            break;
        
        case "handover_date":
            processing_dates[tag] = new Date()

            document.getElementById(tag+'_status').innerHTML = 'Marked done on '+processing_dates[tag].toLocaleDateString();

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

    const visa_fees = document.getElementById('visa_fees').value
    const authority_service_fees = document.getElementById('authority_service_fees').value
    const express_fees = document.getElementById('express_fees').value
    const vbs_fees = document.getElementById('vbs_fees').value
    const cgst_fees = document.getElementById('cgst_fees')
    const sgst_fees = document.getElementById('sgst_fees')

    const total = Number(visa_fees) + Number(authority_service_fees) + Number(express_fees) + Number(vbs_fees)

    console.log(total);

    payment_fees['cgst_fees'] = Number((total * 0.09).toFixed(2))
    
    payment_fees['sgst_fees'] = Number((total * 0.09).toFixed(2))

    payment_fees['visa_fees'] = Number(visa_fees)
    payment_fees['authority_service_fees'] = Number(authority_service_fees)
    payment_fees['express_fees'] = Number(express_fees)
    payment_fees['vbs_fees'] = Number(vbs_fees)


    console.log(obj.name, "165");


    document.getElementById('cgst_fees').value = Number((total * 0.09).toFixed(2))

    document.getElementById('sgst_fees').value = Number((total * 0.09).toFixed(2))

    document.getElementById('total_value').innerHTML =( total + payment_fees['cgst_fees'] + payment_fees['sgst_fees']).toFixed(2)

    console.log(payment_fees)

    

}


function invoiceStatus(status) {
    invoice_status = status;
}

function visaStatus(status) {
    visa_status = status;
}


function updateDocumentProcessing(csrf_token, id, stage_change, stage_name, new_stat) {

    var vendor_name = null;
    var total_value = null;

    let newStage = "processing documents"

    if (stage_change) {
        newStage = "processing payments"
    }

    pushable_data = null;
    switch (stage_name) {
        case 'detail processing':

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "app_id": id,
                "stage": 'processing documents'
            }

            break;

        case 'processing documents':

            vendor_name = document.getElementById('vendor_name').value;

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "vendor_name": vendor_name,
                "app_id": id,
                "stage":newStage
            }

            for (const [key, value] of Object.entries(processing_dates)) {
                if(value == null){
                    delete (processing_dates[key])
                }
            }

            pushable_data = {...pushable_data, ...processing_dates}
            break;
        
        case 'processing payments':

            total_value = Number(document.getElementById('total_value').innerHTML);

            const visa_fees = document.getElementById('visa_fees').value
            const authority_service_fees = document.getElementById('authority_service_fees').value
            const express_fees = document.getElementById('express_fees').value
            const vbs_fees = document.getElementById('vbs_fees').value

            const inv_stat = document.getElementsByClassName('uk-active')[0].firstElementChild.textContent

            console.log(inv_stat);

            if (inv_stat === 'Paid') {
                invoice_status = true
            }else{
                invoice_status = false
            }


            const visa_stat = document.getElementsByClassName('uk-active')[1].firstElementChild.textContent

            if (visa_stat === "Rejected") {
                visa_status = 'rejected'
            } else if (visa_stat === "Accepted") {
                visa_status = 'accepted'
            } else {
                visa_status = 'pending'
            }

            const total = Number(visa_fees) + Number(authority_service_fees) + Number(express_fees) + Number(vbs_fees)

            const cgst_fees = Number((total * 0.09).toFixed(2))
            const sgst_fees = Number((total * 0.09).toFixed(2))

            let app_status = 'open'

            if (new_stat !== undefined || new_stat !== "") {
                app_status = new_stat
            }

            console.log(visa_fees,
            authority_service_fees,
                express_fees,
                vbs_fees,
                cgst_fees,
                sgst_fees)
            
            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "visa_fee": Number(visa_fees),
                "authority_fee": Number(authority_service_fees),
                "express_charges": Number(express_fees),
                "vbs_charges": Number(vbs_fees),
                "total_charges": Number(total_value),
                "cgst_fees": Number(cgst_fees),
                "sgst_fees": Number(sgst_fees),
                "invoice_status": invoice_status,
                "app_id": id,
                "stage":stage_name,
                "status": app_status,
                "visa_status": visa_status
            }
            break;


        case 'block_application':

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "app_id": id,
                "status": "blocked"
            }

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

    if(validateField(vendor_name) || total_value > 0 || validateField(total_value) || stage_name == 'unblock_application' || stage_name == 'block_application' || stage_name == 'detail processing'){
        if(stage_name === 'unblock_application'){
            $.ajax({
                url: 'http://localhost:8000/travel/api/travel_visa_stage_1',
                type: 'PUT',
                data: pushable_data,
                success: function(data){
                    alertbox.innerHTML = data.message;
                    if(stage_change && data.status == 200){
    
                        if(stage_name == 'processing payments'){
                            window.location.href = '/travel/visa/application'
                        }else if(stage_name == 'processing documents'){
                            window.location.href = '/travel/visa/application/'+data.id+'/payment_processing'
                        }else{
                            window.location.href = '/travel/visa/application/'+data.id+'/document_processing'
                        }
                        
                        
                    }
                    // window.location.reload();
                },
                error: function(jqXHR, exception){
                    console.log(jqXHR, ' | ', exception);
                    alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
                },
            }).then((response) => {
                updateFollowUpStatus(csrf_token, id)
            }).then((response) => {
                window.location.reload()
            })
            
        }else{
            $.ajax({
                url: 'http://localhost:8000/travel/api/travel_visa_stage_1',
                type: 'PUT',
                data: pushable_data,
                success: function(data){
                    alertbox.innerHTML = data.message;
                    if(stage_change && data.status == 200){
    
                        if(stage_name == 'processing payments'){
                            window.location.href = '/travel/visa/application'
                        }else if(stage_name == 'processing documents'){
                            window.location.href = '/travel/visa/application/'+data.id+'/payment_processing'
                        }else{
                            window.location.href = '/travel/visa/application/'+data.id+'/document_processing'
                        }
                        
                        
                    }
                    // window.location.reload();
                },
                error: function(jqXHR, exception){
                    console.log(jqXHR, ' | ', exception);
                    alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
                },
            });
        }
    }else{
        alertbox.innerHTML = "Please fill the details properly."
    }
}


function createFollowUpVisa(csrf_token, emp_id, app_id) {
    
    followup_data = {
        csrfmiddlewaretoken: csrf_token,
        employee_id: emp_id,
        appl_id: app_id,
        name: document.getElementById('Cname').value,
        contact_number: document.getElementById('contact').value,
        application_type: "visa",
        followup_stage:"in_followups",
        application_status: "blocked",
        time_for_followups: document.getElementById('followup_time').value,
        date_for_followups: document.getElementById('followup_date').value,
        remarks: document.getElementById('followup_remarks').value
    }

    if(validateField(followup_data['time_for_followups']) && validateField(followup_data['date_for_followups']) && validateField(followup_data['remarks'])){

        $.ajax({
            url: 'http://localhost:8000/travel/api/create_follow_ups',
            type: 'POST',
            data: followup_data,
            success: function(data){
                alertbox.innerHTML = data.message;
                if(data.status == 200){
                    // updateDocumentProcessing(csrf_token , app_id, false, 'block_application')
                    // window.location.reload()
                }else{
                    console.log(data);
                }
                // window.location.reload();
            },
            error: function(jqXHR, exception){
                console.log(jqXHR, ' | ', exception);
                alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
            },
        }).then((response) => {
            updateDocumentProcessing(csrf_token , app_id, false, 'block_application')
        }).then((response) => {
            window.location.reload()
        })

    }

}

function updateFollowUpStatus(csrf_token, id){


    pushable_data = {
        csrfmiddlewaretoken: csrf_token,
        "id": id,
        "application_status": "open",
        "application_type": 'visa'
    }

    $.ajax({
        url: 'http://localhost:8000/travel/api/create_follow_ups',
        type: 'PUT',
        data: pushable_data,
        success: function(data){
            alertbox.innerHTML = data.message;
            console.log(data.status);
            // if(stage_change && data.status == 200){
            //     // if(stage_name == 'processing payments'){
            //     //     window.location.href = '/travel/visa/application'
            //     // }else{
            //     //     window.location.href = '/travel/visa/application/'+data.id+'/document_processing'
            //     // }
                
            //     // console.log(data)
            // }
            // window.location.reload();
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },
    });
}
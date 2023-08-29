var customer_details = {
    employee_ref:null,
    travel_client_ref: null,
    package_name: null,
    client_name: null,
    contact_number: null,
    trip_type: null,
    origin: null,
    destination: null,
    via: null,
    mode_of_transport: null,
    stage:'customer_details',
    status:'pending'
}

var transport_details = {
    vehicle_no: null,
    travel_class: null,
    gds_pnr_no: null,
    airline_pnr_no: null,
    departure_date: null,
    arrival_date: null,
    arrival_time: null,
    departure_time:null,
    app_id: null,
    stage:'transport_details',
    status:'pending'
}

var payments = {
    base_fees:null,
    service_fees:null,
    gross_amount:null,
    total_amount:null,
    markup: null,
    issued_from: null,
    agent_ref: null,
    invoice_status:null,
    stage:'payments',
    status:'pending'
}

function selectedClientIDForTickets(id, client_name, contact_number) {
    customer_details['client_name'] = client_name;
    customer_details['travel_client_ref'] = id;
    customer_details['contact_number'] = contact_number;
} 

function clientDetailAutofillForTickets() {
    document.getElementById('client_name').innerHTML = customer_details['client_name'];
    document.getElementById('contact_no').setAttribute('value', customer_details['contact_number'])
    $(".uk-modal-close").trigger('click');
}

function selectTripType(obj) {
    customer_details['trip_type'] = obj.value;
}

function selectOrigin(value) {
    customer_details['origin'] = value;
}

function selectDestinationTicket(value) {
    customer_details['destination'] = value;
}

function selectTransportMode(value) {
    customer_details['mode_of_transport'] = value;
}

function toggleViaBlock(value) {
   var current_city_checked = document.getElementById('via_city_'+value).checked;
   var via_cities = document.getElementById('via').value;
   city_to_remove = via_cities.split(',')

    if(current_city_checked){
        via_cities = ""+via_cities+value+","
        document.getElementById('via').setAttribute('value', via_cities);

        customer_details['via'] = via_cities;

    }else{
        city_to_remove = city_to_remove.filter(function(e) { return e !== value })
        document.getElementById('via').setAttribute('value', city_to_remove.toString());    

        customer_details['via'] = city_to_remove.toString();
    }
}


function createTicketApplication(csrf_token, id, stage_change, app_id, client_id, stage_name) {
    
    var pushable_data = {};

    switch (stage_name) {
        case 'customer_details':
            customer_details['csrfmiddlewaretoken'] = csrf_token;
            customer_details['employee_ref'] = Number(id)
            customer_details['client_name'] = document.getElementById('client_name').innerHTML;
            customer_details['applicants_name'] = document.getElementById('applicants_name').value;
            customer_details['contact_number'] = document.getElementById('contact_no').value;
            customer_details['destination'] = document.querySelector('input[name="destination"]:checked').value;
            customer_details['origin'] = document.querySelector('input[name="origin"]:checked').value;
            customer_details['via'] = document.getElementById('via').value;
            customer_details['trip_type'] = document.getElementById('form-horizontal-select').value;
            customer_details['onwards'] = document.getElementById('onwards').value;
            console.log(customer_details);
            
            // customer_details['mode_of_transport'] = document.querySelector('li[class="uk-active"]').firstChild.innerHTML

            if(app_id != ''){
                customer_details['app_id'] = Number(app_id)
            }

            if(client_id != ''){
                customer_details['travel_client_ref'] = Number(client_id)
            }

            if (stage_change) {
                customer_details['stage'] = 'transport_details'
            }

            pushable_data = customer_details
            break;
    
        case 'transport_details':

            transport_details['vehicle_no'] = document.getElementById('vehicle_no').value;
            transport_details['travel_class'] = document.getElementById('class').value;
            transport_details['gds_pnr_no'] = document.getElementById('gds_pnr').value;
            transport_details['airline_pnr_no'] = document.getElementById('airline_pnr').value;
            transport_details['departure_date'] = document.getElementById('departure_date').value;
            transport_details['departure_time'] = document.getElementById('departure_time').value;
            transport_details['arrival_date'] = document.getElementById('arrival_date').value;
            transport_details['arrival_time'] = document.getElementById('arrival_time').value;
            transport_details['ticket_no'] = document.getElementById('ticket_no').value;
            transport_details['app_id'] = Number(app_id);

            if (stage_change) {
                transport_details['stage'] = 'payments'
            }

            pushable_data = transport_details
            break;
        
        case 'payments':
            let base_fees = document.getElementById('base_fees').value;
            let service_fees = document.getElementById('service_fees').value;

            let gross = Number(Number(base_fees) + Number(service_fees)) + Number((Number(base_fees)+Number(service_fees))*0.18) 

            payments['base_fees'] = Number(Number(document.getElementById('base_fees').value).toPrecision(2));
            payments['service_fees'] = Number(Number(document.getElementById('service_fees').value).toPrecision(2));
            payments['gross_amount'] = gross
            payments['total_amount'] = gross + Number(Number(document.getElementById('markup').value).toPrecision(2));
            payments['markup'] = Number(Number(document.getElementById('markup').value).toPrecision(2));
            payments['issued_from'] = document.getElementById('issued_from').value;
            payments['agent_ref'] = document.getElementById('agent_ref').value;
            payments['entity'] = document.getElementById('entity').value;
            payments['app_id'] = Number(app_id);

            if(stage_change){
                payments['status'] = 'closed'
            }

            console.log(payments);

            pushable_data = payments;
            break;
        
        
        case 'block_application':

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "app_id": app_id,
                "status": "blocked"
            }

            break;

        case 'unblock_application':

            pushable_data = {
                csrfmiddlewaretoken: csrf_token,
                "app_id": app_id,
                "status": "open"
            }

            break;
        

        default:
            break;
    }

    if(stage_name === 'unblock_application'){
    
    $.ajax({
        url: '/travel/api/travel_tickets_crud',
        type: 'POST',
        data: pushable_data,
        success: function(data){
            
            alertbox.innerHTML = data.message;
            page_url = ['customer_details','transport_details','payments']

            if(stage_change && data.status == 200){
                console.log(stage_change);
                if(page_url.indexOf(stage_name) == page_url.length-1){
                    window.location.href = '/travel/tickets/application';
                }else{
                    window.location.href = '/travel/tickets/application/'+data.id+'/'+page_url[page_url.indexOf(stage_name)+1]
                }
            }else{
                // window.location.reload();
            }  
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side error has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },        
    }).then((response) => {
        updateFollowUpStatusForTickets(csrf_token, app_id)
    }).then((response) => {
        window.location.reload()
    })
    
}else{
    $.ajax({
        url: '/travel/api/travel_tickets_crud',
        type: 'POST',
        data: pushable_data,
        success: function(data){
            
            alertbox.innerHTML = data.message;
            page_url = ['customer_details','transport_details','payments']

            if(stage_change && data.status == 200){
                if(page_url.indexOf(stage_name) == page_url.length-1){
                    window.location.href = '/travel/tickets/application';
                }else{
                    window.location.href = '/travel/tickets/application/'+data.id+'/'+page_url[page_url.indexOf(stage_name)+1]
                }
            }else{
                // window.location.reload();
            }  
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side error has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },        
    });
    
}


}


function changeTotalValue() {
    let base_fees = document.getElementById('base_fees').value;
    let service_fees = document.getElementById('service_fees').value;

    console.log(Number((Number(base_fees) + Number(service_fees))*0.18))

    let gross = Number(Number(base_fees) + Number(service_fees)) + Number((Number(base_fees)+Number(service_fees))*0.18)

    document.getElementById('gross_amount').textContent = gross;

    let markup = Number(document.getElementById('markup').value).toPrecision(2);

    let total = Number(gross + Number(markup));

    document.getElementById('total_amount').textContent = total;

    console.log(base_fees,
        service_fees,
        gross,
        markup,
        total);
}


function markInvoiceStatus(invoice_status) {
    payments['invoice_status'] = invoice_status;
}


function createFollowUpForTickets(csrf_token, emp_id, app_id, client_id) {

    console.log(emp_id, app_id)
    
    followup_data = {
        csrfmiddlewaretoken: csrf_token,
        employee_id: emp_id,
        appl_id: app_id,
        name: document.getElementById('Cname').value,
        contact_number: document.getElementById('contact').value,
        application_type: "tickets",
        followup_stage:"in_followups",
        application_status: "blocked",
        time_for_followups: document.getElementById('followup_time').value,
        date_for_followups: document.getElementById('followup_date').value,
        remarks: document.getElementById('followup_remarks').value
    }

    if(validateField(followup_data['time_for_followups']) && validateField(followup_data['date_for_followups']) && validateField(followup_data['remarks'])){

        $.ajax({
            url: '/travel/api/create_follow_ups',
            type: 'POST',
            data: followup_data,
            success: function(data){
                alertbox.innerHTML = data.message;
                if(data.status == 200){

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
            createTicketApplication(csrf_token , emp_id, false, app_id, client_id, 'block_application')
        }).then((response) => {
            window.location.reload()
        })

    }

}

function updateFollowUpStatusForTickets(csrf_token, id){


    pushable_data = {
        csrfmiddlewaretoken: csrf_token,
        "id": id,
        "application_status": "open",
        "application_type": 'tickets'
    }

    $.ajax({
        url: '/travel/api/create_follow_ups',
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
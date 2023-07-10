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
    app_id: null,
    stage:'transport_details',
    status:'pending'
}

var payments = {
    base_fees:null,
    service_fees:null,
    net_amount:null,
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
}

function selectTripType(obj) {
    customer_details['trip_type'] = obj.value;
}

function selectOrigin(value) {
    customer_details['origin'] = value;
}

function selectDestination(value) {
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
            customer_details['employee_ref'] = id
            customer_details['package_name'] = document.getElementById('package_name').value;
            customer_details['client_name'] = document.getElementById('client_name').innerHTML;
            customer_details['contact_number'] = document.getElementById('contact_no').value;
            customer_details['destination'] = document.querySelector('input[name="destination"]:checked').value;
            customer_details['origin'] = document.querySelector('input[name="origin"]:checked').value;
            customer_details['via'] = document.getElementById('via').value;
            customer_details['trip_type'] = document.getElementById('form-horizontal-select').value;
            
            customer_details['mode_of_transport'] = document.querySelector('li[class="uk-active"]').firstChild.innerHTML

            if(app_id != ''){
                customer_details['app_id'] = Number(app_id)
            }

            if(client_id != ''){
                customer_details['travel_client_ref'] = Number(client_id)
            }

            pushable_data = customer_details
            break;
    
        case 'transport_details':

            transport_details['vehicle_no'] = document.getElementById('vehicle_no').value;
            transport_details['travel_class'] = document.getElementById('class').value;
            transport_details['gds_pnr_no'] = document.getElementById('gds_pnr').value;
            transport_details['airline_pnr_no'] = document.getElementById('airline_pnr').value;
            transport_details['departure_date'] = document.getElementById('departure_date').value;
            transport_details['arrival_date'] = document.getElementById('arrival_date').value;
            transport_details['app_id'] = Number(app_id);

            pushable_data = transport_details
            break;
        
        case 'payments':
            payments['base_fees'] = Number(document.getElementById('base_fees').value).toPrecision(6);
            payments['service_fees'] = Number(document.getElementById('service_fees').value).toPrecision(6);
            payments['net_amount'] = Number(document.getElementById('net_total').innerHTML).toPrecision(6);
            payments['markup'] = Number(document.getElementById('markup').value).toPrecision(6);
            payments['issued_from'] = document.getElementById('issued_from').value;
            payments['agent_ref'] = document.getElementById('agent_ref').value;
            payments['app_id'] = Number(app_id);

            pushable_data = payments;

        default:
            break;
    }

    if(stage_name == 'payments' && stage_change){
        pushable_data['status'] = 'closed'
    }
    
    $.ajax({
        url: 'http://localhost:8000/travel/api/travel_tickets_crud',
        type: 'POST',
        data: pushable_data,
        success: function(data){
            
            alertbox.innerHTML = data.message;
            page_url = ['customer_details','transport_details','payments']

            if(stage_change){
                if(page_url.indexOf(stage_name) == page_url.length-1){
                    window.location.href = '/travel/tickets/application';
                }else{
                    window.location.href = '/travel/tickets/application/'+data.id+'/'+page_url[page_url.indexOf(stage_name)+1]
                }
            }else{
                window.location.reload();
            }  
        },
        error: function(jqXHR, exception){
            console.log(jqXHR, ' | ', exception);
            alertbox.innerHTML = "It seems server side error has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
        },        
    });
}


function changeTotalValue() {
    base_fees = document.getElementById('base_fees').value;
    service_fees = document.getElementById('service_fees').value;

    console.log(Number(base_fees+service_fees)*0.18)

    gross = Number(base_fees)+Number(service_fees)+Number(Number(base_fees)+Number(service_fees))*0.18

    document.getElementById('gross_total').innerHTML = gross;

    markup = Number(document.getElementById('markup').value).toPrecision(6);
    
    document.getElementById('net_total').innerHTML = gross+Number(markup);
}


function markInvoiceStatus(invoice_status) {
    payments['invoice_status'] = invoice_status;
}

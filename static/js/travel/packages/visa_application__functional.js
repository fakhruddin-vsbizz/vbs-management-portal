var id_for_selection = 0;
var org_store = "";
var client_name_store = "";
var contact_number_store = "";

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


 
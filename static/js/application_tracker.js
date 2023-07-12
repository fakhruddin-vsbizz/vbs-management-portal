

class followUpStateSwitcher {

    constructor(id, application_type){
        this.DOMId = id;
        this.app_type = application_type
        this.application_id_ref = null;
    }

    startedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('start', id_ref, function(e) {
            console.log(e.originalEvent.detail[1].id);
        });
    }

    stoppedDrag() {
        $(document).on('stopped', '#'+this.DOMId, function(e) {
            console.log('STOPPED'+this.DOMId);
            console.log(e);
        });
    }

    movedDrag() {
        $(document).on('#'+this.DOMId, 'moved', function(e) {
            // console.log(e.detail[1].id)
            console.log('MOVED'+this.DOMId);
            console.log(e);
        });
    }

    addedDrag() {
        var id_ref = '#'+this.DOMId;
        console.log(id_ref)
        $(document).on('added', id_ref, function(e) {

            console.log('chk1');
            
            let followup_id = null;
            followup_id = e.originalEvent.detail[1].id.split('_')[2];

            console.log('chk2');

            $.ajax({
                url: 'http://localhost:8000/travel/api/travel_followup_crud',
                type: 'PUT',
                data: {
                    csrfmiddlewaretoken: '{{ csrf_token }}',
                    'id': followup_id,
                    'followup_stage': e.currentTarget.id
                },
                success: function(data){
                    if(data.status == 200){
                        console.log('chk3');
                        window.location.reload();
                    }else{
                        console.log('chk_fail');
                        console.log(data);
                    }
                    // window.location.reload();
                },
                error: function(jqXHR, exception){
                    console.log('chk_500');
                    console.log(jqXHR, ' | ', exception);
                    alertbox.innerHTML = "It seems server side erro has occured. Try again after some time. Still if problem persist, contact developer@vsbizz.com";
                },
            });

        });
    }

    removedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('removed', id_ref, function(e) {
            console.log('chk_removed');
            console.log(e.originalEvent.detail[1].id);
        });
    }
}



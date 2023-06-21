class followUpStateSwitcher {



    constructor(id){
        this.DOMId = id;
    }

    startedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('start', id_ref, function(e) {
            console.log('START '+this.DOMId);
            console.log(e);
        });
    }

    stoppedDrag() {
        $(document).on('stopped', '#'+this.DOMId, function(e) {
            console.log('STOPPED'+this.DOMId);
            console.log(e);
        });
    }

    movedDrag() {
        $(document).on('moved', '#'+this.DOMId, function(e) {
            console.log('MOVED'+this.DOMId);
            console.log(e);
        });
    }

    addedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('added', id_ref, function(e) {
                console.log('ADDED'+id_ref);
                $(this).find('.uk-margin').map(function() {
                    console.log($(this).find('.uk-card').find('.client_info').html());
                });
            }
        );
    }

    removedDrag() {
        var id_ref = '#'+this.DOMId;
        $(document).on('removed', id_ref, function(e) {
            console.log('ADDED'+id_ref);
                $(this).find('.uk-margin').map(function() {
                    console.log($(this).find('.uk-card').find('.client_info').html());
                });
        });
    }

}


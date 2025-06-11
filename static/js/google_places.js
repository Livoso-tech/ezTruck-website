$.getScript("https://maps.googleapis.com/maps/api/js?key=" + GOOGLE_API_KEY + "&libraries=places")
    .done(function(script, textStatus) {
        google.maps.event.addDomListener(window, "load", initAutocomplete())

    })


let autocomplete_a;
let autocomplete_b;

function initAutocomplete() {

    autocomplete_a = new google.maps.places.Autocomplete(
        document.getElementById('id-google-address-a'), {
            types: ['address'],
            componentRestrictions: { 'country': ['IND'] },
        })

    autocomplete_a.addListener('place_changed', function() {
        onPlaceChanged('a')
    });


    autocomplete_b = new google.maps.places.Autocomplete(
        document.getElementById('id-google-address-b'), {
            types: ['address'],
            componentRestrictions: { 'country': ['IND'] },
        })

    autocomplete_b.addListener('place_changed', function() {
        onPlaceChanged('b')
    });

}
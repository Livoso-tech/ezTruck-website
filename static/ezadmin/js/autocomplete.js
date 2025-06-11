var searchInput = 'search_input';
$(document).ready(function () {
    var autocomplete;
    autocomplete = new google.maps.places.Autocomplete((document.getElementById(searchInput)), {
        types: ['geocode'],
        componentRestrictions: {
            country: "IND"
        }
    });
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var near_place = autocomplete.getPlace();
    });
});
var searchInput1 = 'search_input1';
$(document).ready(function () {
    var autocomplete1;
    autocomplete1 = new google.maps.places.Autocomplete((document.getElementById(searchInput1)), {
        types: ['geocode'],
        componentRestrictions: {
            country: "IND"
        }
    });
    google.maps.event.addListener(autocomplete1, 'place_changed', function () {
        var near_place1 = autocomplete1.getPlace();
    });
});
var searchInput2 = 'search_input2';
$(document).ready(function () {
    var autocomplete2;
    autocomplete2 = new google.maps.places.Autocomplete((document.getElementById(searchInput2)), {
        types: ['geocode'],
        componentRestrictions: {
            country: "IND"
        }
    });
    google.maps.event.addListener(autocomplete2, 'place_changed', function () {
        var near_place2 = autocomplete2.getPlace();
    });
});
var searchInput3 = 'search_input3';
$(document).ready(function () {
    var autocomplete3;
    autocomplete3 = new google.maps.places.Autocomplete((document.getElementById(searchInput3)), {
        types: ['geocode'],
        componentRestrictions: {
            country: "IND"
        }
    });
    google.maps.event.addListener(autocomplete3, 'place_changed', function () {
        var near_place3 = autocomplete3.getPlace();
    });
});

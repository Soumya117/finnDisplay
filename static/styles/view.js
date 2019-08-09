jQuery(function ($) {
  // Asynchronously Load the map API
  var script = document.createElement('script');
  script.src = "//maps.googleapis.com/maps/api/js?key=AIzaSyBoxlPokqwjkKJPfKNtcXdmbbRuZhp4xjo";
  document.body.appendChild(script);

  var script = document.createElement('script');
  script.src = "//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.js";
  document.body.appendChild(script);
});


function hideMap() {
  document.getElementById('realestates_map').style.display = "none";
  document.getElementById('realesates_list').style.display = "block";

  document.getElementById('price_map').style.display = "none";
  document.getElementById('price_list').style.display = "block";

  document.getElementById('sold_map').style.display = "none";
  document.getElementById('sold_list').style.display = "block";

  document.getElementById('visnings_map').style.display = "none";
  document.getElementById('visnings_list').style.display = "block";
}

function showMap() {
  document.getElementById('realestates_map').style.display = "block";
  document.getElementById('realesates_list').style.display = "none";

  document.getElementById('price_map').style.display = "block";
  document.getElementById('price_list').style.display = "none";

  document.getElementById('sold_map').style.display = "block";
  document.getElementById('sold_list').style.display = "none";

  document.getElementById('visnings_map').style.display = "block";
  document.getElementById('visnings_list').style.display = "none";

}

function displayMap(markers, infoWindowContent) {
  initializeArray(markers, infoWindowContent, ['realestates_map', 'price_map', 'sold_map', 'visnings_map']);
}

function initializeArray(markers, infoWindowContent, divIdArray) {
  for (var i = 0; i < markers.length; i++) {
    initialize(markers[i], infoWindowContent[i], divIdArray[i])
  }
}

function initialize(markers, infoWindowContent, divId) {
  var map;
  var bounds = new google.maps.LatLngBounds();
  var mapOptions = {
    mapTypeId: 'roadmap'
  };
  // Display a map on the page
  if (markers.length === 0) return;

  map = new google.maps.Map(document.getElementById(divId), mapOptions);
  map.setTilt(45);

  // Display multiple markers on a map
  var infoWindow = new google.maps.InfoWindow(), marker, i;

  // Loop through our array of markers & place each one on the map
  for (i = 0; i < markers.length; i++) {
    var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
    bounds.extend(position);
    marker = new google.maps.Marker({
      position: position,
      map: map,
      title: markers[i][0]
    });

    // Allow each marker to have an info window
    google.maps.event.addListener(marker, 'click', (function (marker, i) {
      return function () {
        infoWindow.setContent(infoWindowContent[i]);
        infoWindow.open(map, marker);
      }
    })(marker, i));

    // Automatically center the map fitting all markers on the screen
    map.fitBounds(bounds);
  }

  // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
  var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function (event) {
    this.setZoom(14);
    google.maps.event.removeListener(boundsListener);
  });
}

function toggleGraph() {
  var x = document.getElementById("graph");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function toggleReports() {
  var x = document.getElementById("reports");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function viewData(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

function changeView() {
  var option = document.getElementById("mySelect").value;
  if (option === 'list') {
    hideMap();
  }
  else {
    showMap()
  }
}

$(document).ready(function () {
  changeView()
  document.getElementById("date").addEventListener("change", function () {
    var req = new XMLHttpRequest();

    var markers = [];
    var info = [];

    var markers_links = [];
    var info_links = [];

    var markers_price = [];
    var info_price = [];

    var markers_sold = [];
    var info_sold = [];

    var markers_visnings = [];
    var info_visnings = [];

    req.onreadystatechange = function () {

      if (this.readyState == 4 && this.status == 200) {

        var result = JSON.parse(this.responseText);

        markers_links = result['links']['map']['markers'];
        info_links = result['links']['map']['info'];

        markers_price = result['price']['map']['markers'];
        info_price = result['price']['map']['info'];

        markers_sold = result['sold']['map']['markers'];
        info_sold = result['sold']['map']['info'];

        markers_visnings = result['visnings']['map']['markers'];
        info_visnings = result['visnings']['map']['info'];

        links = result['links']['table']
        price = result['price']['table']
        sold = result['sold']['table']
        visnings = result['visnings']['table']

        $('#realesates_list').append(links)
        $('#price_list').append(price)
        $('#sold_list').append(sold)
        $('#visnings_list').append(visnings)
      }
    };

    req.open('POST', '/status', false);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("date=" + this.value);

    markers.push(markers_links);
    markers.push(markers_price);
    markers.push(markers_sold);
    markers.push(markers_visnings);

    info.push(info_links);
    info.push(info_price);
    info.push(info_sold);
    info.push(info_visnings);

    displayMap(markers, info)
  });
});

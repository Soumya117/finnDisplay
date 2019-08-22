jQuery(function ($) {
  // Asynchronously Load the map API
  var script = document.createElement('script');
  script.src = "//maps.googleapis.com/maps/api/js?key=AIzaSyBoxlPokqwjkKJPfKNtcXdmbbRuZhp4xjo";
  document.body.appendChild(script);

  var script = document.createElement('script');
  script.src = "//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.js";
  document.body.appendChild(script);
});

function hideMap(div) {

  if( !$('#'+div+'_list').is(':empty') )
  {
    document.getElementById(div+'_list').style.display = "block";
  }
  document.getElementById(div+'_map').style.display = "none";
}

function showMap(div) {

  if( !$('#'+div+'_map').is(':empty') )
  {
    document.getElementById(div+'_map').style.display = "block";
  }
  document.getElementById(div+'_list').style.display = "none";
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

function toggle(div_id) {
  var x = document.getElementById(div_id);
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

function changeView(id) {
  var option = document.getElementById(id+'_mySelect').value;
  if (option === 'list') {
    hideMap(id);
  }
  else {
    showMap(id)
  }
}

function callback(result, id) {
  var markers = [];
  var infos = [];

  marker = result[id]['map']['markers'];
  info = result[id]['map']['info'];

  table = result[id]['table'];

  var div_list = '#'+id+'_list';
  var div_map = '#'+id+'_map';

  $(div_list).empty();
  $(div_map).empty();
  document.getElementById(id+'_map').style.display = "none";

  $(div_list).append(table);

  markers.push(marker);
  infos.push(info);

  initialize(marker, info, id+'_map');
}

function registerListener(id) {
  document.getElementById(id+"_date").addEventListener("change", function () {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
        var result = JSON.parse(this.responseText);
        callback(result, id);
        document.getElementById(id+'_date').disabled = false;
        document.getElementById(id+'_mySelect').disabled = false;
        document.getElementById('loading_'+id).style.display = "none";
      }
    };
    document.getElementById('loading_'+id).style.display = "block";
    document.getElementById(id+'_date').disabled = true;
    document.getElementById(id+'_mySelect').disabled = true;
    req.open('POST', '/status/'+id);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("date=" + this.value);
  });
}

function loadPrices(id)
{
   var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
        var result = JSON.parse(this.responseText);
        callback(result, id);
        document.getElementById(id+'_mySelect').disabled = false;
      }
    };
    document.getElementById(id+'_mySelect').disabled = true;
    req.open('POST', '/status/'+id);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send("date=" + this.value);
}

$(document).ready(function () {
  var div_ids = ['visnings', 'sold', 'realestates'];
  div_ids.forEach(changeView);
  div_ids.forEach(registerListener);

  // set today's date for visnings.
  var today = new Date().toISOString().split("T")[0];
  document.getElementById("visnings_date").setAttribute("min", today);
  document.getElementById("sold_date").setAttribute("max", today);

  //call price changes anyways
  changeView('price');
  loadPrices('price');
});

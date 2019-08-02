def jsonToHtml():
    html="""
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
.tab {{
  overflow: hidden;
  border: 1px solid #ccc;
}}
.tabcontent {{
  animation: fadeEffect 1s; /* Fading effect takes 1 second */
}}

/* Go from zero to full opacity */
@keyframes fadeEffect {{
  from {{opacity: 0;}}
  to {{opacity: 1;}}
}}
.tab button {{
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  background-color: #3d5c5c;
  font-size: 120%;
  color: #000000;
  font-weight: 700;
}}
.tab button:hover {{
  background-color: #ddd;
}}
h1 {{
  background-color: #3d5c5c;
  color: #e6f3ff
 }}
.tab button.active {{
  background-color: #ccc;
}}
.tabcontent {{
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
  max-height: 300px;
  overflow-y: scroll;
}}
#graph {{
}}
</style>
  <title>Finn RealEstate Data</title>
  <h1>Finn Data</h1>
</head>
<body bgcolor="#001a33">
<div id="graph">
  <img src="data:image/png;base64, {plot_url_links}" style="margin-right:300px;margin-left:100px;">
  <img src="data:image/png;base64, {plot_url_sold}">
</div>
<h1>Mining Reports</h1>
<div class="tab">
  <button class="tablinks" onclick="openCity(event, 'RealEstates')">RealEstates Added</button>
  <button class="tablinks" onclick="openCity(event, 'Price')">Price Ups And Downs</button>
  <button class="tablinks" onclick="openCity(event, 'Sold')">RealEstates Sold</button>
</div>

<div id="RealEstates" class="tabcontent">
{realestates}
<span onclick="this.parentElement.style.display='none'">x</span> 
</div>

<div id="Price" class="tabcontent">
{price}
<span onclick="this.parentElement.style.display='none'">x</span> 
</div>

<div id="Sold" class="tabcontent">
{soldHouses}
<span onclick="this.parentElement.style.display='none'">x</span> 
</div>

<script>
function openCity(evt, cityName) {{
  console.log("Calling open city..")
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {{
    tabcontent[i].style.display = "none";
  }}
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {{
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }}
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}}
</script>
</body>
</html>"""
    return html

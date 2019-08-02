def jsonToHtml():
    html="""
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
.tab {{
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
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
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}}
.tab button:hover {{
  background-color: #ddd;
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
</style>
  <title>Finn RealEstate Data</title>
  <h2>Finn Data</h2>
</head>
<body>
<div id="graph">
  <img src="data:image/png;base64, {plot_url_links}">
  <img src="data:image/png;base64, {plot_url_sold}">
</div>
<h2>Mining Reports</h2>
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
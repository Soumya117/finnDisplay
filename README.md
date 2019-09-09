# Python Flask App to present finn.no data.

This app uses the data stored by #finnazureflaskapp. On load, it queries the Azure Storage Blob for data and presents a 
graphical representation. It also shows the overall data collected from finn in the tables below. 

The app has two views: List view and map view. User can select between these views. Uses google maps api to fetch the geocode location of the address and then marks and displays the google maps.

It displays the following:

Graph
1. Statistics of realestates added.
2. Statistics of realestates sold.

Reports
1. Realestates added that day.
2. Price Changes for the same house.
3. Houses sold on that day.
4. Visnings added.

DEPLOYMENT

The app is now deployed on google cloud.
Browse link: http://finn117.appspot.com/


Sample Graph

![alt text](https://github.com/Soumya117/finnDisplay/blob/master/sold.png) <br /><br />



![alt text](https://github.com/Soumya117/finnDisplay/blob/master/realstatepng.png)



<br />

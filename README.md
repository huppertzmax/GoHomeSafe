# GoHomeSafe

>  "Roughly 6 in 10 South Korean women in their 20s and 30s feel unsafe in the streets at night [...]"
> - http://koreabizwire.com/majority-of-young-korean-women-feel-unsafe-at-night/178066

GoHomeSafe is a safety application that provides the most secure routes based on the existence of CCTV cameras along 
the route for residents in Daejeon (South Korea), particularly women. 

This repository contains the server-side code of GoHomeSafe. The client-side mobile application can be found at 
[GoHomeSafe_Mobile](https://github.com/huppertzmax/GoHomeSafe_Mobile)

## Installation
The server-side of GoHomeSafe is a Python Flask server. 

Follow the following steps to install and run the server: 

1. Install all the requirements for the project: `pip install -r requirements.txt`
2. Navigate to GoHomeSafe/app
3. Run the application `python3 -m flask run --host=0.0.0.0`
--host=0.0.0.0 allows to later access the server with the mobile application on another device (remove this option if 
the server should be only accessible via localhost) 

## Usage

Once the Flask application is running, four endpoints become accessible. These endpoints facilitate the calculation of 
either the safest or fastest route, retrieval of all CCTV camera locations, or retrieval of locations within a specified 
area. The [GoHomeSafe_Mobile](https://github.com/huppertzmax/GoHomeSafe_Mobile) mobile application utilizes all of these
endpoints to visualize the results.

For instance, to request the safest route from a designated starting point (specified by latitude and longitude values)
to an endpoint (also specified by latitude and longitude values), a GET request can be made. An example request URL is 
as follows (with coordinates provided solely for demonstration purposes):
`http://127.0.0.1:5000/route?start_lat=36.363398&start_lon=127.366698&end_lat=36.339342&end_lon=127.394470`

Keep in mind that the current version only works in Daejeon, South Korea and the points therefore have to be in Daejeon.


## Background of the project 
The project represents the result of my term project undertaken within the Services Computing course at the Korea 
Advanced Institute of Science & Technology. 

## Warning

This project constitutes a proof of concept aimed at leveraging technology to augment safety in daily life. It is expressly
stated that there is no warranty or guarantee regarding the actual safety of the routes provided within real-world 
scenarios. The designation of routes as "safest" is predicated upon optimization strategies that prioritize the inclusion 
of a maximum number of closed-circuit television (CCTV) cameras, while minimizing any significant increase in route length.
It is important to note, however, that such routes are not guaranteed to be completely safe and are only considered 
potentially safer. 
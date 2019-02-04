		//set up markers
		var myMarkers = {"markers": [
				{"latitude": "34.0671741", "longitude":"74.7525609", "icon": "/static/img/map-marker.png"}
			]
		};

		//set up map options
		$("#map").mapmarker({
			zoom	: 14,
			center	: 'Hotel Rose Petal, 56, Rajbagh, Opp. IHM Srinagar, Srinagar, Jammu and Kashmir 190008',
			markers	: myMarkers
		});

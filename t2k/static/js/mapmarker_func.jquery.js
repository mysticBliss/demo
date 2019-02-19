		//set up markers
		var myMarkers = {"markers": [
				{"latitude": "34.067194", "longitude":"74.82260099999996", "icon": "/static/img/map-marker.png"}
			]
		};

		//set up map options
		$("#map").mapmarker({
			zoom	: 14,
			center	: 'Hotel Rose Petal, 56, Rajbagh, Opp. IHM Srinagar, Srinagar, Jammu and Kashmir 190008',
			markers	: myMarkers
		});

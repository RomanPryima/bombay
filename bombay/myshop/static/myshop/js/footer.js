function initMap() {
	document.getElementById('map').style.height = "16em"
	document.getElementById('map').style.width = "100%"
  var pos = {lat: 49.836431, lng: 24.030665};
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 17, center: pos});
  var marker = new google.maps.Marker({position: pos, map: map, title: document.getElementById('marker-name').textContent});
  marker.setAnimation(google.maps.Animation.BOUNCE);
}

var $button = document.querySelector('.btn-contactus');
$button.addEventListener('click', function() {
	$( "#contactus-place" ).load( "/contact" );
  var duration = 0.3,
      delay = 0.08;
  TweenMax.to($button, duration, {scaleY: 1.6, ease: Expo.easeOut});
  TweenMax.to($button, duration, {scaleX: 1.2, scaleY: 1, ease: Back.easeOut, easeParams: [3], delay: delay});
  TweenMax.to($button, duration * 1.25, {scaleX: 1, scaleY: 1, ease: Back.easeOut, easeParams: [6], delay: delay * 3 });
});




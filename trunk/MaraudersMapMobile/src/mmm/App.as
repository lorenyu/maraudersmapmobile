import mmm.*;
import mx.transitions.Tween;
import mx.transitions.easing.None;

class mmm.App extends MovieClip
{
	// MovieClips
	var userIcon:MovieClip = null;
	var targetIcon:MovieClip = null;
	var map:Map = null;
	
	var gpsX:Number = 700;
	var gpsY:Number = 1100;
	var compassDirection:Number = 0; // in degrees (x-axis is 0)
	var timer:Object = null;
	var turn:Number = 0; // TODO: remove
	
	public function App()
	{
		trace("App started");
		
		Key.addListener(this);
		
		userIcon = this.attachMovie("UserIcon", "userIcon", 999);
		userIcon._x = this._width / 2;
		userIcon._y = this._height / 2;
		
		// Create new instance of Map with instance name "map" at depth 100
		map = Map(this.attachMovie("Map", "map", 100));
		//map = attachMovie("Map", "map", 100);
		
		run();
	}
	
	public function run()
	{
		trace("run");
		updateLocation();
		loadMap();
		
		// Need to pass this as an argument since setInterval(this, update, 500) doesn't work for Flash Lite 2.0
		//timer = setInterval(update, 500, this);
	}
	
	public function update(_this:MovieClip)
	{
		trace("update");
		_this.updateLocation();
		_this.updateMap();
	}
	
	public function updateLocation()
	{
		if (turn >= 10)
		{
			compassDirection += 3;
			turn = 0;
		}
		else
		{
			turn++;
		}

		gpsX += 2 * Math.cos(compassDirection * Math.PI / 180);
		gpsY += 2 * Math.sin(compassDirection * Math.PI / 180);
		
		trace("new coords = (" + gpsX + "," + gpsY + "," + compassDirection + ")");
	}
	
	public function updateMap()
	{
		//this.map.updateDisplay(this.gpsX, this.gpsY, this.compassDirection);
		
		var u:Number = gpsX - map.gpsXMin;
		var v:Number = map.gpsYMax - gpsY;
		var theta:Number = compassDirection * Math.PI / 180;
		var dx:Number = v*Math.cos(theta) + u*Math.sin(theta);
		var dy:Number = -u*Math.cos(theta) + v*Math.sin(theta);
		
		map._x = userIcon._x - dx;
		map._y = userIcon._y - dy;
		// In actionscript, positive angles represent clockwise rotation
		map._rotation = -90 + compassDirection;
		
		trace("new coords = (" + map._x + "," + map._y + "," + map._rotation + ")");
	}
	
	public function loadMap()
	{
		trace("loadMap tressider");
		map.loadMap("tressider");
	}
	
	public function onKeyDown()
	{
		switch(Key.getCode())
		{
			case Key.UP:
				gpsX += 2 * Math.cos(compassDirection * Math.PI / 180);
				gpsY += 2 * Math.sin(compassDirection * Math.PI / 180);
				break;
		
			case Key.DOWN:
				gpsX -= 2 * Math.cos(compassDirection * Math.PI / 180);
				gpsY -= 2 * Math.sin(compassDirection * Math.PI / 180);
				break;
				
			case Key.LEFT:
				compassDirection += 3; // or 5!
				if(compassDirection >= 360) compassDirection -= 360;
				break;
				
			case Key.RIGHT:
				compassDirection -= 3;
				if(compassDirection <= 0) compassDirection += 360;
				break;
		}
		this.updateMap();
	}
		
}
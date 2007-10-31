import mmm.*;
import mx.transitions.Tween;
import mx.transitions.easing.None;

class mmm.Map extends MovieClip
{
	var gpsXMin:Number;
	var gpsYMin:Number;
	var gpsXMax:Number;
	var gpsYMax:Number;
	
	public function Map()
	{
		trace("Map contructor");
		this._xscale = 200.0; // in percent
		this._yscale = 200.0; // in percent
	}

	public function loadMap(map:String)
	{
		var clipLoader:MovieClipLoader = new MovieClipLoader();
		var listener:Object = new Object();
		listener.onLoadInit = function(target:MovieClip)
		{
			trace("loading map");
			// TODO: do this properly
			target.gpsXMin = 0;
			target.gpsYMin = 0;
			target.gpsXMax = target._width;
			target.gpsYMax = target._height;
			target._parent.update();
			trace("gpsX: [" + target.gpsXMin + "," + target.gpsXMax + "]");
			trace("gpsY: [" + target.gpsYMin + "," + target.gpsYMax + "]");
		}
		clipLoader.addListener(listener);
		// params: address, target movie to load to
		clipLoader.loadClip("resources/" + map + "-medquality.jpg", this);
	}

	/*
	public function updateDisplay(gpsX:Number, gpsY:Number, compassDirection:Number)
	{
		trace("update display");

		var u:Number = gpsX - this.gpsXMin;
		var v:Number = gpsYMax - gpsY;
		var theta:Number = compassDirection * Math.PI / 180;
		var dx:Number = v*Math.cos(theta) + u*Math.sin(theta);
		var dy:Number = -u*Math.cos(theta) + v*Math.sin(theta);
		
		this._x = this._parent.userIcon._x - dx;
		this._y = this._parent.userIcon._y - dy;
		// In actionscript, positive angles represent clockwise rotation
		this._rotation = -90 + theta;
	}
	*/
}
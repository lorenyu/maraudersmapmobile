import mmm.*;
import mx.transitions.Tween;
import mx.transitions.easing.None;

class mmm.App extends MovieClip
{
	var myText:TextField;
	
	public function App()
	{
		trace("Hello, world!");
		this.myText.text = "Hello, Marcia!";
		this.myText._x = 100;
		this.myText._rotation = 90;
	}
}
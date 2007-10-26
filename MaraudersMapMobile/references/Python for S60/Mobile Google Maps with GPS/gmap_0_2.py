<html>
<head>
<base href="http://www.gmaptrack.com" />

<title>Python application for Nokia phones</title>

<meta id="metaDescription" name="description" content="A demonstration Python application for Nokia phones that links a 
# Bluetooth GPS to retrieve and display Google Maps in realtime"></meta>
		<meta id="metaKeywords" name="keywords" content="python application, nokia python application, bluetooth gps, nokia python sdk"></meta>
<link rel="stylesheet" type="text/css" href="http://web.archive.org/web/20051212055648/http://www.gmaptrack.com/gmaptrack.css">

<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAY8f9EudoyhAiFGcQMMf_ShTjKjj-p5k_a9zXse2GaHZX7ULU2xQNgP07pC1FlE2H7FhKeEUaD1EN4g"
      type="text/javascript"></script>
    <script type="text/javascript">
    //<![CDATA[
    function load() {
      if (GBrowserIsCompatible()) {
        var map = new GMap2(document.getElementById("map"));
        map.setCenter(new GLatLng(40.714, -74.006), 13);
      }
    }
    //]]>
    </script>

</head>
<body>
<table id="container" width="95%">
<span>
<tr><td id="logo" width="95%">
<span>
	<a href="http://www.gmaptrack.com/">
	<img src="http://d1862092.u34.whsecure.net/gmaptracklogo.gif" width="230" height="51" longdesc="../Google Maps"></a><a href="http://www.tkqlhce.com/ec106r09608ORSXQYYQOQPSYUTUW" target="_blank" onmouseover="window.status='http://www.travelocity.com';return true;" onmouseout="window.status=' ';return true;">
<img src="http://www.lduhtrp.net/c581y7B-53PSTYRZZRPRQTZVUVX" alt="" border="0"/></a></span></td></tr>
<tr><td id="topnav" colspan="2">
	<p style="text-align: center"><font color="#FFFFFF">PYTHON APPLICATION</font></td>
</tr>
</span>

<tr>
<td id="mainleft" width="89%">
<table border="1" width="100%" id="table1">
	<tr>
		<td><script type="text/javascript"><!--
google_ad_client = "pub-3805447958177994";
google_ad_width = 160;
google_ad_height = 600;
google_ad_format = "160x600_as";
google_ad_type = "text";
//2007-04-11: Gmaptrack
google_ad_channel = "4012762423";
google_color_border = "FFFFFF";
google_color_bg = "FFFFFF";
google_color_link = "0000FF";
google_color_text = "000000";
google_color_url = "008000";
//-->
</script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script><br>
<script type="text/javascript"><!--
google_ad_client = "pub-3805447958177994";
google_ad_width = 160;
google_ad_height = 600;
google_ad_format = "160x600_as";
google_ad_type = "text";
//2007-04-11: Gmaptrack
google_ad_channel = "4012762423";
google_color_border = "FFFFFF";
google_color_bg = "FFFFFF";
google_color_link = "0000FF";
google_color_text = "000000";
google_color_url = "008000";
//-->
</script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
</td>
		<td>
		<pre># gmap.py
#
# License : GPL
# http://www.gnu.org/copyleft/gpl.html
# (c) Rhys Jones 2005
# rhys.jones@calso.co.uk
#
# A demonstration Python application for Nokia phones that links a 
# Bluetooth GPS to retrieve and display Google Maps in realtime.
# It is very limited, and will only show 30 or so map tiles before
# giving a system error since too many Content_handlers are open.
# The next release of the Nokia Python sdk should allow better UI
# and graphics capabilities, such as:
#
# - overlaying current position on map tile
# - rotate and centre tiles to current GPS heading
# - background downloading of adjacent tiles
# - incorporate speed, position, satellites, etc. in UI
# 
# Thanks to:
# Google Map info:
# http://jgwebber.blogspot.com/2005/02/mapping-google.html
# Bluetooth and GPS info:
# http://www.postneo.com/postwiki/moin.cgi/PythonForSeries60


import appuifw
import urllib
import e32
import socket
import time

class App:
    def __init__(self):
        self.currentURL=None
        self.optionList = ({'start':u'Start'},{'exit':u'Exit'})
        self.lock = e32.Ao_lock()
        self.old_exit_key = appuifw.app.exit_key_handler
        appuifw.app.exit_key_handler = self.exit_handler
        self.current_tab = 0
        appuifw.app.set_tabs([u'Google Maps GPS'], self.display_tab)
        self.display_tab(0)
        self.lock.wait()

    def exit_handler(self):
        self.lock.signal()

    def display_tab(self, id):
        appuifw.app.body = appuifw.Listbox(self.optionList[id].values(), self.load)
        self.current_tab = id

    def load(self):
        haveFix=0
        latitude_in=0
        longitude_in=0
        
        self.sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
        address,services=socket.bt_discover()
        target=(address,services.values()[0]) 
        self.sock.connect(target)

        while 1:
            buffer=&quot;&quot;
            ch=self.sock.recv(1)
            while(ch!='$'):
              ch=self.sock.recv(1)
            while 1:
                if (ch=='\r'):
                    break
                buffer+=ch
                ch=self.sock.recv(1)
            if (buffer[0:6]==&quot;$GPGGA&quot;):
                try:
                    (GPGGA,utcTime,lat,ns,lon,ew,posfix,sats,hdop,alt,altunits,sep,sepunits,age,sid)=buffer.split(&quot;,&quot;)
                    latitude_in=float(lat)
                    longitude_in=float(lon)
                    haveFix=int(posfix)
                except:
                    haveFix=0

                if haveFix:
                    zoom=2
                    if ns == 'S':
                        latitude_in = -latitude_in
                    if ew == 'W':
                        longitude_in = -longitude_in

                    latitude_degrees = int(latitude_in/100)
                    latitude_minutes = latitude_in - latitude_degrees*100

                    longitude_degrees = int(longitude_in/100)
                    longitude_minutes = longitude_in - longitude_degrees*100

                    latitude = latitude_degrees + (latitude_minutes/60)
                    longitude = longitude_degrees + (longitude_minutes/60)

                    x=int(int((longitude + 98.35) * (131072 &gt;&gt; zoom) * 0.77162458338772) / 128);
                    y=int(int((39.5 - latitude) * (131072 &gt;&gt; zoom)) / 128);

                    url = &quot;http://mt.google.com/mt?v=.1&amp;x=%s&amp;y=%s&amp;zoom=%s&quot;%(x, y, zoom)

                    if url!=self.currentURL:
                        try:
                            id = appuifw.app.body.current()
                            urllib.urlretrieve(url, &quot;C:\\gmap.jpg&quot;)
                            # Need to close previous image here...
                            content_handler = appuifw.Content_handler()
                            content_handler.open(&quot;C:\\gmap.jpg&quot;)
                        except IOError:
                            appuifw.note(u&quot;Could not fetch the map.&quot;,'info')
                        except Exception, E:
                            appuifw.note(u&quot;Could not open the map, %s&quot;%E,'info')
                        self.currentURL=url

            time.sleep(0.2)

A = App()
 
</pre>
		<p style="text-align: center">
		<body onload="load()" onunload="GUnload()">
    	</td>
	</tr>
	</table>
</center></td>


</tr>

<span>
<tr id="foot">
<td id="copy" bgcolor="#445782" width="99%">
<p>
<span class="sep"></span>
<!--a href="http://www.gmaptrack.com/privacy.html" target="new">Privacy Policy</a-->&nbsp;
</p>
<p>
<span class="sep"></span>
<font color="#FFFFFF">Copyright &copy; 1997-2007 gmaptrack.com</font></p>
</td>

<td id="corp" bgcolor="#445782" width="1%"> 
<p class="nav">
&nbsp;</p>
</td>
</tr>
</span>

</table>

</body>



</html>
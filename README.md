# ORPHEUS - a simple streaming client

<p>The following setup runs smooth and is tested on a raspberry pi 4
<br>The project requires mpd, mpc and nginx</p>

<p>The raspberry pi will play the audio signal from a public streaming url<br>
A simple status overview is indicated on a web site</p>
<br>
<p>Install Raspberry Pi OS using the Raspberry Pi Imager or Balena Etcher</p>

Connect via ssh
-> hardening the access via ssh-key is recommended

Update your raspberry:

	sudo apt-get update
	sudo apt-get upgrade

<h3>Installlation and Configuration of MPD, MPC</h3>
Install MPD and MPC:
	
	sudo apt install mpd mpc

Configure the audio output in the mpd.conf - Config file:
	
	sudo nano /etc/mpd.conf 

	audio_output {
	        type            "alsa"
	        name            "My ALSA Device"
	        device          "hw:0,0"        # optional
	        mixer_type      "hardware"      # optional
	        mixer_device    "default"       # optional
	        mixer_control   "PCM"           # optional
	        mixer_index     "0"             # optional
	}
	

Create the Playlist File.m3u:

	sudo nano /var/lib/mpd/playlists/playlist_name.m3u

Write the following code into the file:
	
	#EXTM3U
	#EXTINF:-1, "Playlist Name"
	http://0008E1087ACE:0008E1087ACE@playlist.com/V1026.mp3
	
Alsa Config:<br>
Source: https://strobelstefan.de/blog/2021/01/22/raspberry-pi-musik-auf-der-stereoanlage-wiedergeben/#npcm-client-fur-die-konsole

	sudo modprobe snd_bcm2835
	sudo alsamixer cset numid=3 1

Activate and start the service:

  	sudo systemctl enable mpd
	sudo systemctl start mpd

Load the playlist:

	mpc load playlist_name

Start the player:

	mpc play

<h3>Note:</h3>
If you are using Wifi, the wifi connection has to be established before the stream starts otherwhise it will run into an error 'cause the url cannot be resolved (no internet connection)
therefore i've delayed the start of the mpd.service for 30sec

Edit the mpd.service - Service file:

	sudo nano /lib/systemd/system/mpd.service
	
Add the following line to SERVICE:

	ExecStartPre=/bin/sleep 30

<h3>Installation and Configuration of NGINX (engineX)</h3>

Install nginx:

	sudo apt install nginx

Creating the website:

	cd /var/www
	sudo mkdir orpheus
	cd orpheus
	sudo nano index.html

Setting up the virtual host:

 	cd /etc/nginx/sites-enabled
	sudo nano orpheus

Content of the newly created file:

	server {
       		listen 81;
       		listen [::]:81;

		server_name localhost;

       		root /var/www/orpheus;
       		index index.html;

	       location / {
        	       try_files $uri $uri/ =404;
       		}
	 }

Activate the virtual host:

	sudo service nginx restart

The website will be reachable under ip-from-raspberrypi:81


<h3>Installation and Configuration of MPC Status Website</h3>

Install Python

	sudo apt install python3 python3-pip

Move to the directory where you want to have the script (in the given example it's /home/admin/orpheus)

Clone the orpheus project from Git

	git clone https://github.com/Spiel0r/orpheus.git

 Add the python script to the crontab - file

	sudo crontab -e

The line says execute the python script every minute.
It will be executed every minute and adds the date of execution as well as the output of the script into a log file:

 	* * * * * echo "$(date) - Ausführung von mpc_status.py" >> /home/admin/orpheus/mpc_status.log && /usr/bin/python3 /home/admin/orpheus/mpc_status.py >> /home/admin/orpheus/mpc_status.log 2>&1

The python script does the following:
It will print the output of "mpc status" and "systemctl status mpd" as well as the current date into a generated index.html file which will be accessible via web browser

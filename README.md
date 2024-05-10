# ORPHEUS - a simple streaming client

<p>The following instruction runs and is tested on a raspberry pi 4
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

Activate and start the service

  	sudo systemctl enable mpd
	sudo systemctl start mpd


Load the playlist:

	mpc load playlist_name

Start the player:

	mpc play

If you are using Wifi, the wifi connection has to be established before the stream starts otherwhise it will run into an error 'cause the url cannot be resolved (no internet connection)
therefore i've delayed the start of the mpd.service for 30sec

Edit the mpd.service - Service file:

	sudo nano /lib/systemd/system/mpd.service
	
Add the following line to SERVICE

	ExecStartPre=/bin/sleep 30


ToDo for me:
Write instruction for nginx website and python mpc status update script

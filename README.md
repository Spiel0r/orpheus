# orpheus is a simple streaming client

the following instruction runs and is tested on a raspberry pi 4
the project requires mpd, mpc and nginx

The raspberry pi will play the audio signal from a public streaming url
A simple status overview is indicated on a web site

########################################################################
########################################################################
Install Raspberry Pi OS using the Raspberry Pi Imager or Balena Etcher

Connect via ssh
-> hardening the access via ssh-key is recommended

Update the Software

	sudo apt-get update
	sudo apt-get upgrade

Install MPD and MPC
	
	sudo apt install mpd mpc

Configure output in mpd.conf
	
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
	

Create the Playlist File.m3u
	sudo nano /var/lib/mpd/playlists/playlist_name.m3u


	Inhalt der Datei:
	#EXTM3U
	#EXTINF:-1, "Playlist Name"
	http://0008E1087ACE:0008E1087ACE@roomvibes2.com/V1026.mp3
	

Alsa Config:
Source:
https://strobelstefan.de/blog/2021/01/22/raspberry-pi-musik-auf-der-stereoanlage-wiedergeben/#npcm-client-fur-die-konsole

	sudo modprobe snd_bcm2835
	sudo alsamixer cset numid=3 1

Activate and start the service

  sudo systemctl enable mpd
  sudo systemctl start mpd


Load the playlist
	mpc load martinauerroomvibes

Start the player

	mpc play

If you are using Wifi, the wifi connection has to be established before the stream starts otherwhise it will run into an error
therefore if delayed the start of the mpd.service for 30sec

	sudo nano /lib/systemd/system/mpd.service
	
	SERVICE um folgende Zeile ergänzt
	ExecStartPre=/bin/sleep 30
![image](https://github.com/Spiel0r/orpheus/assets/168893268/e8be7465-f65e-4b57-91c9-74317d77a5d7)


ToDo:
Write instruction for nginx website and python mpc status update script

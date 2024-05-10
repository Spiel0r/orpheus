#!/usr/bin/env python3

import subprocess
from datetime import datetime

# Funktion, um den Output von `mpc status` abzurufen
def get_mpc_status():
    # `mpc status` ausführen und den Output abrufen
    output = subprocess.check_output(['mpc', 'status']).decode('utf-8')
    return output

# Funktion, um den Status des MPD-Dienstes abzurufen
def get_mpd_status():
    try:
        # Status des MPD-Dienstes abrufen
        output = subprocess.check_output(["systemctl", "status", "mpd"]).decode("utf-8")
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

# Funktion, um den HTML-Code zu generieren
def generate_html(mpc_output, mpd_output, last_updated):
    # HTML-Code mit dem Output von `mpc status` und dem MPD-Status einbetten
    html_content = f"""
    <h1>ORPHEUS - a simple streaming client  by Spiel0r</h1>

    <h2>MPC Status</h2>
    <pre>{mpc_output}</pre>

    <h2>MPD Status</h2>
    <pre>{mpd_output}</pre>

    <h3>Last Updated: {last_updated}</h3>
    """
    return html_content

# Output von `mpc status` und MPD-Status abrufen
mpc_output = get_mpc_status()
mpd_output = get_mpd_status()

# Aktuelles Datum und Uhrzeit als letzte Aktualisierung
last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# HTML generieren
html_content = generate_html(mpc_output, mpd_output, last_updated)

# HTML in die index.html schreiben
with open('/var/www/orpheus/index.html', 'w') as html_file:
    html_file.write(html_content)

print("MPC-Status und MPD-Status wurden in die index.html geschrieben.")

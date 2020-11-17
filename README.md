# Fermitech-Website
Fermitech Softworks website written in Python, Jinja2, Javascript and HTML.

## Installation

1. Clone this repository using `git`:
   ```
   git clone https://github.com/Fermitech-Softworks/Fermitech-Website.git
   ```
   
2. Create a new `venv`:
   ``` 
   python -m venv venv
   ```
   
3. `activate` the venv you just created:
   ```bash
   source venv/bin/activate
   ```
  
4. Install the requirements using `pip`:
   ```
   pip install -r requirements.txt
   ```
   
### For development

5. Use `export` to set the required environment variables:
   ```bash
   export COOKIE_SECRET_KEY='qwerty'  # A random string of characters
   ```
   
6. Run the `flask` development server:
   ```
   python server.py
   ```
   
### For production


5. Create the file `/etc/systemd/system/web-erre2.service` with the following contents:
   ```ini
   [Unit]
   Name=web-fermitech-site
   Description=Fermitech Gunicorn Server
   Wants=network-online.target
   After=network-online.target nss-lookup.target
   
   [Service]
   Type=exec
   User=fermitech-site
   WorkingDirectory=/opt/fermitech-site  # Replace with the directory where you cloned the repository
   ExecStart=/opt/fermitech-site/venv/bin/gunicorn -b 127.0.0.1:30002 server:app  # Replace with the directory where you cloned the repository
   
   [Install]
   WantedBy=multi-user.target
   ```
   
6. Create the file `/etc/systemd/system/web-erre2.service.d/override.conf` with the following contents:
   ```ini
   [Service]
   Environment="COOKIE_SECRET_KEY=qwerty"  # A random string of characters
   ```
   
7. Reload all `systemd` daemon files:
   ```
   systemctl daemon-reload
   ```
   
8. `start` (and optionally `enable` to run at boot) the `web-erre2` systemd service:
   ```
   systemctl start web-fermitech-site
   systemctl enable web-fermitech-site
   ```
   
9. Configure a reverse proxy.

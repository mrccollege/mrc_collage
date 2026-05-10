import json
import requests
import os
import re


WHATSAPP_TOKEN = "Pgow2uDQrh9cLLpAZyeqT1iBBRKVU5ERVJTQ09SRQxeHn04rDCJg8PoJiHMbXrpM1tgrTiyD3W0YVU5ERVJTQ09SRQNuC0tfcJaK4QIpPLYV2QU9zIyd4v6hS0MxQtMfKKMSCvGNJ4Q8kMeqZ61Uw"
WHATSAPP_PHONE_ID = "1028028933720765"


def send_whatsapp_registration_msg(phone, name):
    # Meta API usually requires: 919876543210 (No '+' sign)
    clean_phone = ''.join(filter(str.isdigit, phone))
    if len(clean_phone) == 10:
        clean_phone = f"91{clean_phone}"
        
    url = f"https://crmapi1.whatapi.in/api/meta/v19.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    
    data = {
        "to": clean_phone,
        "recipient_type": "individual",
        "type": "template",
        "template": {
            "language": {
                "policy": "deterministic",
                "code": "en"
            },
            "name": "reminder",
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": "Welcome to MRC Therapy App"
                        },
                        {
                            "type": "text",
                            "text": "You have been succesfully registered with us"
                        },
                        {
                            "type": "text",
                            "text": "Dr. Abhishek Sharma's Team, MRC Research center , Vrindavan"
                        }
                    ]
                }
            ]
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data) # Use json=data directly
        print(f"WhatsApp API Status: {response.status_code}")
        print(f"WhatsApp API Response: {response.text}")
        return response.json()
    except Exception as e:
        print(f"WhatsApp Exception: {e}")
        return None


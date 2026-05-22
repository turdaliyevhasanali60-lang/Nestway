import os
import urllib.request
import urllib.parse
import json
import logging

logger = logging.getLogger(__name__)

def send_telegram_lead(lead):
    """
    Sends a lead notification to the designated Telegram chat using standard urllib.
    Fails gracefully so that missing environment variables or network issues
    never crash the user-facing website.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        logger.warning("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not configured. Skipping Telegram notification.")
        return False

    # Format the lead type label if it exists
    lead_type_label = lead.get_lead_type_display() if hasattr(lead, 'get_lead_type_display') else str(lead.lead_type)
    
    # Let's construct the main message body exactly as requested
    msg_lines = [
        "New Contact Form Submission",
        f"Name: {lead.name}",
        f"Email: {lead.email}",
        f"Phone: {lead.phone or 'N/A'}"
    ]
    
    # If this is a career or academy application, let's add those details to the Telegram notification elegantly
    if lead.lead_type != 'general':
        msg_lines.append(f"Category: {lead_type_label}")
    if lead.country:
        msg_lines.append(f"Country: {lead.country}")
    if lead.experience_level:
        msg_lines.append(f"Experience: {lead.experience_level}")
        
    msg_lines.append("Message:")
    msg_lines.append(lead.message or '')

    message_text = "\n".join(msg_lines)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML" if False else None  # plain text matching format exactly
    }

    try:
        data = urllib.parse.urlencode(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('ok'):
                logger.info("Telegram notification sent successfully.")
                return True
            else:
                logger.error(f"Telegram API error: {res_data}")
                return False
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}", exc_info=True)
        return False

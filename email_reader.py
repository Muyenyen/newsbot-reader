
import imaplib
import email
from email.header import decode_header
import re

def fetch_filtered_emails(username, app_password, allowed_senders=None, extract_links=True, extract_text=True, num_emails=15):
    results = []

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, app_password)
    mail.select("inbox")

    result, data = mail.search("UTF-8", "ALL")
    email_ids = data[0].split()[-num_emails:]

    for eid in reversed(email_ids):
        result, message_data = mail.fetch(eid, "(RFC822)")
        for response_part in message_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg["From"]
                if allowed_senders and not any(s.lower() in sender.lower() for s in allowed_senders):
                    continue  # skip non-matching senders

                payload = {"from": sender, "links": [], "text": ""}
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        if ctype == "text/plain" and "attachment" not in part.get("Content-Disposition", ""):
                            body += part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                if extract_links:
                    payload["links"] = re.findall(r'https?://\S+', body)
                if extract_text:
                    payload["text"] = body.strip()
                results.append(payload)

    mail.logout()
    return results

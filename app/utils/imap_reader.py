import imaplib
import email
from email.header import decode_header
from config import Config

def read_unread_emails_for_account(imap_server, email_address, password,sender, limit=10):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        mail.select("inbox")

        # Buscar solo correos no leídos y del remitente específico
        result, data = mail.search(None, f'(UNSEEN FROM "{sender}")')
        mail_ids = data[0].split()[-limit:]

        emails = []
        for num in mail_ids:
            result, msg_data = mail.fetch(num, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            from_ = msg.get("From")

            # Obtener cuerpo de texto si es posible
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            emails.append({
                "subject": subject,
                "from": from_,
                "body": body
            })

        mail.logout()
        return emails

    except Exception as e:
        return [{"error": str(e)}]
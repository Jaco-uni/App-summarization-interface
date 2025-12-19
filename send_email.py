from ast import operator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def format_summary_email(diz_summ):
    html = "<h2>Paper Summaries</h2><ul>"  # intestazione generale
    #print(diz_summ)
    for url in diz_summ:
        title, author, subj, date, _, summ = diz_summ[url]  # ignoro il secondo 'url' con _
        #print(author)
        if len(author) == 1:
            html += f"<li><strong>{title}</strong> — Written by {author[0]}, in <em>{subj}</em>, published on {date}.<br>"
        else:
            html += f"<li><strong>{title}</strong> — Written by {author[0]}, {author[1]}, in <em>{subj}</em>, published on {date}.<br>"
        summ = summ.replace("Link to paper", "").replace(":","").strip()
        html += f"Summary: {summ}<br>"
        
        html += f"<a href='{url}'>Link to paper:</a></li><br><br>"

    html += "</ul>"
    #print(html)
    return html

def email_confermation(name, surname, to_email, subject, keywords, classification):
    html = f"""
    <h2>Subscription Confirmation</h2>
    <p>Dear {name} {surname},</p>
    <p>Thank you for subscribing to our paper summary service. Here are the details of your subscription:</p>
    <ul>
        <li><strong>Email:</strong> {to_email}</li>
        <li><strong>Subject:</strong> {subject if subject else 'All Subjects'}</li>
        <li><strong>Keywords:</strong> {', '.join(keywords) if keywords else 'None'}</li>
        <li><strong>Classification:</strong> {classification}</li>
    </ul>
    <p>You will start receiving summaries based on your preferences soon.</p>
    <p>Best regards,<br>Your Paper Summary Team</p>
    """
    return html

def send_email(to_email, subject, html_content, smtp_server, smtp_port, sender_email, sender_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())




# -*- coding: utf-8 -*-
"""
Gmail Audio Drama Completion Notifier
Sends instant notification to user's Gmail when 30k-40k words audio drama completes rendering.
"""

import os
import sys
import ssl
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

GMAIL_USER = os.environ.get("GMAIL_USER", "9329238475x@gmail.com")
GMAIL_APP_PASS = os.environ.get("GMAIL_APP_PASS", "ziqkkzjwffqnzrgn")
NOTIFICATION_RECIPIENT = os.environ.get("NOTIFICATION_RECIPIENT", "9329238475x@gmail.com")

def send_drama_complete_email(
    story_title: str,
    duration_str: str,
    word_count: int,
    master_file_path: str,
    character_breakdown: Optional[Dict[str, int]] = None,
    engine_name: str = "Chatterbox V3 Neural TTS",
    director_name: str = "Google Gemini AI Drama Director",
    recipient: Optional[str] = None
) -> bool:
    """
    Sends a rich, styled HTML email notification to the user upon audio drama completion.
    """
    to_email = recipient or NOTIFICATION_RECIPIENT
    sender_email = GMAIL_USER
    app_password = GMAIL_APP_PASS

    if not sender_email or not app_password:
        print("[EmailNotifier] Missing GMAIL_USER or GMAIL_APP_PASS in environment!")
        return False

    subject = f"[Audio Drama Ready] '{story_title}' - {duration_str} Complete!"

    # Format characters
    char_html = ""
    if character_breakdown:
        char_html = "<ul>"
        for char, count in character_breakdown.items():
            char_html += f"<li><b>{char}:</b> {count} scenes</li>"
        char_html += "</ul>"
    else:
        char_html = "<p>Multi-Speaker Hero, Heroine & Narrator Cast</p>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
            .card {{ max-width: 650px; margin: auto; background: #1e293b; border-radius: 12px; padding: 28px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            h2 {{ color: #38bdf8; margin-top: 0; border-bottom: 2px solid #334155; padding-bottom: 12px; }}
            .badge {{ display: inline-block; background: #10b981; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px; text-transform: uppercase; }}
            .details-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 20px; }}
            .details-table td {{ padding: 10px 12px; border-bottom: 1px solid #334155; }}
            .details-table td.label {{ color: #94a3b8; font-weight: 600; width: 35%; }}
            .details-table td.value {{ color: #f8fafc; font-weight: bold; }}
            .characters-box {{ background: #0f172a; padding: 14px; border-radius: 8px; border: 1px solid #334155; margin-top: 15px; }}
            .footer {{ font-size: 12px; color: #64748b; margin-top: 24px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">Master Render Complete</span>
            <h2>Audio Drama Master is Ready!</h2>
            <p>भाई, आपका 30k-40k शब्द का नया ऑडियो ड्रामा सफलतापूर्वक तैयार हो गया है!</p>

            <table class="details-table">
                <tr>
                    <td class="label">Story Title</td>
                    <td class="value">{story_title}</td>
                </tr>
                <tr>
                    <td class="label">Audio Duration</td>
                    <td class="value" style="color: #38bdf8;">{duration_str}</td>
                </tr>
                <tr>
                    <td class="label">Word Count</td>
                    <td class="value">{word_count:,} Words</td>
                </tr>
                <tr>
                    <td class="label">Voice Engine</td>
                    <td class="value">{engine_name}</td>
                </tr>
                <tr>
                    <td class="label">Drama Director</td>
                    <td class="value">{director_name}</td>
                </tr>
                <tr>
                    <td class="label">Master Audio File</td>
                    <td class="value" style="word-break: break-all; font-family: monospace; font-size: 12px;">{master_file_path}</td>
                </tr>
                <tr>
                    <td class="label">Timestamp</td>
                    <td class="value">{datetime.now().strftime("%d %b %Y, %I:%M:%S %p")}</td>
                </tr>
            </table>

            <div class="characters-box">
                <h4 style="margin: 0 0 10px 0; color: #cbd5e1;">Character Dialogue Breakdown:</h4>
                {char_html}
            </div>

            <div class="footer">
                Audio-Automation Production Engine • Kaggle GPU & Gemini AI Edition
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Audio-Automation Studio <{sender_email}>"
    msg["To"] = to_email

    # Plaintext fallback
    plain_text = f"""
    Audio Drama Ready: {story_title}
    Duration: {duration_str}
    Words: {word_count}
    Engine: {engine_name}
    Director: {director_name}
    Master File: {master_file_path}
    """
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    print(f"\n[EmailNotifier] Sending completion alert to: {to_email}...")
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"  [EmailNotifier] Email notification delivered successfully to {to_email}!")
        return True
    except Exception as e:
        print(f"  [EmailNotifier] Error delivering email: {e}")
        return False

if __name__ == "__main__":
    send_drama_complete_email(
        story_title="निर्मला (भाग 1) - मुंशी प्रेमचंद",
        duration_str="3.8 Hours (~230 mins)",
        word_count=34113,
        master_file_path="/kaggle/working/output/masters/nirmala_part1_master.mp3",
        character_breakdown={"HERO": 80, "HEROINE": 32, "NARRATOR": 1569}
    )

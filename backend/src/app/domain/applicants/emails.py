from __future__ import annotations

import smtplib
from email.message import EmailMessage

from app.server import get_settings
from app.models.applicant import Applicant


def send_email(msg: EmailMessage) -> None:
    settings = get_settings()
    email_cfg = settings.email

    msg["From"] = email_cfg.sender_email
    msg["Sender"] = email_cfg.sender_email

    """ if settings.api.debug:
        return """

    try:
        with smtplib.SMTP(email_cfg.smtp_server, email_cfg.smtp_port) as server:
            server.starttls()
            server.login(email_cfg.smtp_username, email_cfg.smtp_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_welcome_email(applicant: Applicant) -> None:
    settings = get_settings()

    msg = EmailMessage()
    msg["To"] = applicant.email
    msg["Subject"] = "Köszöntünk a KözCampus közösségében!"
    msg.set_content(
        f"Kedves {applicant.first_name} {applicant.last_name}!\n"
        "\n"
        "Örülünk, hogy téged is vonz a kihívás: a KözCampusnál hiszünk abban, "
        "hogy együtt erősebbek vagyunk, mint külön-külön. Jelentkezéseddel megtetted "
        "az első lépést, hogy egy olyan csapat tagja legyél, amely a szakma és a "
        "politika teljes spektrumán átívelő párbeszédet épít.\n"
        "\n"
        "Mi történik most? HR-csapatunk hamarosan felveszi veled a kapcsolatot. "
        "Addig is maradj kíváncsi, hamarosan jelentkezünk a részletekkel!\n"
        "\n"
        "Kövess minket Instagramon!\n"
        "https://www.instagram.com/kozcampus/\n"
        "\n"
        "Üdvözlettel,\n"
        "A KözCampus Csapata\n"
        "\"A fiatal értelmiség közös nevezője\""
    )

    send_email(msg)

    print(f"Sent welcome email to {applicant.email}")


def send_organizer_notification(applicant: Applicant) -> None:
    settings = get_settings()
    email_cfg = settings.email

    name = f"{applicant.first_name} {applicant.last_name}"
    admin_url = settings.api.redirect_url

    msg = EmailMessage()
    msg["To"] = email_cfg.organizer_email
    msg["Subject"] = f"\U0001f6a8 Új jelentkező a láthatáron! - {name} jelentkezett"
    msg.set_content(
        "Szia!\n"
        "\n"
        "Újabb motivált fiatal szeretne csatlakozni a csapathoz!\n"
        f"\n"
        f"Név: {name}\n"
        f"E-mail: {applicant.email}\n"
        f"\n"
        f"Nézd meg az adatlapját az admin felületen: {admin_url}\n"
        "és indítsd el az onboarding folyamatot!"
    )

    send_email(msg)

    print(f"Sent organizer notification for {applicant.email}")

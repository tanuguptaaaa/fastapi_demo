from fastapi_mail import MessageSchema, FastMail, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="guptatanu842002@gmail.com",
    MAIL_PASSWORD="wsoj jraw dnqx xioo",  # Your app-specific password
    MAIL_FROM="guptatanu842002@gmail.com",
    MAIL_PORT=587,  # Port for StartTLS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Correct field for StartTLS (port 587)
    MAIL_SSL_TLS=False,  # SSL/TLS should be False if using StartTLS
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(email: str, content: str):
    try:
        message = MessageSchema(
            subject="OTP for Password Reset",
            recipients=[email],
            body=content,
            subtype="html"
        )
        fm = FastMail(conf)  # Pass the ConnectionConfig object here
        await fm.send_message(message)
    except Exception as e:
        print("error in send_email",e)


# 📧 smtp-python-mail_sender

`smtp-python-mail_sender` is a simple graphical email-sending utility built with **Python** and **Pygame**. It supports sending emails via **Mailgun**, **Mailjet**, and **SendGrid** using their respective API endpoints.

---

## 🎯 Features

- Send emails through:
  - ✅ Mailgun
  - ✅ Mailjet
  - ✅ SendGrid
- Simple **GUI interface using Pygame**
- Interactive form inputs for:
  - Sender and recipient
  - Subject and message
  - API credentials per service
- Real-time feedback on send status

---

## 🖼️ Interface

The app uses **Pygame** to create a basic GUI with multiple input fields:

| Field       | Description |
|-------------|-------------|
| Service     | Mail service to use: `Mailgun`, `Mailjet`, or `SendGrid` |
| From        | Sender's email address |
| To          | Recipient email address |
| Subject     | Email subject |
| Body        | Email message body |
| API Key     | Your service's API key |
| Domain      | *(For Mailgun only)*: your domain |
| Username    | *(For Mailjet only)*: your username |
| Password    | *(For Mailjet only)*: your password |

Press **Enter/Return** to send the email.

Success and failure messages are displayed at the bottom of the window.

---

## 🛠️ Requirements

- Python 3.7+
- [pygame](https://pypi.org/project/pygame/)
- [requests](https://pypi.org/project/requests/)

### Install dependencies:

```bash
pip install pygame requests

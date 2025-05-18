import pygame
import requests

pygame.init()
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Email Sender")

FONT = pygame.font.Font(None, 28)

# Text input class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get(self):
        return self.text

def send_mail(service, creds, to_email, subject, body):
    if service == "Mailgun":
        return requests.post(
            f"https://api.mailgun.net/v3/{creds['domain']}/messages",
            auth=("api", creds["api_key"]),
            data={
                "from": creds["from"],
                "to": [to_email],
                "subject": subject,
                "text": body
            }
        )

    elif service == "Mailjet":
        return requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(creds["username"], creds["password"]),
            json={
                "Messages": [{
                    "From": {
                        "Email": creds["from"],
                        "Name": "Mailjet User"
                    },
                    "To": [{
                        "Email": to_email,
                        "Name": "Recipient"
                    }],
                    "Subject": subject,
                    "TextPart": body
                }]
            }
        )

    elif service == "SendGrid":
        return requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {creds['api_key']}",
                "Content-Type": "application/json"
            },
            json={
                "personalizations": [{
                    "to": [{"email": to_email}]
                }],
                "from": {"email": creds["from"]},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}]
            }
        )

# Input fields
input_boxes = {
    "service": InputBox(100, 30, 140, 30),
    "from": InputBox(100, 80, 400, 30),
    "to": InputBox(100, 130, 400, 30),
    "subject": InputBox(100, 180, 400, 30),
    "body": InputBox(100, 230, 400, 30),
    "api_key": InputBox(100, 280, 400, 30),
    "domain": InputBox(100, 330, 400, 30),
    "username": InputBox(100, 380, 400, 30),
    "password": InputBox(100, 430, 400, 30),
}

clock = pygame.time.Clock()
message = ""

while True:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        for box in input_boxes.values():
            box.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            service = input_boxes["service"].get().strip()
            from_email = input_boxes["from"].get()
            to_email = input_boxes["to"].get()
            subject = input_boxes["subject"].get()
            body = input_boxes["body"].get()

            creds = {
                "api_key": input_boxes["api_key"].get(),
                "domain": input_boxes["domain"].get(),
                "username": input_boxes["username"].get(),
                "password": input_boxes["password"].get(),
                "from": from_email
            }

            try:
                res = send_mail(service, creds, to_email, subject, body)
                if res.status_code in [200, 202]:
                    message = "✅ Email sent successfully!"
                else:
                    message = f"❌ Failed: {res.status_code} - {res.text}"
            except Exception as e:
                message = f"❌ Error: {e}"

    # Draw inputs
    y_labels = ["Service (Mailgun/Mailjet/SendGrid)", "From", "To", "Subject", "Body",
                "API Key", "Domain", "Username", "Password"]
    for i, (label, box) in enumerate(input_boxes.items()):
        lbl = FONT.render(y_labels[i], True, pygame.Color('white'))
        screen.blit(lbl, (box.rect.x, box.rect.y - 20))
        box.draw(screen)

    if message:
        msg_surface = FONT.render(message, True, pygame.Color('green' if "✅" in message else 'red'))
        screen.blit(msg_surface, (20, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(30)

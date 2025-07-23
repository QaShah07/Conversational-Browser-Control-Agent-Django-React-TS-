from .controller import BrowserController

def send_gmail(conv_id, shots_dir, creds, email_data, push_cb):
    """
    creds = {email,password}
    email_data = {recipient, subject, body}
    push_cb(type, payload) -> WS
    """
    bc = BrowserController(conv_id, shots_dir)
    bc.launch(headless=False)

    try:
        push_cb('status.update', {'msg':'Opening Gmail...'})
        img = bc.goto('https://mail.google.com/')
        push_cb('message.new', {'role':'screenshot','image_path':img})

        bc.wait_for('input[type="email"]')
        push_cb('status.update', {'msg':'Typing email...'})
        img = bc.fill('input[type="email"]', creds['email'])
        push_cb('message.new', {'role':'screenshot','image_path':img})
        img = bc.click('button:has-text("Next")')
        push_cb('message.new', {'role':'screenshot','image_path':img})

        bc.wait_for('input[type="password"]')
        push_cb('status.update', {'msg':'Typing password...'})
        img = bc.fill('input[type="password"]', creds['password'])
        push_cb('message.new', {'role':'screenshot','image_path':img})
        img = bc.click('button:has-text("Next")')
        push_cb('message.new', {'role':'screenshot','image_path':img})

        bc.wait_for('div[role="main"]')
        push_cb('status.update', {'msg':'Inbox loaded. Composing...'})
        img = bc.click('div[gh="cm"]')
        push_cb('message.new', {'role':'screenshot','image_path':img})

        bc.wait_for('textarea[name="to"]')
        img = bc.fill('textarea[name="to"]', email_data['recipient'])
        push_cb('message.new', {'role':'screenshot','image_path':img})
        img = bc.fill('input[name="subjectbox"]', email_data['subject'])
        push_cb('message.new', {'role':'screenshot','image_path':img})
        # Body sometimes needs type()
        bc.page.click('div[aria-label="Message Body"]')
        bc.page.type('div[aria-label="Message Body"]', email_data['body'])
        img = bc.snap('body')
        push_cb('message.new', {'role':'screenshot','image_path':img})

        img = bc.click('div[aria-label*="Send"]')
        push_cb('message.new', {'role':'screenshot','image_path':img})

        bc.wait_for('span:has-text("Message sent")')
        img = bc.snap('sent')
        push_cb('message.new', {'role':'screenshot','image_path':img})
        push_cb('message.new', {'role':'agent','content':'✓ Email sent successfully!'})
    finally:
        bc.close()
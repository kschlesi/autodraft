import gmailer
from email.message import EmailMessage

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

# ## create default draft
# message = EmailMessage()
# message.set_content('Auto Message Test 2')
# message['To'] = 'kschlesi42@gmail.com'
# message['From'] = 'kschlesi42@gmail.com'
# message['Subject'] = 'Automated draft test 2'
# draft = cr.create_draft(message)

# ## get test draft raw
# draft_id = 'r3770215706863068957'
# draft_id = 'r2408711609765372954'
# draft = cr.get_draft(draft_id, format='string')

## get most recent sliding scale draft
q = "from:kschlesi42@gmail.com sliding scale"
draft_list = cr.list_drafts(q=q, maxResults=10)
drafts = [cr.get_draft(d['id'], format='string') for d in draft_list['drafts']]
if len(drafts)==1:
    draft = drafts[0]
    template_id = draft['id']
    # print(draft['message']['string'])

# replace draft strings with variable info
replace_tuples = [('XXX','Kim'), ('XXX', '6'), ('XXX', '5.1')]
draft = cr.create_draft_from_template(template_id=template_id, replace_tuples=replace_tuples)

print(draft)

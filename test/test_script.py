import gmailer

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

## create default draft
draft = cr.create_draft()

# get test draft raw
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

new_draft = cr.create_draft_from_template()
# print(draft)

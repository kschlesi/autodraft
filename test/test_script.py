import gmailer

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

# ## create default draft
# draft = cr.create_draft()

## get test draft raw
## draft_id = 'r3770215706863068957'
# draft_id = 'r2408711609765372954'
# draft = cr.get_raw_draft(draft_id)

## get most recent sliding scale draft
q = "from:kschlesi42@gmail.com sliding scale"
draft_list = cr.list_drafts(q=q, maxResults=10)
drafts = [cr.get_raw_draft(d['id']) for d in draft_list['drafts']]
draft = drafts[0]

print(draft['message']['snippet'])
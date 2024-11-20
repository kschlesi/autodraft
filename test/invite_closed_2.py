import gmailer
import pandas as pd

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

## get most recent sliding scale draft
q = "You’re Invited - BFG Invite Tryout 5/18 _NAME_"
draft_list = cr.list_drafts(q=q, maxResults=10)
drafts = [cr.get_draft(d['id'], format='full') for d in draft_list['drafts']]

print([draft['id']+draft['message']['snippet'] for draft in drafts])
if len(drafts)>0:
    draft = drafts[0]
    template_id = draft['id']
    print(template_id)
else:
    template_id = 'r5781599331753565967'

# replace draft strings with variable info
data = pd.read_csv('/Users/kimberly.schlesinger/Documents/codethings/autodraft/test/invite_closed_2.csv')
for row in data.iterrows():
    print(row[1]['FULLNAME'])
    if row[1]['SEND'] == 'Yes':
        replace_tuples = [
            ('_NAME_',row[1]['NAME'])
        ]
        print(template_id)
        print(replace_tuples)
        print(row[1]['EMAIL'])
        draft = cr.create_draft_from_template(
            template_id=template_id
            , replace_tuples=replace_tuples
            , send_from='bfgtc2024@gmail.com'
            , send_to=row[1]['EMAIL']
        )
import gmailer
import pandas as pd

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

## get most recent sliding scale draft
q = "from:kschlesi42@gmail.com Round 1 Dues"
draft_list = cr.list_drafts(q=q, maxResults=10)
drafts = [cr.get_draft(d['id'], format='full') for d in draft_list['drafts']]

if len(drafts)==1:
    draft = drafts[0]
    template_id = draft['id']
    print(template_id)
else:
    template_id = 'r2408711609765372954'

# replace draft strings with variable info
data = pd.read_csv('/Users/kimberly.schlesinger/Documents/codethings/autodraft/test/raw_dues_round1.csv')
i = 0
for row in data.iterrows():
    if i==0 or i==1:
        print(row[1]['Fullname'])
        replace_tuples = [
            ('XNAMEX',row[1]['Name'])
            , ('XNOUNX', str(row[1]['Noun']))
            , ('XAMTX', str(row[1]['Amount']))
            , ('XEXPX', str(row[1]['Explanation']))
        ]
        draft = cr.create_draft_from_template(
            template_id=template_id
            , replace_tuples=replace_tuples
            , send_from='kschlesi42@gmail.com'
            , send_to=row[1]['Email']
            , send_cc='crystal.koo@gmail.com,cherylhsu168@gmail.com'
        )
        i = i+1
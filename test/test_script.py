import gmailer

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

#draft = cr.create_draft()
draft_id = 'r3770215706863068957'
draft = cr.get_raw_draft(draft_id)

# all_events = cr.get_scheduled_events()

# bl_events = cr.get_scheduled_events(device_name='Bedroom Light')

print(draft)
#print(bl_events)

import gmailer

cr = gmailer.GMailer(credentials_path='/var/autodraft/secrets')

draft = cr.create_draft()

# all_events = cr.get_scheduled_events()

# bl_events = cr.get_scheduled_events(device_name='Bedroom Light')

print(draft)
#print(bl_events)

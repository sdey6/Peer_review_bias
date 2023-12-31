def process(client, note, invitation):
    GROUP_PREFIX = ''
    SUPPORT_GROUP = GROUP_PREFIX + '/Support'

    forum_note = client.get_note(note.forum)
    subject = f'''{note.content['title']} for service: {forum_note.content['title']}'''
    message = f'''An error occurred while running the stage {note.content['stage_name']} your service request. 
\n\nError: {note.content['error']} 
\n\nTo view the comment, click here: https://openreview.net/forum?id={note.forum}&noteId={note.id}
'''

    client.post_message(subject=subject, message=message, recipients=note.readers, ignoreRecipients=[note.tauthor, SUPPORT_GROUP])

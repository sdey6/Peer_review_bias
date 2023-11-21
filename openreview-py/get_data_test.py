import openreview

guest_client = openreview.Client(baseurl='https://api.openreview.net')
venues = openreview.tools.get_invitation(guest_client)
print(venues)
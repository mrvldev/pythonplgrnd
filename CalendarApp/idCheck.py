from caldav import DAVClient

client = DAVClient(
    url="https://caldav.icloud.com",
    username="mike.raw@gmx.at",
    password="tavz-ctkj-nvqy-jiqg"
)

principal = client.principal()

# Alle verfügbaren Kalender holen
calendars = principal.calendars()

print("Gefundene iCloud-Kalender:")
for i, cal in enumerate(calendars):
    print(i, cal.name)

# WICHTIG: den richtigen Kalender manuell auswählen
calendar = calendars[0]  # 0 = erster Kalender

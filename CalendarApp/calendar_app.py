import tkinter as tk
from tkinter import simpledialog, messagebox
from caldav import DAVClient
import vobject
import datetime

# === iCloud Zugang ===
ICLOUD_EMAIL = "mike.raw@gmx.at"
ICLOUD_APP_PASSWORD = "tavz-ctkj-nvqy-jiqg"

client = DAVClient(
    url="https://caldav.icloud.com/",
    username=ICLOUD_EMAIL,
    password=ICLOUD_APP_PASSWORD
)
principal = client.principal()
calendar = principal.calendars()[2]  # erster Kalender, ggf. anpassen

# === GUI ===
class CalendarApp:
    def __init__(self, master):
        self.master = master
        master.title("iOS Kalender Organizer – Heute")

        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        # Buttons
        self.add_button = tk.Button(self.frame, text="Termin hinzufügen", command=self.add_event)
        self.add_button.pack(fill='x')

        self.delete_button = tk.Button(self.frame, text="Termin löschen", command=self.delete_event)
        self.delete_button.pack(fill='x', pady=(0,5))

        self.refresh_button = tk.Button(self.frame, text="Refresh", command=self.refresh)
        self.refresh_button.pack(fill='x', pady=(0,10))

        # Termin-Liste
        self.listbox = tk.Listbox(self.frame, width=60, height=15)
        self.listbox.pack()

        self.event_map = {}  # Map für ausgewählte Events

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.event_map.clear()
        today = datetime.date.today()
        events = calendar.events()
        counter = 0
        for event in events:
            try:
                summary = event.vobject_instance.vevent.summary.value
                start = event.vobject_instance.vevent.dtstart.value
                uid = event.vobject_instance.vevent.uid.value

                if isinstance(start, datetime.datetime):
                    date_only = start.date()
                    start_str = start.strftime("%H:%M")
                else:
                    continue  # skip non-datetime events

                if date_only == today:
                    # Priorität anhand Keyword im Titel/Notiz (optional)
                    priority = "normal"
                    description = getattr(event.vobject_instance.vevent, 'description', None)
                    if description:
                        description_text = description.value.lower()
                        if "hoch" in description_text:
                            priority = "hoch"
                        elif "niedrig" in description_text:
                            priority = "niedrig"

                    display_text = f"{start_str} - {summary}"
                    self.listbox.insert(tk.END, display_text)

                    # Farbcodierung
                    if priority == "hoch":
                        self.listbox.itemconfig(counter, fg="red")
                    elif priority == "niedrig":
                        self.listbox.itemconfig(counter, fg="blue")
                    else:
                        self.listbox.itemconfig(counter, fg="orange")

                    self.event_map[counter] = uid
                    counter += 1

            except Exception as e:
                print("Fehler beim Laden eines Termins:", e)

    def add_event(self):
        title = simpledialog.askstring("Titel", "Titel des Termins:")
        date_str = simpledialog.askstring("Datum", "Datum (YYYY-MM-DD):")
        time_str = simpledialog.askstring("Uhrzeit", "Uhrzeit (HH:MM):")
        priority = simpledialog.askstring("Priorität", "Priorität (hoch/mittel/niedrig):")
        note = simpledialog.askstring("Notiz", "Notiz (optional):")

        if not title or not date_str or not time_str:
            messagebox.showerror("Fehler", "Titel, Datum und Uhrzeit sind erforderlich!")
            return

        start = f"{date_str}T{time_str.replace(':','')}00Z"
        end_time = (datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M") +
                    datetime.timedelta(hours=1)).strftime("%Y%m%dT%H%M%SZ")

        # Priorität in Beschreibung speichern
        description_text = f"{note if note else ''} | {priority}"

        ics_template = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:{datetime.datetime.utcnow().timestamp()}@example.com
DTSTAMP:{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{start}
DTEND:{end_time}
SUMMARY:{title}
DESCRIPTION:{description_text}
END:VEVENT
END:VCALENDAR
"""
        calendar.add_event(ics_template)
        messagebox.showinfo("Erfolg", "Termin hinzugefügt!")
        self.refresh()

    def delete_event(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Fehler", "Bitte zuerst einen Termin auswählen!")
            return
        idx = selection[0]
        uid = self.event_map.get(idx)
        if uid:
            events = calendar.events()
            for event in events:
                if getattr(event.vobject_instance.vevent, 'uid', None) and \
                   event.vobject_instance.vevent.uid.value == uid:
                    event.delete()
                    break
            messagebox.showinfo("Erfolg", "Termin gelöscht!")
            self.refresh()

# === App starten ===
root = tk.Tk()
app = CalendarApp(root)
root.mainloop()

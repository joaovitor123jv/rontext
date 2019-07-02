#!env python3

from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC

cal = Calendar()

cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2019, 5, 31, 22, 58, 0, tzinfo=UTC))
event.add('dtend', datetime(2019, 5, 31, 23, 58, 0, tzinfo=UTC))
event.add('dtstamp', datetime(2019, 5, 31, 22, 50, 0, tzinfo=UTC))
event['uid'] = '20190511T101010/27346262376@mxm.dk'
event.add('priority', 5)
cal.add_component(event)

f = open('teste.ics', 'wb')
f.write(cal.to_ical())
f.close()

g = open('teste.ics', 'rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    if component.name == 'VEVENT':
        print(component.get('summary'))
        print(component.get('dtstart'))
        print(component.get('dtend'))
        print(component.get('dtstamp'))

g.close()

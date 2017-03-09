from bot_mcgill.models import McgillEvent
import json
class EventService:
    def listAllEventDates(self):
        academicEvents = McgillEvent.objects.filter(event_type='event_academic')
        eventsDict = {}
        i = 1
        for event in academicEvents:
            keys = ['event_name', 'event_date']
            values = [event.event_name, str(event.event_date)]
            eventDict = dict(zip(keys,values))
            eventsDict[i] = eventDict
            i = i+1

        #TODO:make the return more elegant and not just a dictionary.
        return json.dumps(eventsDict)
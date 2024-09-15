import json
from datetime import datetime

class DataManager:
    def __init__(self, filename='events.json'):
        self.filename = filename
        self.events = self.load_events()

    def load_events(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_events(self):
        with open(self.filename, 'w') as file:
            json.dump(self.events, file, indent=4)

    def add_event(self, date, title, content, tags):
        event_data = {
            'title': title,
            'content': content,
            'tags': tags
        }
        self.events[date] = event_data
        self.save_events()

    def get_events(self, date):
        return self.events.get(date, {})

    def update_event(self, date, title, content, tags):
        if date in self.events:
            self.events[date]['title'] = title
            self.events[date]['content'] = content
            self.events[date]['tags'] = tags
            self.save_events()

    def delete_event(self, date):
        if date in self.events:
            del self.events[date]
            self.save_events()

    def search_events(self, keyword):
        results = {}
        for date, event in self.events.items():
            if keyword.lower() in event['title'].lower() or keyword.lower() in event['content'].lower() or keyword.lower() in event['tags'].lower():
                results[date] = event
        return results

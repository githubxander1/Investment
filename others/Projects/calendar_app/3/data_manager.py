# data_manager.py

class DataManager:
    def __init__(self):
        self.events = []  # 初始化 events 列表

    def get_events_by_date(self):
        events_by_date = {}
        for event in self.events:
            date = event['date']
            events_by_date.setdefault(date, []).append(event)
        return events_by_date

    def get_events_by_tag(self):
        events_by_tag = {}
        for event in self.events:
            for tag in event['tags'].split(','):
                tag = tag.strip()
                events_by_tag.setdefault(tag, []).append(event)
        return events_by_tag

    def search_events(self, keyword):
        return [event for event in self.events if keyword.lower() in event['title'].lower() or keyword.lower() in event['content'].lower()]

    def save_event(self, date, title, description, tags):
        new_event = {
            'date': date,
            'title': title,
            'content': description,
            'tags': tags
        }
        self.events.append(new_event)

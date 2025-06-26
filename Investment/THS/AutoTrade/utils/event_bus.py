# utils/event_bus.py
import asyncio

class EventBus:
    def __init__(self):
        self._handlers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event_type, data=None):
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                asyncio.create_task(handler(data))

# 全局单例
event_bus = EventBus()

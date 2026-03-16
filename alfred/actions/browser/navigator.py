class BrowserNavigator:
    def goto_chatgpt(self, operator, topic=None, thread_hint=None):
        operator.open_chatgpt(topic=topic, thread_hint=thread_hint)

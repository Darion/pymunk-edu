class Log():
    TYPE_INFO = 0
    TYPE_WARNING = 1
    TYPE_ERROR = 2
    log = []
    def add(self, text, message_type=0):
        self.log.append([text, message_type])
    def tail(self, num):
        tail = self.log[-num:]
        return "\n".join([ line[0] for line in tail ])

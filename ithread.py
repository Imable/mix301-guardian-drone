import threading

class IThread(threading.Thread):
    '''
    Threading interface defining common functionality
    '''

    def __init__(self, consumers, queue, **kwargs):
        super().__init__(**kwargs)
        self.queue     = queue
        self.consumers = consumers

    def put_queue(self, obj):
        self.queue.put(obj)
    
    def notify_consumers(self, obj):
        for consumer in self.consumers:
            consumer.put_queue(obj)

    def run(self):
        while True:
            while not self.queue.empty():
                self.do()

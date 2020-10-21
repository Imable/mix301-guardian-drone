import threading

class IThread(threading.Thread):
    '''
    Threading interface defining common functionality
    '''

    def __init__(self, consumers, queue, **kwargs):
        super().__init__(**kwargs)
        self.queue     = queue
        self.consumers = consumers
        self.exit      = False

    def put_queue(self, obj):
        self.queue.put(obj)
    
    def notify_consumers(self, obj):
        for consumer in self.consumers:
            consumer.put_queue(obj)
    
    def graceful_exit(self):
        pass

    def run(self):
        while not self.exit:
            while not self.queue.empty():
                self.do()
                
        self.graceful_exit()

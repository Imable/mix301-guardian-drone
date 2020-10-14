# # Hacky way to allow for importing from parent folders
# from sys import path
# path.append('..')

from ithread import IThread

class Process(IThread):

    # Override the put_queue function, because this thread uses a PriorityQueue
    def put_queue(self, obj, priority=3):
        self.queue.put((priority, obj))
    
    def do(self):
        _, observation = self.queue.get()
        print(f'Observed {observation.kind} at {observation.rect}!')
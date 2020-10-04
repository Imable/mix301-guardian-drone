from observe.stream import Stream
from observe.observer import Observer

from process.process import Process

from queue import Queue
from queue import PriorityQueue

def get_threads():
    process = Process(
        [], PriorityQueue(5)
    )

    observer = Observer(
        'face', 
        'haarcascade_frontalface_default.xml', 
        [process], Queue(5)
    )

    stream = Stream(
        [observer], None
    )

    return [
        process, observer, stream
    ]
    
def start_threads():
    for thread in THREADS:
        thread.setDaemon(True)
        thread.start()

def end_threads():
    for thread in THREADS:
        thread.join()

THREADS = get_threads()
start_threads()
end_threads()

from observe.stream import Stream
from observe.observer import Observer

from queue import Queue

def get_threads():
    observer = Observer(
        'haarcascade_frontalface_default.xml', [], Queue(5)
    )

    stream = Stream(
        [observer], None
    )

    return [
        observer, stream
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

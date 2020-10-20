from observe.stream import Stream
from observe.observer import Observer
from observe.viewer import Viewer

from process.process import Process

from act.act import Act

from queue import Queue
from queue import PriorityQueue

def get_threads():
    act = Act(
        [], Queue(5)
    )

    process = Process(
        [act], PriorityQueue(5)
    )

    viewer = Viewer(
        [], Queue(1)
    )

    observer = Observer(
        'face', 
        'haarcascade_frontalface_default.xml', 
        [process], Queue(5)
    )

    stream = Stream(
        [observer, viewer], None
    )

    return [
        act, process, viewer, observer, stream
    ]
    
def start_threads():
    for thread in THREADS:
        thread.setDaemon(True)
        thread.start()

def end_threads():
    for thread in THREADS:
        thread.exit = True
        thread.join()

THREADS = get_threads()
start_threads()

# Wait for keypress to exit
input('')

end_threads()


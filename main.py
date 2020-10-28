from observe.stream import Stream
from observe.observer import Observer
from observe.umbrella_observer import UmbrellaObserver
from observe.viewer import Viewer

from process.process import Process

from act.act import Act

from queue import Queue
from queue import PriorityQueue
from queue import LifoQueue

def get_threads():
    act = Act(
        [], LifoQueue(0)
    )

    process = Process(
        [act], LifoQueue(0)
    )

    viewer = Viewer(
        [], LifoQueue(0)
    )

    # observer = Observer(
    #     'face', 
    #     'haarcascade_frontalface_default.xml', 
    #     [process], Queue(5)
    # )

    umbrella_observer = UmbrellaObserver(
        [process, viewer], LifoQueue(0)
    )

    stream = Stream(
        [umbrella_observer], None
    )

    return [
        act, process, viewer, umbrella_observer, stream
    ]
    
def start_threads():
    for thread in THREADS:
        thread.setDaemon(True)
        thread.start()

def end_threads():
    for thread in THREADS:
        thread.exit = True
    print('Set exit flag for all threads.')

    for thread in THREADS:
        thread.join()
    print('Joined all threads.') 

THREADS = get_threads()
start_threads()

# Wait for keypress to exit
input('')

end_threads()


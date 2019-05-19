from threading import Condition, Lock, Thread
import random
from time import sleep
from agar.model import Plankton
from agar.config import Config


class PlanktonGenerator:

    def __init__(self):
        print("Plankton generator")
        self._changesLock = Lock()
        self._newPlanktonUpdate = Condition()
        self._threadExitFlag = False
        self._generatingThread = None
        self._newPlanktonList = []

    def start(self):
        thread = Thread(name='plankton_generator', target=self.generate_plankton)
        thread.start()
        self._generatingThread = thread

    def stop(self):
        self._changesLock.acquire()
        self._threadExitFlag = True
        self._changesLock.release()
        if self._generatingThread is not None:
            self._generatingThread.join()
        self._newPlanktonUpdate.acquire()
        self._newPlanktonUpdate.notifyAll()
        self._newPlanktonUpdate.release()

    def generate_plankton(self):
        while True:
            #print("plankton generated")
            self._changesLock.acquire()
            if self._threadExitFlag:
                self._threadExitFlag.release()
                return None

            vertical_position = random.randint(0, Config.MAP_HEIGHT)
            horizontal_position = random.randint(0, Config.MAP_WIDTH)
            print("new plankton: (" + str(vertical_position) + "," + str(horizontal_position)+")")
            plankton = Plankton(horizontal_position, vertical_position)
            self._newPlanktonList.append(plankton)

            self._changesLock.release()
            self._newPlanktonUpdate.acquire()
            self._newPlanktonUpdate.notifyAll()
            self._newPlanktonUpdate.release()
            sleep(1)

    def get_new_plankton(self):
        print("\ngetPlanktonUpdate")
        self._newPlanktonUpdate.acquire()
        self._newPlanktonUpdate.wait()
        self._newPlanktonUpdate.release()

        self._changesLock.acquire()
        result = self._newPlanktonList
        self._newPlanktonList.clear()
        self._changesLock.release()
        return result



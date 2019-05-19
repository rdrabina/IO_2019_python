from threading import Condition, Lock, Thread
import random
from time import sleep
from agar.model import Powerup
from agar.config import Config
import copy


class PowerupGenerator:

    def __init__(self):
        print("Powerup generator")
        self._changesLock = Lock()
        self._newPowerupUpdate = Condition()
        self._threadExitFlag = False
        self._generatingThread = None
        self._newPowerupList = []

    def start(self):
        thread = Thread(name='powerup_generator', target=self.generate_powerup)
        thread.start()
        self._generatingThread = thread

    def stop(self):
        self._changesLock.acquire()
        self._threadExitFlag = True
        self._changesLock.release()
        if self._generatingThread is not None:
            self._generatingThread.join()
        self._newPowerupUpdate.acquire()
        self._newPowerupUpdate.notifyAll()
        self._newPowerupUpdate.release()

    def generate_powerup(self):
        while True:
            self._changesLock.acquire()
            if self._threadExitFlag:
                self._threadExitFlag.release()
                return None

            vertical_position = random.randint(0, Config.MAP_HEIGHT)
            horizontal_position = random.randint(0, Config.MAP_WIDTH)
            print("new powerup: (" + str(vertical_position) + "," + str(horizontal_position)+")")
            powerup = Powerup(horizontal_position, vertical_position)
            self._newPowerupList.append(powerup)

            self._changesLock.release()
            self._newPowerupUpdate.acquire()
            self._newPowerupUpdate.notifyAll()
            self._newPowerupUpdate.release()
            sleep(20)

    def get_new_powerup(self):
        print("\ngetPowerupUpdate")
        self._newPowerupUpdate.acquire()
        self._newPowerupUpdate.wait()
        self._newPowerupUpdate.release()

        self._changesLock.acquire()
        result = copy.deepcopy(self._newPowerupList)
        self._newPowerupList.clear()
        self._changesLock.release()
        return result

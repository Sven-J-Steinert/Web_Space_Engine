from datetime import datetime

from . import three


class Scene:

    def __init__(self):
        self.scene = three.Scene()
        self.camera = None
        self.objects = []
        self.selected_object = None
        self._realtime = True
        self._stopped = False
        self._time = None
        self._last_tick = None
        self._time_factor = 1
        self._time_offset = 0

    def get_time(self):
        if self._realtime:
            return datetime.utcnow()
        else:
            return self._time

    def set_time(self, time):
        self._realtime = False
        self._time = time

    def get_delta_time(self):
        if self._realtime:
            return datetime.utcnow() - self._last_tick
        else:
            delta_time = datetime.utcnow() - self._last_tick
            return self._time_factor * delta_time

    def get_time_str(self):
        return self.get_time().strftime('%Y-%m-%d %H:%M:%S')

    def realtime(self):
        self._realtime = True

    def play(self, forward=True):
        if forward:
            self._time_factor = abs(self._time_factor)
        else:
            self._time_factor = -abs(self._time_factor)

        if self._realtime:
            self._time = datetime.utcnow()
            self._realtime = False
        self._stopped = False

    def stop(self):
        if self._realtime:
            self._time = datetime.utcnow()
            self._realtime = False
        self._stopped = True

    def faster(self):
        if self._realtime:
            self.play()
        if self._time_factor < 10000:
            self._time_factor = self._time_factor * 10

    def slower(self):
        if self._realtime:
            self.play()
        if self._time_factor > 1:
            self._time_factor = self._time_factor // 10

    def tick(self):  # called to update scenario time
        if not self._realtime and not self._stopped:
            delta_time = datetime.utcnow() - self._last_tick
            self._time += self._time_factor * delta_time
        self._last_tick = datetime.utcnow()

import sys
from collections import namedtuple
from datetime import datetime as DateTime, timedelta as TimeDelta
from time import sleep

HMS = namedtuple('HMS', 'hours minutes seconds')


def time_delta2hms(time_delta):
    minutes, seconds = divmod(time_delta.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return HMS(hours % 60, minutes, seconds)


class Clock(object):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.start = DateTime.now()
        self.offset = TimeDelta(hours=hours, minutes=minutes, seconds=seconds)

    def __str__(self):
        return '%02d:%02d:%02d' % self.get_time()

    def get_time(self):
        return time_delta2hms(DateTime.now() - self.start + self.offset)

    @classmethod
    def from_system_time(cls):
        now = DateTime.now()
        return cls(now.hour, now.minute, now.second)


def main():
    clock = Clock.from_system_time()
    while True:
        sys.stdout.write('\r' + str(clock))
        sys.stdout.flush()
        sleep(0.5)


if __name__ == "__main__":
    main()
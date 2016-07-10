import copy
from enum import Enum
import random

class Modes(Enum):
    """An enum to represent the possible 'modes' a queue can be in"""
    normal = "Normal"
    shuffled = "Shuffled"


class SongQueue(object):
    """Class to represent a queue of songs to be played"""

    def __init__(self, songs=[]):
        self.mode = Modes.normal
        self.queues = {}  # This is to hold a serparate queue for shuffling
        self.queues[self.mode] = songs

    @property
    def queue(self):
        """Return the list of songs in the queue corresponding to the mode the queue is in"""
        return self.queues[self.mode]

    def add(self, song):
        """Add a song to the back of the normal queue and in a random position in the
        shuffled queue"""
        print("Adding {} to queue".format(song))

        self.queues[Modes.normal].append(song)

        if Modes.shuffled in self.queues:
            # For shuffled queue pick a random index and insert the new song there
            r = random.randint(0, len(self.queue))
            self.queues[Modes.shuffled].insert(r, song)

    def dequeue(self):
        """Return the song at the front of the queue, or None is queue is empty. If the queue is
        shuffled then remove from the normal queue as well"""
        if len(self.queue) > 0:
            s = self.queue[0]

            for q in self.queues.values():
                q.remove(s)

            return s
        else:
            return None

    def get_length(self):
        """Get the number of songs currently in the queue"""
        return len(self.queue)


    def toggle_shuffle(self):
        """Set the queue mode to shuffled if currently normal and vice versa"""
        if self.mode == Modes.normal:
            self.mode = Modes.shuffled

            # Copy normal queue...
            self.queues[Modes.shuffled] = copy.copy(self.queues[Modes.normal])
            # ...and shuffle it
            random.shuffle(self.queues[Modes.shuffled])

            print("Queue set to shuffled")

        elif self.mode == Modes.shuffled:
            self.mode = Modes.normal

            # Can get rid of the shuffled queue when going back to normal
            del self.queues[Modes.shuffled]

            print("Queue set to normal")

    def __str__(self):
        """String representation of the queue"""
        return ", ".join([str(i) for i in self.queue])

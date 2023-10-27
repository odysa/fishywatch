"""
This module provides a simple implementation of a communication system using asynchronous queues.
It defines generic Sender and Receiver classes for sending and receiving messages, respectively,
and a Channel class that encapsulates a pair of sender and receiver for communication.
"""

from asyncio import Queue
from typing import Generic, TypeVar

_T = TypeVar("_T")


class Sender(Generic[_T]):
    """
    A generic class representing a sender in a channel communication system.

    Attributes:
        q (asyncio.Queue): An asyncio queue for sending items of type _T.

    Methods:
        __init__(self, q: Queue[_T]) -> None:
            Initializes the Sender with the given asyncio queue.

        async def send(self, item: _T) -> None:
            Asynchronously sends an item to the queue.

    """

    q: Queue[_T]

    def __init__(self, q: Queue[_T]) -> None:
        self.q = q

    async def send(self, item: _T) -> None:
        """
        Asynchronously sends an item to the queue.

        Args:
            item (_T): The item to be sent to the queue.

        Returns:
            None
        """
        return await self.q.put(item)


class Receiver(Generic[_T]):
    """
    A generic class representing a receiver in a channel communication system.

    Attributes:
        q (asyncio.Queue): An asyncio queue for receiving items of type _T.

    Methods:
        __init__(self, q: Queue[_T]) -> None:
            Initializes the Receiver with the given asyncio queue.

        async def recv(self) -> _T:
            Asynchronously receives an item from the queue.

        Returns:
            _T: The received item from the queue.

    """

    q: Queue[_T]

    def __init__(self, q: Queue[_T]) -> None:
        self.q = q

    async def recv(self) -> _T:
        """
        Asynchronously receives an item from the queue.

        Returns:
            _T: The received item from the queue.
        """
        return await self.q.get()


class Channel(Generic[_T]):
    """
    A generic class representing a channel for communication between sender and receiver.

    Methods:
        new(cls, max_size: int = 0) -> (Sender[_T], Receiver[_T]):
            Creates a new channel with the specified maximum size.

        Args:
            max_size (int): The maximum size of the channel queue. Defaults to 0 (unbounded).

        Returns:
            tuple: A tuple containing a Sender instance and a Receiver instance.
    """

    @classmethod
    def new(cls, max_size: int = 0) -> (Sender[_T], Receiver[_T]):
        """
        Creates a new channel with the specified maximum size.

        Args:
            max_size (int): The maximum size of the channel queue. Defaults to 0 (unbounded).

        Returns:
            tuple: A tuple containing a Sender instance and a Receiver instance.
        """
        q = Queue[_T](max_size)
        return (Sender(q), Receiver(q))

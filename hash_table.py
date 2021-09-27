from collections import deque
from typing import Any


class HashTable:

    def __init__(self):
        self.__capacity = 4
        self.__keys = [None] * self.__capacity
        self.__values = [None] * self.__capacity
        self.__last_items = deque()

    def __setitem__(self, key, value):
        if None not in self.__keys:
            self.__resize()
        try:
            index = self.__keys.index(key)
            self.__values[index] = value
            return
        except ValueError:
            index = self.__get_index(key)
            self.__keys[index] = key
            self.__last_items.append(key)
            self.__values[index] = value

    def __getitem__(self, key) -> Any:
        try:
            index = self.__keys.index(key)
            return self.__values[index]
        except ValueError:
            raise KeyError(f"Key: {key} not found")

    def __check_index(self, index) -> int:
        """
        Recursive function for handling collisions using linear approach

        :param index: Required. The index to be checked whether is free in the table
        :return: The first possible free index
        """

        if index == len(self.__keys):
            return self.__check_index(0)
        if self.__keys[index] is None:
            return index
        return self.__check_index(index+1)

    def __get_index(self, key) -> int:
        """
        Finding index for the given key to be stored at

        :param key: Required. The key to be found index for
        :return: Integer. Free table index for the key/value pair to be stored at
        """

        index = self.__hash(key)
        available_index = self.__check_index(index)
        return available_index

    def __hash(self, key) -> int:
        """
        Hashing a key to index

        :param key: Required. The key to be hashed to a possibly unique index
        :return: Index (Integer) to be used for storing the key/value at
        """

        index = sum([ord(ch) for ch in str(key)]) % self.__capacity
        return index

    def __resize(self):
        """
        Resize the table
        """

        self.__keys = self.__keys + [None] * self.__capacity
        self.__values = self.__values + [None] * self.__capacity
        self.__capacity *= 2

    def __len__(self) -> int:
        """
        Calculates the length of the used part of the table.

        :return: A number showing the used slots of the table.
        """

        return len([item for item in self.__keys if item is not None])

    def __contains__(self, item):
        return item in self.__keys

    def capacity(self) -> int:
        """
        :return: A number showing the total current capacity of the table.
        """

        return self.__capacity

    def free_space(self) -> int:
        """
        Calculates the current free space of the table.

        :return: A number showing the free slots before next resize
        """

        return self.__capacity - self.__len__()

    def get(self, key, default=None) -> Any:
        """
        Returns the value of the item with the specified key.

        :param key: Required. The keyname of the item you want to return the value from
        :param default: Optional. A value to return if the specified key does not exist.
        Default value is None

        :return: The value of the item with the specified key or None if the key were not found
        """

        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def keys(self) -> tuple:
        """
        Generates a tuple with all the keys currently in the table.

        :return: A tuple containing the keys of the table.
        """

        return tuple(item for item in self.__keys if item is not None)

    def __get_keys(self):
        """
        Generate a list with the keys of the table

        :return: A a list with the keys of the table
        """

        return [item for item in self.__keys if item is not None]

    def values(self) -> tuple:
        """
        Generates a tuple with all the values currently in the table.

        :return: A tuple containing the values of the table.
        """

        keys = self.__get_keys()
        values = tuple(self.get(x) for x in keys)
        return values

    def __get_values(self) -> list:
        """
        Generate a list with the values of the table

        :return: A a list with the values of the table
        """

        keys = self.__get_keys()
        values = [self.get(x) for x in keys]
        return values

    def items(self) -> tuple:
        """
        Generates a tuple of all the key-value pairs currently in the table.

        :return: A tuple containing tuples of the key-value pairs of the table.
        """

        return tuple(zip(self.__get_keys(), self.__get_values()))

    def clear(self):
        """
        Clears the table by resetting to default init
        """

        self.__init__()

    def pop(self, key, default=None) -> Any:
        """
        Removes the specified key from the table.

        :param key: Required. The keyname of the item you want to remove
        :param default: Optional. A value to return if the specified key do not exist.
        If this parameter is not specified, and no item with the specified key is found, an error is raised

        :return: The value of the removed item
        """

        if key not in self.__keys and not default:
            raise KeyError(f"Key: {key} not found")
        value = self.get(key)
        try:
            self.__keys.remove(key)
            self.__values.remove(value)
            self.__last_items.remove(key)
        except ValueError:
            pass
        return value if value else default

    def popitem(self) -> tuple:
        """
        Removes the item that was last inserted into the table

        :return: Tuple of the removed key/value pair
        """

        if not self.__get_keys():
            raise KeyError(f"popitem(): table is empty")
        key = self.__last_items.pop()
        value = self.get(key)
        self.__keys.remove(key)
        self.__values.remove(value)
        return key, value

    def copy(self) -> object:
        """"
        Creates a copy of the specified table

        :return: new instance of the table with all the copied data
        """

        c = HashTable()
        c.__capacity = self.__capacity
        c.__keys = self.__keys
        c.__values = self.__values
        c.__last_items = self.__last_items
        return c

    def setdefault(self, key, value=None) -> Any:
        """
        Returns the value of the item with the specified key.
        If the key does not exist, inserts the key, with the specified value or with None if not specified

        :param key: Required. The keyname of the item you want to return the value from
        :param value: Optional. If the key exist, this parameter has no effect.
        If the key does not exist, this value becomes the key's value. Default value is None.

        :return: The value of the key if the key exists
        """

        if key not in self.__keys:
            self.__setitem__(key, value)
            return
        return self.__getitem__(key)

    def __repr__(self) -> str:
        return f"{dict(zip(self.__get_keys(), self.__get_values()))}"

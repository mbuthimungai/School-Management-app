# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from collections.abc import MutableSequence
from itertools import zip_longest

class ListView(MutableSequence):
    __slots__ = ('source', 'select')

    def __init__(self, source: list, select):
        super().__init__()
        self.source = source
        self.select = select

    # impl MutableSequence

    def __check_key(self, key):
        if not isinstance(key, (int, slice)):
            raise TypeError(f'list indices must be integers or slices, not {type(key).__name__}')

    def __check_value(self, value):
        if not self.select(value):
            raise ValueError

    def __get_real_index(self, index: int):
        'return None if not found'
        def iter_index():
            for i, item in enumerate(self.source):
                if self.select(item):
                    yield i

        def iter_index_rv():
            for i, item in enumerate(reversed(self.source)):
                if self.select(item):
                    yield -1-i

        if index >= 0:
            for i, ri in enumerate(iter_index()):
                if i == index:
                    return ri
        else:
            for i, ri in enumerate(iter_index_rv()):
                if (-1-i) == index:
                    return ri

    def __get_real_indexes(self, key: slice) -> list:
        def iter_index():
            for i, item in enumerate(self.source):
                if self.select(item):
                    yield i
        return list(iter_index())[key]

    def __iter__(self):
        for item in self.source:
            if self.select(item):
                yield item

    def __list__(self):
        return [i for i in self]

    def __tuple__(self):
        return tuple(i for i in self)

    def __reversed__(self):
        for item in reversed(self.source):
            if self.select(item):
                yield item

    def __delitem__(self, key):
        self.__check_key(key)

        if isinstance(key, int):
            real_index = self.__get_real_index(key)
            if real_index is None:
                raise IndexError('list assignment index out of range')
            del self.source[real_index]
        elif isinstance(key, slice):
            for i in reversed(self.__get_real_indexes(key)):
                self.source.pop(i)
        else:
            raise NotImplementedError

    def __getitem__(self, key):
        self.__check_key(key)

        if isinstance(key, int):
            real_index = self.__get_real_index(key)
            if real_index is None:
                raise IndexError('list assignment index out of range')
            return self.source[real_index]
        elif isinstance(key, slice):
            return [self.source[i] for i in self.__get_real_indexes(key)]
        else:
            raise NotImplementedError

    def __setitem__(self, key, value):
        self.__check_key(key)

        if isinstance(key, int):
            self.__check_value(value)
            real_index = self.__get_real_index(key)
            if real_index is None:
                raise IndexError('list assignment index out of range')
            self.source[real_index] = value
        elif isinstance(key, slice):
            for item in value:
                self.__check_value(item)
            fillvalue = object()
            indexmaps = list(zip_longest(self.__get_real_indexes(key), value, fillvalue=fillvalue))
            for f, t in reversed(indexmaps):
                if f is fillvalue:
                    self.source.append(value)
                elif t is fillvalue:
                    self.source.pop(f)
                else:
                    self.source[f] = t
        else:
            raise NotImplementedError

    def __len__(self):
        return sum(1 for _ in self)

    def insert(self, index, object):
        self.__check_value(object)

        if index >= len(self.source):
            # fast path without enumerate
            self.source.append(object)
            return

        real_index = self.__get_real_index(index)
        if real_index is None:
            self.source.append(object)
        else:
            self.source.insert(real_index, object)

    def append(self, object):
        'Append object to the end of the list.'
        self.source.append(object)

    def extend(self, iterable):
        'Extend list by appending elements from the iterable.'
        self.source.extend(iterable)

    # impl list

    def __add__(self, other):
        return self.__list__().__add__(other)

    def __rmul__(self, other):
        return self.__list__().__rmul__(other)

    def __mul__(self, other):
        return self.__list__().__mul__(other)

    def __imul__(self, other):
        return self.__list__().__imul__(other)

    def copy(self):
        'copy source list and make a same view.'
        return ListView(self.source.copy(), self.select)

    def sort(self, *, key=None, reverse=False):
        items = self.__list__()
        items.sort(key=key, reverse=reverse)
        self[:] = items

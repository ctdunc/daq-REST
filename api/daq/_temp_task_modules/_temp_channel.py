class _TempChannel:
    def __init__(self, channel_name, daqmx_function, **kwargs):
        self.channel_name = channel_name
        self.daqmx_function = daqmx_function
        self.kwargs = kwargs

class _TempChannelCollection(list):
    def __init__(self, iterable=None):
        super(_TempChannelCollection, self).__init__()
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, item):
        if isinstance(item, _TempChannel):
            super(_TempChannelCollection, self).append(item)
        else:
            raise ValueError("Incorrect type for channel collection")

    def insert(self, index, item):
        if isinstance(item, _TempChannel):
            super(_TempChannelCollection, self).insert(index, item)
        else:
            raise ValueError("Incorrect type for channel collection")

    
    def __add__(self, item):
        if isinstance(item, _TempChannel):
            super(_TempChannelCollection, self).__add__(item)
        else:
            raise ValueError("Incorrect type for channel collection")

    def __iadd__(self, item):
        if isinstance(item, _TempChannel):
            super(_TempChannelCollection, self).__iadd__(item)
        else:
            raise ValueError("Incorrect type for channel collection")

def _convert_chan_from_max():
    return 0

def _convert_chan_coll_from_max(channel_collection):
    for channel in channel_collection:
        print(channel)
    return 0

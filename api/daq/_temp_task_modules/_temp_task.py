from _temp_channel import _TempChannel, _TempChannelCollection

class _TempTask:
    def __init__(self, task_id):
        self.task_id = task_id

    def load_attributes_from_max():

        return 0
    @property
    def ai_channels(self):
        return self.__ai_channels

    @ai_channels.setter
    def ai_channels(self, channels):
        if isinstance(channels, _TempChannelCollection): 
            self.__ai_channels = channels
        else:
            raise ValueError("Attribute must be of type _TempChannelCollection")


    @property
    def di_channels(self):
        return self.__di_channels

    @di_channels.setter
    def di_channels(self, channels):
        if isinstance(channels, _TempChannelCollection): 
            self.__di_channels = channels
        else:
            raise ValueError("Attribute must be of type _TempChannelCollection")
            

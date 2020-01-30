import nidaqmx
from _temp_channel import _convert_chan_coll_from_max

sy = nidaqmx.system.System.local()
task = sy.tasks[0].load()
_convert_chan_coll_from_max(task.ai_channels)

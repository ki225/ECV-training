import asyncio
import enum as Enum

# 4 corporate status: PENDING, RUNNING, CANCELLED, FINISHED
class ResultState(Enum):
    PENDING = 'PENDING' # not yet started
    RUNNING = 'RUNNING' # in event loop
    CANCELLED = 'CANCELLED' # break from event loop
    FINISHED = 'FINISHED' # done

class CommandResult:
    def __init__(self):
        self._future = asyncio.Future() # future object
        self._output = ""

    def set_cancelled(self):
        self._future.cancelled()

    def set_finished(self, result):
        self._future.set_result(result)

    def set_running(self):
        self._state = ResultState.RUNNING

    # set the Future obj is finished and raise an exception
    def set_exception(self, exception):
        self._future.set_exception() = exception

    def set_result(self, result):
        if not self._future.done():
            self._future.set_result(result)
    
    def set_output(self, output):
        self._output = output

    def get_output(self):
        return self._output
            
    async def wait(self):
        if self._future is None:
            raise RuntimeError("No command has been run yet")
        return await self._future
        

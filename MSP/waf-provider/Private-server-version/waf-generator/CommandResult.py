import asyncio
import enum as Enum

class ResultState(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    CANCELLED = 'CANCELLED'
    FINISHED = 'FINISHED'

class CommandResult:
    def __init__(self):
        self._state = ResultState.PENDING
        self._exception = None
        self._future = asyncio.Future() # future object
        self._result = None

    def set_cancelled(self):
        self._state = ResultState.CANCELLED

    def set_finished(self):
        self._state = ResultState.FINISHED

    def set_running(self):
        self._state = ResultState.RUNNING

    def set_exception(self, exception):
        self._exception = exception

    def set_result(self, result):
        if not self._future.done():
            self._future.set_result(result)
            
    async def wait(self):
        if self._future is None:
            raise RuntimeError("No command has been run yet")
        return await self._future
        

import asyncio
import enum as Enum

# 4 corporate status: PENDING, RUNNING, CANCELLED, FINISHED
# class ResultState(Enum):
#     PENDING = 'PENDING' # not yet started
#     RUNNING = 'RUNNING' # in event loop
#     CANCELLED = 'CANCELLED' # break from event loop
#     FINISHED = 'FINISHED' # done


# inherent from CommandState
class CommandResult:
    def __init__(self, customer_id):
        self._customer_id = customer_id
        self._future = asyncio.Future() # future object
        self._output = ""
        self._alive = True

    @property
    def customer_id(self):
        return self._customer_id
    
    def set_cancelled(self):
        self._future.cancelled()

    def set_finished(self, result):
        self._future.set_result(result)


    # set the Future obj is finished and raise an exception
    def set_exception(self, exception):
        self._future.set_exception() 

    def set_result(self, result):
        if not self._future.done():
            self._future.set_result(result)
    
    def set_output(self, output):
        if output != None:
            self._output = output

    def get_output(self):
        return self._output
            
    async def wait(self):
        if self._future is None:
            raise RuntimeError("No command has been run yet")
        return await self._future
    
    def set_death(self):
        self._alive = False
        

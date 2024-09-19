class stopEvent:
    def __init__(self):
        
        self.stop_event = False
    # Generate stopped signal
    def set(self):
        self.stop_event = True
    def is_set(self):
        return self.stop_event
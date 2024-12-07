import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0

    def start(self):
        """Start the timer."""
        self.start_time = time.perf_counter()

    def stop(self):
        """Stop the timer and calculate the elapsed time."""
        if self.start_time is not None:
            self.elapsed += time.perf_counter() - self.start_time
            self.start_time = None

    def elapsed_time(self):
        """Get the total elapsed time."""
        if self.start_time is not None:
            return self.elapsed + (time.perf_counter() - self.start_time)
        return self.elapsed

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.elapsed = 0

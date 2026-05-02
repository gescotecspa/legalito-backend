import time
from collections import defaultdict, deque
from threading import Lock


class InMemoryRateLimiter:
    def __init__(self):
        self._attempts = defaultdict(deque)
        self._lock = Lock()

    def hit(self, key, limit, window_seconds):
        now = time.time()

        with self._lock:
            attempts = self._attempts[key]
            cutoff = now - window_seconds

            while attempts and attempts[0] <= cutoff:
                attempts.popleft()

            if len(attempts) >= limit:
                retry_after = max(1, int(attempts[0] + window_seconds - now))
                return False, retry_after

            attempts.append(now)
            return True, None

    def reset(self):
        with self._lock:
            self._attempts.clear()


rate_limiter = InMemoryRateLimiter()

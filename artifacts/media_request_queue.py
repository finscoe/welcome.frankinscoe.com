import heapq
import hashlib
import pickle
import os

class MediaRequestQueue:
    def __init__(self):
        self._queue = []
        self._request_hashes = set()

    def _hash_request(self, request):
        request_str = f"{request['title']}-{request['user']}"
        return hashlib.sha256(request_str.encode()).hexdigest()

    def add_request(self, request, priority=5):
        req_hash = self._hash_request(request)
        if req_hash in self._request_hashes:
            print(f"Duplicate request detected: {request['title']} by {request['user']}")
            return False
        heapq.heappush(self._queue, (priority, request))
        self._request_hashes.add(req_hash)
        print(f"Added request: {request['title']} by {request['user']} with priority {priority}")
        return True

    def pop_request(self):
        if self._queue:
            priority, request = heapq.heappop(self._queue)
            req_hash = self._hash_request(request)
            self._request_hashes.discard(req_hash)
            print(f"Processing request: {request['title']} by {request['user']}")
            return request
        else:
            print("No requests to process.")
            return None

    def save_queue(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump((self._queue, self._request_hashes), f)
        print(f"Queue saved to {filepath}")

    def load_queue(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self._queue, self._request_hashes = pickle.load(f)
            print(f"Queue loaded from {filepath}")
        else:
            print(f"No existing queue file found at {filepath}")

    def show_queue(self):
        if not self._queue:
            print("Queue is empty.")
            return
        print("Current request queue:")
        for priority, request in sorted(self._queue):
            print(f"Priority {priority}: {request['title']} by {request['user']}")

# Example usage
if __name__ == "__main__":
    queue = MediaRequestQueue()
    queue.add_request({'title': 'Inception', 'user': 'alice'}, priority=1)
    queue.add_request({'title': 'Interstellar', 'user': 'bob'}, priority=3)
    queue.add_request({'title': 'Inception', 'user': 'alice'}, priority=2)  # Duplicate
    queue.show_queue()
    queue.pop_request()
    queue.show_queue()
    queue.save_queue('media_queue.pkl')

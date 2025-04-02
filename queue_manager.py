import json
import os
from collections import deque
from pathlib import Path

class EmailQueue:
    def __init__(self, max_size=3):
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)
        self.queue_file = Path("email_queue.json")
        self.load_queue()

    def load_queue(self):
        """Load the queue from file if it exists"""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
                    self.queue = deque(data, maxlen=self.max_size)
            except Exception as e:
                print(f"Error loading queue: {e}")

    def save_queue(self):
        """Save the queue to file"""
        try:
            with open(self.queue_file, 'w') as f:
                json.dump(list(self.queue), f)
        except Exception as e:
            print(f"Error saving queue: {e}")

    def add_email(self, email):
        """Add an email to the queue if it's not full"""
        if len(self.queue) < self.max_size:
            self.queue.append(email)
            self.save_queue()
            return True
        return False

    def get_next_email(self):
        """Get and remove the next email from the queue"""
        if self.queue:
            email = self.queue.popleft()
            self.save_queue()
            return email
        return None

    def is_full(self):
        """Check if the queue is full"""
        return len(self.queue) >= self.max_size

    def get_queue_size(self):
        """Get current queue size"""
        return len(self.queue)

# Create a global instance of the queue
email_queue = EmailQueue(max_size=3) 
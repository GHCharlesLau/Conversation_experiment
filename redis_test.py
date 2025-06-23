import redis
import uuid

# Instantiate a Redis client, connecting to localhost on port 6379
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0  # The default Redis database index
)

#%% Strings in Redis
# 1. SET command: store a string under 'mykey'
r.set("mykey", "hello from Windows")

# 2. GET command: retrieve the value stored at 'mykey'
value = r.get("mykey")
print(value)   # Output is b'hello from Windows', since redis-py returns bytes.

# 3. Convert bytes to string
print(value.decode())  # prints "hello from Windows"

# 4. DEL command: remove 'mykey' from Redis
r.delete("mykey")

# Example: Storing and retrieving user sessions
def store_user_session(user_id):
    """
    Generates a unique session token (UUID) for a user and stores it in Redis.
    The session is stored under the key pattern: user:{user_id}:session
    """
    session_key = f"user:{user_id}:session"
    token = str(uuid.uuid4())   # Generate a random UUID as a session token
    r.set(session_key, token)   # Store token in Redis
    return token

def get_user_session(user_id):
    """
    Retrieves the stored session token for the given user_id.
    Returns None if the session does not exist or is expired.
    """
    session_key = f"user:{user_id}:session"
    token = r.get(session_key)
    return token.decode('utf-8') if token else None

def delete_user_session(user_id):
    """
    Deletes the session entry from Redis for the specified user_id.
    """
    session_key = f"user:{user_id}:session"
    r.delete(session_key)

# Usage demonstration
session_token = store_user_session(1001)
print(f"Stored session token: {session_token}")

retrieved_token = get_user_session(1001)
print(f"Retrieved session token: {retrieved_token}")

delete_user_session(1001)
print(f"Session after delete: {get_user_session(1001)}")  # Should be None or empty


#%% Lists in Redis
"""
Redis Lists are ordered sequences of strings. 
They allow operations on both ends, making them handy for queues, stacks, or logs.
"""
# LPUSH: Push an element to the head (left) of the list
r.lpush("task_queue", "task1")

# RPUSH: Push an element to the tail (right) of the list
r.rpush("task_queue", "task2")
r.rpush("task_queue", "task3")

# LPOP: Pop (remove and return) the element at the head
task = r.lpop("task_queue")
print(task)  # b'task1'

# Optional: RPOP removes and returns the element at the tail
task = r.rpop("task_queue")
print(task)  # b'task3'

# Example: Implementing a simple Redis-backed queue
def enqueue_task(queue_name, task):
    """
    Appends a task to the end (right) of the Redis list named queue_name.
    """
    r.rpush(queue_name, task)

def dequeue_task(queue_name):
    """
    Removes a task from the front (left) of the Redis list named queue_name.
    Returns the task as a string, or None if the queue is empty.
    """
    task = r.lpop(queue_name)
    return task.decode('utf-8') if task else None

# Example usage:
enqueue_task("my_queue", "send_email")
enqueue_task("my_queue", "generate_report")

while True:
    task = dequeue_task("my_queue")
    if not task:
        print("No more tasks in queue.")
        break
    print(f"Processing task: {task}")


#%% Hashes in Redis
'''
Hashes are similar to Python dictionaries but stored in Redis. 
They're best for grouping related fields (e.g., user details).
'''
# HSET: Store 'name' and 'email' fields for a user hash key
r.hset("user:1001", "name", "Alice")
r.hset("user:1001", "email", "alice@example.com")

# HGET: Retrieve a single field from the hash
email = r.hget("user:1001", "email")
print(email.decode('utf-8'))  # alice@example.com

# HDEL: Remove a field from the hash
r.hdel("user:1001", "email")

# Example: Storing and accessing structured user profiles
def create_user_profile(user_id, name, email):
    """
    Creates a user profile in Redis under the key 'user:{user_id}'.
    'name' and 'email' are stored as separate fields in the hash.
    """
    user_key = f"user:{user_id}"
    r.hset(user_key, mapping={"name": name, "email": email})

def get_user_profile(user_id):
    """
    Retrieves and returns all fields in the user profile hash
    as a Python dictionary. Keys and values are decoded from bytes.
    """
    user_key = f"user:{user_id}"
    profile_data = r.hgetall(user_key)
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in profile_data.items()}

def delete_user_profile(user_id):
    """
    Deletes the entire user profile key from Redis.
    """
    user_key = f"user:{user_id}"
    r.delete(user_key)

# Usage demonstration
create_user_profile(1002, "Bob", "bob@example.com")
print(get_user_profile(1002))  # e.g. {'name': 'Bob', 'email': 'bob@example.com'}
delete_user_profile(1002)

#%% Sets and Sorted Sets
"""
Sets are collections of unique values, 
while sorted sets are collections of key-value pairs with a score associated with each value.
"""
# Sets
# SADD: Add multiple members to a set
r.sadd("tags:python", "redis", "windows", "backend")

# SMEMBERS: Retrieve all unique members in the set
tags = r.smembers("tags:python")
print(tags)  # {b'redis', b'windows', b'backend'}

# Sorted Sets
# ZADD: Add members with scores
r.zadd("leaderboard", {"player1": 10, "player2": 20})

# ZRANGE: Retrieve members in ascending order of score
leaders = r.zrange("leaderboard", 0, -1, withscores=True)
print(leaders)  # [(b'player1', 10.0), (b'player2', 20.0)]

# Example: Managing tags or leaderboards
def add_tag(post_id, tag):
    """
    Adds a 'tag' to the set of tags belonging to a specific post.
    Each post has its own set under 'post:{post_id}:tags'.
    """
    r.sadd(f"post:{post_id}:tags", tag)

def get_tags(post_id):
    """
    Retrieves all tags for a specific post, decoding the bytes into strings.
    """
    raw_tags = r.smembers(f"post:{post_id}:tags")
    return {tag.decode('utf-8') for tag in raw_tags}

def update_leaderboard(player, score):
    """
    Updates or inserts a player's score in the 'game:leaderboard' sorted set.
    A higher score indicates a better position if sorting descending.
    """
    r.zadd("game:leaderboard", {player: score})

def get_leaderboard():
    """
    Returns an ascending list of (player, score) tuples from the leaderboard.
    To invert the sorting (highest first), you'd use ZREVRANGE.
    """
    entries = r.zrange("game:leaderboard", 0, -1, withscores=True)
    return [(player.decode('utf-8'), score) for player, score in entries]

# Usage demonstration
add_tag(123, "python")
add_tag(123, "redis")
print(get_tags(123))

update_leaderboard("Alice", 300)
update_leaderboard("Bob", 450)
print(get_leaderboard())

#%% Advanced topic: Using Pub/Sub with Redis
"""
Pub/Sub (Publish/Subscribe) is a popular messaging pattern for real-time communication. 
Publishers send messages to a channel, and all subscribers to that channel receive the messages.
"""
import threading

def subscriber(r, channel_name):
    """
    Subscribes to the given Redis channel and listens for messages.
    When a new message is published on that channel, it is printed.
    """
    pubsub = r.pubsub()
    pubsub.subscribe(channel_name)
    print(f"Subscribed to {channel_name}")

    # pubsub.listen() yields messages from the subscribed channel(s) in real time
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")

def publisher(r, channel_name, message):
    """
    Publishes a message to the specified Redis channel.
    All subscribers to this channel immediately receive the message.
    """
    r.publish(channel_name, message)

# Example usage
channel = "updates"

# Start subscriber in a separate thread to avoid blocking the main thread
sub_thread = threading.Thread(target=subscriber, args=(r, channel))
sub_thread.start()

# Publish messages
publisher(r, channel, "Hello from Windows!")
publisher(r, channel, "Another update!")


#%%
if __name__ == "__main__":
    print("Redis test completed successfully.")

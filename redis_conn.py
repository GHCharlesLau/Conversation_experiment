import os
import urllib.parse as urlparse
import redis
import json
from datetime import datetime, timezone
from snowflake import SnowflakeGenerator  # for generating unique channel IDs

# Instantiate a Redis client
url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

# Or, connecting to localhost on port 6379
# r = redis.Redis(
#     host='localhost',
#     port=6379,
#     db=0  # The default Redis database index
# )


# Create a pub/sub object
pubsub = r.pubsub()

def publish_message(group_id, player, text):
    """Publish a message to a channel"""
    channel = f"group:{group_id}"
    timestamp = datetime.now(timezone.utc).timestamp()
    message = dict(timestamp=timestamp, player=player, text=text)
    r.publish(channel, json.dumps(message))

def subscribe_message(group_id):
    """Subscribe to a channel"""
    channel = f"group:{group_id}"
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        # message = json.loads(message)
        yield message

# publish_message('channel_test', 'player1', 'Hello, Redis!')

# msg = next(subscribe_message('channel_test'))
# print(msg['data'].decode('utf-8'))


# Store data using hashs
def store_message(group_id, player_id, text):
    """Store a message in Redis"""
    group_key = f"group:{group_id}:{player_id}"  # Separately store messages from each player in the group
    timestamp = datetime.now(timezone.utc).timestamp()
    sender = player_id
    r.hset(group_key, 
           mapping={'timestamp': timestamp, 
                    'sender': sender,
                    'text': text})
    
# Retrieve data using hashs
def retrieve_message(group_id, player_id):
    group_key = f"group:{group_id}:{player_id}"
    message = r.hgetall(group_key)
    return message


if __name__ == "__main__":
    pass
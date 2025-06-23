import os
import urllib.parse as urlparse
import redis
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

def publish_message(channel, message):
    """Publish a message to a channel"""
    r.publish(channel, message)

def subscribe_message(channel):
    """Subscribe to a channel"""
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        yield message
import json
from models import Authors, Quotes
import redis
from connect import connect
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, password=None)
cache_time = 3600 # 1 hour


def RedisLRU(cache_name, expiration_time=cache_time, max_size=100):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{cache_name}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"
            result = redis_client.get(key)
            if result:
                return f"from cache: {json.loads(result)}"
            else:
                result = func(*args, **kwargs)
                redis_client.setex(key, expiration_time, json.dumps(result))
                # Implement LRU eviction
                if redis_client.llen(cache_name) > max_size:
                    oldest_key = redis_client.lpop(cache_name)
                    redis_client.delete(oldest_key)
                redis_client.rpush(cache_name, key)
                return result
        return wrapper
    return decorator

@RedisLRU("author_cache")
def search_by_author(author_name):
    author = Authors.objects(fullname__istartswith=author_name).first()
    if author:
        quotes = Quotes.objects(author=author)
        result = [quote.quote for quote in quotes]
        return result[0]
    else:
        return []

@RedisLRU("tag_cache")
def search_by_tag(tag):
    quotes = Quotes.objects(tags__name__istartswith=tag)
    result = [quote.quote for quote in quotes]
    return result[0]

@RedisLRU("tags_cache")
def search_by_tags(tags):
    tag_list = tags.split(',')
    quotes = Quotes.objects(tags__name__in=tag_list)
    result = [quote.quote for quote in quotes]
    return result[0]


while True:
    input_command = input("Enter information in format - command: value - ")
    split_command = input_command.split(": ")
    match split_command[0]:
        case 'name':
            print(search_by_author(split_command[1]))
        case 'tag':
            print(search_by_tag(split_command[1]))
        case 'tags':
            print(search_by_tags(split_command[1]))
        case 'exit':
            break
        case _:
            raise ValueError("Enter valid information in format - command: value")

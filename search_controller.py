# Summary: Construct a Redis Search Index with String Prefixes using Sorted Sets & Hashes.
import redis
import json
from disk_to_mem import DiskToMem
from string_to_prefixes import StringToPrefixes
from match_prefixes import MatchPrefixes

class searchController:
    def __init__(self, srch_string):
        self.srch_string = srch_string.lower()
        # Convert the search_str to it's prefixes(StringToPrefixes will return a dict).
        self.srch_prefixes = StringToPrefixes(self.srch_string).get()
        # Initialize the connection to redis.
        self.r = redis.StrictRedis(host = 'HOST ADDRESS', port = <PORT NUMBER>, db = 0)
        # Define redis hash key 
        self.hash_key = "lxp-data:all"
        # Define redis sorted set partial name (The real sorted set will have the prefix appended ex. lxp-index:all:ta).
        self.sorted_set_partial_key = "lxp-index:all"
        
    def check_redis_hash(self):
        # Check redis hash object to ensure that the data has persisted, if not rebuild them from disk.
        if not self.r.hexists(self.hash_key, 100):
            # Send redis connection so we don't have to connect again.
            rebuild = DiskToMem(self.hash_key, self.r, self.sorted_set_partial_key) 
    
    def match_prefixes(self):
        self.matches = {}
        # Compare prefixes to the Sorted Set and find a match
        # Returns a list of corresponding hash_object fields
        self.matches = MatchPrefixes(self.srch_prefixes, self.sorted_set_partial_key, self.r).get()
    
    def get_hash_objects(self):
        r = self.r
        self.results = []
        # Retrieve the data stored in the hash object using the keys and fields returned by MatchPrefixes
        for hash_field in self.matches:
            hash_object = r.hget(self.hash_key, hash_field)
            # Convert json data to dictionary 
            json_to_dict = json.loads(hash_object)
            # Append formatted data to the results
            self.results.append(json_to_dict)

    def get_search_results(self):
        return self.results

def search(srch_string):
    # Initialize the search
    search = searchController(srch_string)
    # 1.) Check if disk data still exists in redis.
    search.check_redis_hash()
    # 2.) Match existing redis prefix sorted sets with the prefixes in the search string.
    search.match_prefixes()
    # 3.) Using the matching hashes get the hash objects
    search.get_hash_objects()
    # 4.) Get and return the search results
    return search.get_search_results()
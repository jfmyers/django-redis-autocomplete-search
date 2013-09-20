import json
from string_to_prefixes import StringToPrefixes
from contributions.models import Posts
from tags.models import Tags
from userProfile.models import Profile

class DiskToMem:
    def __init__(self, hash_key, redis_connection, sorted_set_partial_key):
        self.hash_key = hash_key
        self.sorted_set_partial_key = sorted_set_partial_key
        self.r = redis_connection
        #Initialize by calling method get_from_disk
        self.get_from_disk()
        self.format_disk_data()
        self.save_to_redis_hash()
    
    def get_from_disk(self):
        # Get experiences, tags and profiles from disk
        posts = Posts.objects.all()
        tags = Tags.objects.all() 
        people = Profile.objects.all()
        self.disk_data = {"experiences":posts, "people":people, "tags":tags}
        
    def save_to_redis_hash(self):
        # The hash object contains information on experiences, people or tags.
        r = self.r
        hash_key = self.hash_key
        data = self.formatted_data_list
        for (counter, data_dict) in enumerate(data):
            data_json = json.dumps(data_dict)
            # Save this data to redis hash, using the hash_key and the field as the counter.
            r.hset(hash_key, counter, data_json)
            # Save the prefixes of the data title to redis sorted set, counter is the hash key's field
            self.save_to_redis_sorted_set(data_dict["title"], counter)
        
            
    def save_to_redis_sorted_set(self, string, field):
        # The sorted set is the search index.
        r = self.r
        ss_partial_key = self.sorted_set_partial_key
        # StringToPrefixes will return a dict containing the prefixes for each word and each word as a key.
        prefix_dict = StringToPrefixes(string).get()
        for key, prefix_word in prefix_dict.iteritems():
            for prefix in prefix_word:
                sorted_set_key = ss_partial_key+":"+prefix
                r.zadd(sorted_set_key, 0, field)
    
    def format_disk_data(self):
        disk_data = self.disk_data
        # Get only the data we need for search(pk, type, title, handle)
        formatted_data_list = []
        for key, data_models in disk_data.iteritems():
            for data in data_models:
                formatted_data = {}
                if key == "experiences":
                    formatted_data["pk"] = data.id
                    formatted_data["type"] = "Experience"
                    formatted_data["title"] = data.title.title()
                    formatted_data["handle"] = data.url
    
                elif key == "people":
                    formatted_data["pk"] = data.id
                    formatted_data["type"] = "Person"
                    formatted_data["title"] = data.fname.title()+" "+data.lname.title()
                    formatted_data["handle"] = data.handle
            
                elif key == "tags":
                    formatted_data["pk"] = data.id
                    formatted_data["type"] = "Career Topic"
                    formatted_data["title"] = data.name.title()
                    formatted_data["handle"] = data.handle
                    
                formatted_data_list.append(formatted_data)
            
        self.formatted_data_list = formatted_data_list
class MatchPrefixes:
    def __init__(self, srch_prefixes, partial_redis_ss_key, redis_connection):
        self.srch_prefixes = srch_prefixes
        self.sorted_set_partial_key = partial_redis_ss_key
        self.r = redis_connection
        
        # Start matching...
        self.match()
        self.find_intersection()
    
    def match(self):
        r = self.r
        srch_prefixes = self.srch_prefixes
        ss_partial_key = self.sorted_set_partial_key
        self.matches = {}
        for key, word in srch_prefixes.iteritems():
            for prefix in word:
                sorted_set = ss_partial_key + ":" + prefix
                # Returns a list of hash fields corresponding to the hash_object
                hash_fields = r.zrange(sorted_set, 0, -1)
                if hash_fields:
                    self.matches[key] = hash_fields
                    break
                    
    def find_intersection(self):
        self.result = []
        match_length = len(self.matches)
        if match_length > 1:
            # Find where the intersection occurs and return that list
            self.result = reduce( set.intersection, ( set(val) for val in self.matches.values() ) )
        else:
            for key, hash_field_list in self.matches.iteritems():
                for hash_field in hash_field_list:
                    self.result.append(hash_field)

    def get(self):
        return self.result     
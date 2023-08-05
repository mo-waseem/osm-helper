import hashlib

def get_hashed_str(long_string):
    long_string_bytes = long_string.encode('utf-8')
    
    sha256_hash = hashlib.sha256(long_string_bytes).hexdigest()
    
    hashed_data = sha256_hash[:20]
    
    return hashed_data
import hashlib  
  
def hash_read_file(fileName):
  
    h1 = hashlib.sha1()
    with open(fileName, "rb") as file:
  
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h1.update(chunk)
              
    # 160bit digest should be enough
    return h1.hexdigest()

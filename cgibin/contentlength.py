import os
length = os.getenv('CONTENT_LENGTH')
if length is None:
    exit(-1)
print("<h1>{}</h1>".format(length))
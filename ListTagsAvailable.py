from PIL.ExifTags import TAGS
# Small helper to list all available tagnames/nrs in PIL.ExifTags

_TAGS_r = dict(((v, k) for k, v in TAGS.items()))
print(">>> Know TAGS names that can be set")
print(">>>(Note that Different TAGS can have different datatype)<<<")
print(">>>(     This project only sets/adds STRING datatype values (which is default datatype)<<<")
for tag in _TAGS_r:
    print("TagName: " , tag,  ",TagNr:" ,  _TAGS_r[f'{tag}'])
#

# read setup file
with open('data.txt') as file:
    api_id = file.readline().split('=')
    hash_id = file.readline().split('=')

    api_id = int(api_id[1])
    hash_id=hash_id[1]

print(api_id)
print(hash_id)
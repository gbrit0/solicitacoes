import random, string

for i in range(5):
   print(''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
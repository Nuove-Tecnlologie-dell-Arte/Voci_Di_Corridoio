import os
folder = 'wav/'
prova= len([f for f in os.listdir(folder)if os.path.isfile(os.path.join(folder, f))])
print(prova)

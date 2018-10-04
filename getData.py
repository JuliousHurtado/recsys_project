import argparse
import os
import numpy as np


def checkFileExists(filename):
    if os.path.exists(filename):
        return True
    else:
        print("Archivo no encontrado: ", filename)

class User(object):
    def __init__(self, uid, age, gender, occupation):
        self.id = uid
        self.age = age
        self.gender = gender
        self.occupation = occupation

        self.setVectorGender()

    def setVectorOccupation(self, list_occupation):
        self.vec_occupation = np.zeros(len(list_occupation))
        self.vec_occupation[list_occupation.index(self.occupation)] = 1

    def setVectorGender(self):
        self.vec_gender = np.zeros(2)
        if self.gender == 'M':
            self.vec_gender[0] = 1
        else:
            self.vec_gender[1] = 1

class Users(object):
    def __init__(self, path):
        self.unique_occupation = []
        self.users = {}
        self.path = path

        self.getOccupation()
        self.getUsers()
            
    def getOccupation(self):
        filename = self.path + 'u.occupation'
    
        if checkFileExists(filename):
            with open(filename) as file:  
                for line in file:
                    self.unique_occupation.append(line.strip())

    def getUsers(self):
        filename = self.path + 'u.user'

        if checkFileExists(filename):
            with open(filename) as file:  
                for line in file:
                    context = line.split('|')
    
                    self.users[context[0]] = User(context[0], context[1], context[2], context[3])
                    self.users[context[0]].setVectorOccupation(self.unique_occupation)

class Item(object):
    def __init__(self, uid, title, r_date, v_date, url, categories):
        self.id = uid
        self.title = title
        self.r_date = r_date
        self.v_date = v_date
        self.url = url
        self.categories = [ int(c) for c in categories ]    

class Items(object):
    def __init__(self, path):
        self.unique_genres = []
        self.path = path
        self.items = {}

        self.getGenres()
        self.getItems()

    def getGenres(self):
        filename = self.path + 'u.genre'
    
        if checkFileExists(filename):
            with open(filename) as file:  
                for line in file:
                    self.unique_genres.append(line.split('|')[0])

    def getItems(self):
        filename = self.path + 'u.item'
    
        if checkFileExists(filename):
            with open(filename, encoding = "ISO-8859-1") as file:  
                for line in file:
                    context = line.strip().split('|')

                    self.items[context[0]] = Item(context[0], context[1], context[2], context[3], context[4], context[5:])

class Relations(object):
    def __init__(self, path):
        self.relation = None
        self.path = path + 'u.data'

    def setRelations(self, n_items, n_users):
        self.relation = np.zeros((n_users,n_items))
        
        if checkFileExists(self.path):
            with open(self.path) as file:
                for line in file:
                    context = line.strip().split('\t')[:3]
                    context = [ int(c) for c in context ]

                    self.relation[context[0]-1,context[1]-1] = context[2]

    def getNeighbour(self,uid,user = True):
        if user:
            return np.argwhere(self.relation[uid,:] > 0)
        else:
            return np.argwhere(self.relation[:,uid] > 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path',default='./', help='path to the dataset')
    args = parser.parse_args()

    u = Users(args.path)
    print(len(u.users))

    i = Items(args.path)
    print(len(i.items))

    r = Relations(args.path)
    r.setRelations(len(i.items),len(u.users))

    print(r.getNeighbour(305))
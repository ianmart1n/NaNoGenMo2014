import random
import re
import os
import string
import urllib2
 
class Book():
  
    def __init__(self):
        # lists of words i need
        self.sourceDb = {} 

        # keep track of things unique to a playthrough
        self.town = ""
        self.event = ""
        self.concept = ""
        self.affected = {'name':"",'relation':""}
        self.locations = []
        self.relatives = []

        self.output = ""
  

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = re.split('\n', data)
        return words

    def get_words(self, open_file):
        self.open_file = open_file
        words = self.file_to_words()
        dbName = os.path.basename(open_file.name)
        dbName = dbName[:-4]
        words_size = len(words)
        for i in xrange(words_size):
            if dbName in self.sourceDb:
                self.sourceDb[dbName].append(words[i])
            else:
                self.sourceDb[dbName] = [words[i]]

    def make_databases(self):
        directory_name = os.getcwd() + "/words2"
        for file in os.listdir(directory_name):
            if file.endswith(".txt"):
                open_file = open(directory_name+"/"+file)
                self.get_words(open_file);


    # This function will only handle word grabs. TODO: make it do ALL of the *words*
    def replace_words(self, string):
        while "*" in string:
            m = re.search('\*(.+?)\*', string)
            if m:
                word = m.group(1)
                replacer = "*"+word+"*"
                string = string.replace(replacer, random.choice(self.sourceDb[word]))
        return string

    def make_stuff(self):
       for i in xrange(len(self.sourceDb["concept"])):
            self.output = self.output + "CHAPTER "+str(i+1)+"\n\n"
            self.output = self.output + "I asked everyone I met what they think "+self.sourceDb["concept"][i]+" is.\n\n"
            for j in range(0,1000):
                r = random.randint(1, 4)
                if r == 1:
                    musing = self.replace_words(random.choice(self.sourceDb["name"]) + " says they think "+self.sourceDb["concept"][i]+" is maybe a *noun*. ")
                elif r == 2:
                    musing = self.replace_words(random.choice(self.sourceDb["name"]) + " said that "+self.sourceDb["concept"][i]+" is like a *noun*. ")
                elif r == 3:
                    musing = self.replace_words("I remember "+random.choice(self.sourceDb["name"]) + " insisted "+self.sourceDb["concept"][i]+" is a *noun*. ")
                elif r == 4:
                    musing = self.replace_words("When I asked "+ random.choice(self.sourceDb["name"]) + " they said "+self.sourceDb["concept"][i]+" is a *noun*. ")
                self.output = self.output + musing
            self.output = self.output + "\n\n"

    def generate_story(self):
        # open file
        write_file = open("book.txt", "w+")

        self.output = "Maybe This Is How It Is\n"
        self.output = self.output + "A book of questions and answers\n\n"
        self.output = self.output + "Over the past few years I have asked everyone I have ever met a few questions.\n\n"

        # the book
        self.make_databases()
        self.make_stuff()

        # make the file
        write_file.write(self.output)
        return "book.txt created"
      
      
    
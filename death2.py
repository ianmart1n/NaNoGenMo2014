import random
import re
import os
import string
import urllib2
 
class Twee():
  
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
        directory_name = os.getcwd() + "/words"
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

    def pick_relatives(self):
        self.affected["name"] = random.choice(self.sourceDb["name"])
        self.affected["relation"] = random.choice(self.sourceDb["relative"])
        if self.affected["relation"] in self.sourceDb["relative"]:
            self.sourceDb["relative"].remove(self.affected["relation"])
        
        gameRelatives = random.sample(self.sourceDb['relative'], 10)
        for i in xrange(len(gameRelatives)):
            name = random.choice(self.sourceDb['name'])
            location = random.choice(self.locations)
            self.relatives.append([ gameRelatives[i], name, location ])

    def pick_locations(self):
        gameLocations = random.sample(self.sourceDb['location'], 10)
        for i in xrange(len(gameLocations)):
            self.locations.append(gameLocations[i])

    def setup_premise(self):
        self.event = random.choice(self.sourceDb["event"])
        if self.event == "funeral":
            self.concept = "Death"
        elif self.event == "wedding":
            self.concept = "Love"
        else:
            self.concept = "Life"
        
        self.town = random.choice(self.sourceDb["town"])

        self.pick_locations()
        self.pick_relatives()

    def make_intro(self):
        # first passage
        adj1 = random.choice(self.sourceDb["adj"])
        adj2 = random.choice(self.sourceDb["adj"])
        firstSen = self.replace_words("You arrive in "+self.town+" on a "+adj1+", "+adj2+" day.\n\n")
        secondSen = self.replace_words("You've been away for *time*. Ever since the *incident*, things have been *adj*. But now you are back.\n\n")
        thirdSen = self.replace_words("It is a "+adj1+", "+adj2+" day, and there's going to be a [["+self.event+"]].\n\n")

        self.output = self.output + "::Start\n"
        self.output = self.output + firstSen + secondSen + thirdSen

        #second passage
        nextstep = random.choice(self.sourceDb["nextstep"])
        firstSen = self.replace_words("Your "+self.affected["relation"]+" "+self.affected["name"]+" always said that "+self.concept+" is *metaphor*. ")
        secondSen = self.replace_words("You think "+self.concept+" is a *noun*. ")
        thirdSen = self.replace_words("Maybe "+self.concept+" is a *noun*.\n\n")
        fourthSen = self.replace_words("Maybe [["+nextstep+"]].\n\n")

        self.output = self.output + "::"+self.event+"\n"
        self.output = self.output + firstSen + secondSen + thirdSen + fourthSen

        firstSen = self.replace_words("You step off the bus at "+self.town+"'s bus station. It's raining. The clouds are *adj* ")
        secondSen = self.replace_words("and *adj*.\n\n")
        thirdSen = self.replace_words("You should find your family. "+self.affected["name"]+"'s "+self.event+" is on Sunday and you promised you would get everyone to go.\n\n")
        fourthSen = self.replace_words("The first place you think to look is the [["+self.locations[0]+"]].")

        self.output = self.output + "::"+nextstep+"\n"
        self.output = self.output + firstSen + secondSen + thirdSen + fourthSen + "\n\n"

    def make_locations(self):
        for i in xrange(len(self.locations)):
            firstSen = "You arrive at the " + self.locations[i] + ". "
            secondSen = self.replace_words("It is just as you remember: *adj*. ")
            thirdSen = self.replace_words("Someone has discarded a *noun* *area*. ")
            thirdSen = thirdSen + self.replace_words("You see a *adj* *noun*. ")
            thirdSen = thirdSen + self.replace_words("The nature here seems *adj*. ")
            thirdSen = thirdSen + self.replace_words("It sounds like a *noun* is *verbing* somewhere. ")
            thirdSen = thirdSen + self.replace_words("\n\nThe *weather* *weatherDesc*. \n\n")
            fourthSen = ""
            
            for j in xrange(len(self.relatives)):
                if self.relatives[j][2] == self.locations[i]:
                    fourthSen = fourthSen + "You see your " + self.relatives[j][0] + " [[" + self.relatives[j][1] + "|"+self.relatives[j][0]+self.relatives[j][1]+"]] here. "
            if fourthSen == "":
                fourthSen = "There is no one here that you know. You think about moving on to the "
                try:
                    fourthSen = fourthSen + "[[" + self.locations[i+1]+"]]."
                except: 
                    fourthSen = fourthSen + "[[" + self.locations[0]+"]]."

            self.output = self.output + "::"+self.locations[i]+"\n"
            self.output = self.output + firstSen + secondSen + thirdSen + fourthSen + "\n\n"

    def make_relatives(self):
        for i in xrange(len(self.relatives)):
            passage1 = self.relatives[i][0]+self.relatives[i][1]+"story"
            passage2 = self.relatives[i][0]+self.relatives[i][1]+self.event
            passage3 = self.relatives[i][0]+self.relatives[i][1]+self.concept
            passage4 = self.relatives[i][0]+self.relatives[i][1]+"advice"

            firstSen = self.replace_words("Your " + self.relatives[i][0] + ", " + self.relatives[i][1] + ", is *verbing* here. ")
            secondSen = self.replace_words("They still have their *adj* *attribute*. ")
            thirdSen = self.replace_words("You remember that around the time of the *incident* they seemed like they were *adj*. ")
            thirdSen = thirdSen + self.replace_words("They seem more *adj* right now. \n\n")

            firstAct = "You wonder if they have a story about [["+self.affected["name"]+"|"+passage1+"]] to share.\n"
            secondAct = "You should ask if they are going to the [[" + self.event + "|"+passage2+"]].\n"
            thirdAct = "Perhaps ask them what they think [["+ self.concept+"|"+passage3+"]] is.\n"
            fourthAct = self.relatives[i][1] + " might know [[where to look|"+passage4+"]] for the rest of your family.\n"
            fifthAct = "\n\nYou could leave them [[alone|"+self.relatives[i][2]+"]] for now."
            
            self.output = self.output + "::"+self.relatives[i][0]+self.relatives[i][1]+"\n"
            self.output = self.output + firstSen + secondSen + thirdSen + firstAct + secondAct + thirdAct + fourthAct + fifthAct + "\n\n"

            self.output = self.output + "::"+passage1+"\n"
            self.output = self.output + self.replace_words("\""+self.affected["name"]+" always seemed *adj* to me. Before the *incident* I remember I saw them *verbing* by the *location*. ")
            self.output = self.output + self.replace_words("I asked "+self.affected["name"]+" what they were doing. They looked at me like I was *adj*, and *verbed*.\"\n\n")
            self.output = self.output + self.replace_words("\"Remember their *adj* *attribute*?\"\n\n <<back>>\n\n")
            self.output = self.output + "::"+passage2+"\n"
            answer = random.choice([1,2,3])
            if answer == 1:
                reply = "*affirmative*. "+self.affected["name"]+" would want me to. I feel *adj*."
            elif answer == 2:
                reply = "*maybe*. "+self.affected["name"]+" makes me feel *adj*. After what happened at the *incident*, I'd have to think about it. "
            else:
                reply = "*negative*. I can't go to an event for "+self.affected["name"]+". Things are kind of *adj* right now."
            self.output = self.output + "\"" + self.replace_words(reply) + "\"\n\n<<back>>\n\n"
            self.output = self.output + "::"+passage3+"\n"
            self.output = self.output + self.replace_words("\"I think "+self.concept+" is a *noun*.\"\n\n<<back>>\n\n")
            self.output = self.output + "::"+passage4+"\n"
            checkLoc = self.relatives[i][2]
            while checkLoc == self.relatives[i][2]:
                checkLoc = random.choice(self.locations)
            self.output = self.output + "\"You could trying checking out the [["+checkLoc+"]],\" says "+self.relatives[i][1]+". \"That's just a guess.\"\n\n<<back>>\n\n"

    def generate_twee(self):
        # open file
        write_file = open("game.tw", "w+")

        # set up
        self.make_databases()
        self.setup_premise()

        # intro
        self.make_intro()

        # other passages
        self.make_locations()
        self.make_relatives()

        # make the file
        write_file.write(self.output)
        return "game.tw created"
      
      
    
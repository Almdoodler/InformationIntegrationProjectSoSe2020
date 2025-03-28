
class Movie:

    def __init__(self, title, year, imdbID):
    		self.title, self.year, self.imdbID = title, year, imdbID

    def getTitle(self):
        return self.title
    
    def getYear(self):
        return self.year

    def getImbID(self):
        return self.imdbID
    
    def setRuntime(self, runTime):
        self.runtTime = runTime
    
    def getRuntime(self):
        return self.runtTime
    
    def setProduction(self, production):
        self.production = production

    def getProduction(self):
        return self.production
    
    def getActors(self):
        return self.actors

    def setActors(self, actors):
        self.actors = actors
    
    def string(self):
        return "Title: " + str(self.title) + "\nYear:" + str(self.year) + "\nimdbID: " + str(self.imdbID) + "\nruntime: " + str(self.runtTime) + "\nProduction: " + str(', '.join(self.production)) + "\nactors: " + str(', '.join(self.actors))
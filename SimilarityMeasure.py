import math
from difflib import SequenceMatcher
import re, math
from collections import Counter

class SimilarityMeasure:

    def __init__(self):
        self.WORD = re.compile(r'\w+')
    
    
    
    def simJaro(self, s1, s2):
        
        o = 0 
        t = 0
        if s1 == s2: 
            return 1
        elif s1 == 0 or s2 == 0 or s1 == "N/a" or s2 == "N/A":
            return 0.5
        else:
            for i in range(0, len(s1)):
                for j in range(0, len(s2)):
                    if s1[i] == s2[j]:
                        if abs(i-j) <= 0.5 * max(len(s1), len(s2)) - 1:
                            print("i ", i, ",j ", j,",abs ", abs(i-j), ",<= ", 0.5 * (max(len(s1), len(s2)) - 1))
                            o = o + 1 
                            if i is not j:
                                t = t + 1
        if o == 0:
            return 0
        print("o ", o)
        print("t ", t) 
        return 1/3 * (  (o/len(s1)) + (o/len(s2)) + ((o-0.5*t)/o)   )

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def get_jaccard_sim(self, s1, s2): 
        a = set(s1.split()) 
        b = set(s2.split())
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))
    


    def get_cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
            
        return Counter(self.WORD.findall(text))

    def get_similarity(self, a, b):
        a = self.text_to_vector(a.strip().lower())
        b = self.text_to_vector(b.strip().lower())

        return self.get_cosine(a, b)
    


            
        

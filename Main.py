"""

@author: Psp98

Application program that provides 3 features:
    1) Next Word Prediction
    2) Word Completion
    3) Word Correction
"""

import tkinter as tk
import operator

# ----------------------------------------------------------------------------------------

"""
Class to decribe the Trie node
It includes:
    1) char stored in this node
    2) children of this node
    3) boolean to check if word is finished or not
"""
class TrieNode(object):
    
    def __init__(self, char):
        
        self.char = char
        self.children = []
        self.wordFinished = False;
        
        
# ----------------------------------------------------------------------------------------        
        
"""
An utility Class that includes methods to implement the above 3 features.
"""
class Application(object):
        
        """
        Method to get String array from the Input file
        return: String array
        """
        def getStringArrayFromCorpus(self, fileName):
            
            corpus = self.getCorpus(fileName)
            corpusArray = corpus.split(' ')
            
            return corpusArray
        
        """
        Method to read the file and convert it to string
        return: string
        """
        def getCorpus(self, fileName):
            
            with open(fileName, 'r') as myfile:
                data = myfile.read().replace('\n', ' ')
            
            return data
        
        """
        Method to make an Unigram Map from the Corpus
        """
        def makeUnigramMap(self):
            
            for string in self.corpusArray:
                self.unigramMap[string] = self.unigramMap.get(string, 0) + 1
                
                
        """
        Method to make a Bigram Map from the Corpus
        """
        def makeBigramMap(self):
            
            size = len(self.corpusArray)
            
            for i in range(size - 1):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1]
                self.bigramMap[string] = self.bigramMap.get(string, 0) + 1
            
        
        """
        Method to make a Trigram Map from the Corpus
        """
        def makeTrigramMap(self):
            
            size = len(self.corpusArray)
            
            for i in range(size - 2):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1] + ' ' + self.corpusArray[i + 2]
                self.trigramMap[string] = self.trigramMap.get(string, 0) + 1
            
            
        """
        Method to make a Ngram Map from the Corpus
        """
        def makeNgramMap(self):
            
            size = len(self.corpusArray)
            
            for i in range(size - 3):
                string = self.corpusArray[i] + ' ' + self.corpusArray[i + 1] + ' ' + self.corpusArray[i + 2] + ' ' + self.corpusArray[i + 3]
                self.ngramMap[string] = self.ngramMap.get(string, 0) + 1
            
            
        """
        Method to add all words after a selected word in its set.
        It creates a next Word List Map.
        Key: word
        Value: A set consisting of all words after this key
        """
        def makeNextWordsListMap(self):
            
            for string in self.corpusArray:
                self.nextWordsListMap[string] = set()
                
            size = len(self.corpusArray)
            
            for i in range(size - 1):
                self.nextWordsListMap[self.corpusArray[i]].add(self.corpusArray[i + 1])
        
            
        """
        Main method to predict next Words from given input
        Output: Max of 3 words that are predicted as per logic
        """
        def getNextWordsPrediction(self, screenText):
            
            screenTextArray = screenText.split()
            size = len(screenTextArray)
            
            probabilityMap = dict()
            
            # Bigram Case
            if(size == 1):
                denString = screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.unigramMap.get(denString))
                
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString
                    
                    if(self.bigramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.bigramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    
                    probabilityMap[numString] = value
            
            # Trigram Case
            elif(size == 2):
                denString = screenTextArray[size - 2] + ' ' + screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.bigramMap.get(denString))
                
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString
                    
                    if(self.trigramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.trigramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    probabilityMap[numString] = value
            
            # Ngram Case
            else:
                denString = screenTextArray[size - 3] + ' ' + screenTextArray[size - 2] + ' ' + screenTextArray[size - 1]
                lastWord = screenTextArray[size - 1]
                den = float(self.trigramMap.get(denString))
                
                for numString in self.nextWordsListMap[lastWord]:
                    search = denString + ' ' + numString
                    
                    if(self.ngramMap.get(search) == None):
                        num = 0
                    else:
                        num = float(self.ngramMap.get(search))
                    
                    value = self.calculateProbability(num, den)
                    probabilityMap[numString] = value
            
            # get max of 3 words only to show on screen
            size = min(3, len(probabilityMap))
            
            # get top 3 words
            sortedProbabilityMap = dict(sorted(probabilityMap.items(), key = operator.itemgetter(1), reverse = True)[:size])
            
            # print these words
            for key in sortedProbabilityMap.keys():
                print(key, end='     ')
                
            print()
            print('-------------------------------------------------------------------')
            
        """
        Utility Method to calculate probability
        return probability
        """
        def calculateProbability(self, num, den):
            return float(float(num) / float(den))
        
        """
        Method to initialize Trie with all the words in the Input file
        """
        def addWordsToTrie(self):
            
            size = len(self.corpusArray)
            
            for i in range(size):
                
                word = str(self.corpusArray[i])
                node = self.root
            
                for char in word:
                    
                    charFound = False
                    
                    for child in node.children:
                        
                        if char == child.char:
                            node = child
                            charFound = True
                            break
                        
                    if not charFound:
                        newNode = TrieNode(char)
                        node.children.append(newNode)
                        node = newNode
                    
                node.wordFinished = True
            
        """
        Method to get last word entered by user on screen
        """
        def getLastWordFromSentence(self, screenText):
            
            screenTextArray = screenText.split()
            size = len(screenTextArray)
            
            return screenTextArray[size - 1]
        
        """
        Method to get all words after the given prefix in Trie
        Computes "wordList" array
        """
        def getAllWordsAfterPrefix(self, node, prefix):
        
            self.getLargestCommonPrefix(node, prefix)
        
        """
        Method to get Largest Common Prefix from the last word 
        entered by user in Trie and call DFS method to get compute "wordList" array
        """
        def getLargestCommonPrefix(self, root, word):
            
            node = root
            prefix = ""
            
            for char in word:
                
                charFound = False
                
                for child in node.children:
                    
                    if char == child.char:
                        node = child
                        charFound = True
                        prefix = prefix + child.char
                        break
                    
                if not charFound:
                    return self.DFSOnTrie(node, prefix)
                
            return self.DFSOnTrie(node, prefix)
        
        """
        Recursive Method to compute DFS on Trie from given 
        Prefix Node
        All words encountered are added to "wordList" array
        """
        def DFSOnTrie(self, node, prefixNow):
            
            if node.wordFinished:
                self.wordList.append(prefixNow)
            
            for child in node.children:
                self.DFSOnTrie(child, prefixNow + child.char)
            
            
        """
        Get max of Top 3 words as per priority logic
        from the "wordList" array
        """
        def getTopFrequentWords(self):
            
            frequencyMap = dict()
            
            for word in self.wordList:
                
                frequencyMap[word] = self.unigramMap.get(word)
                
            size = min(3, len(frequencyMap))
            
            sortedFrequencyMap = dict(sorted(frequencyMap.items(), key = operator.itemgetter(1), reverse = True)[:size])
            
            for key in sortedFrequencyMap.keys():
                print(key, end='     ')
            
            print()
            print('-------------------------------------------------------------------')
        
        """
        Method to clear wordList once function is done implementing
        """
        def clearWordList(self):
            
            self.wordList = []
        
        """
        Method to initialize various Map, Array and call require methods
        """
        def __init__(self):
            
            self.unigramMap = dict()
            self.bigramMap = dict()
            self.trigramMap = dict()
            self.ngramMap = dict()
            self.nextWordsListMap = dict()
            
            self.root = TrieNode('*')
            self.corpusArray = self.getStringArrayFromCorpus('Big.txt')
            
            self.makeUnigramMap()
            self.makeBigramMap()
            self.makeTrigramMap()
            self.makeNgramMap()
            self.makeNextWordsListMap()
            self.addWordsToTrie()
            
            # To store results everytime a button is pressed.
            self.wordList = []


# -----------------------------------------------------------------------------------------

"""
API Class that builds the simple UI and calls respective function as required
"""
class Main:
    
    """
    Method that is called when "Next" button is pressed
    """
    def nextFunction(self, textBox, nwp):
        
        print('Top words predicted are: ')
        nwp.getNextWordsPrediction(textBox.get("1.0", 'end-1c'))
        
    """
    Method that is called when "Complete" button is pressed
    """
    def completionFunction(self, textBox, nwp):
        
        print('Any of the following words you want: ')
        prefix = nwp.getLastWordFromSentence(textBox.get("1.0", 'end-1c'))
        nwp.getAllWordsAfterPrefix(nwp.root, prefix)
        nwp.getTopFrequentWords()
        nwp.clearWordList()
        
    """
    Method that is called when "Correct" button is pressed
    """
    def correctionFunction(self, textBox, nwp):
        
        print('Did you mean? ')
        lastWord = nwp.getLastWordFromSentence(textBox.get("1.0", 'end-1c'))
        nwp.getAllWordsAfterPrefix(nwp.root, lastWord)
        nwp.getTopFrequentWords()
        nwp.clearWordList()
        
    """
    Init method to generate a simple UI
    """
    def __init__(self):
        
        nwp = Application()
        
        main = tk.Tk()
        frame = tk.Frame(main, width = 250, height = 150)
        frame.pack()
        
        textBox = tk.Text(frame)
        textBox.place(x = 20, y = 5, height = 30, width = 200)
        
        nextButton = tk.Button(main, text = 'Next', command = lambda: self.nextFunction(textBox, nwp))
        nextButton.place(x = 20, y = 50, height = 30, width = 100)
        
        completeButton = tk.Button(main, text = 'Complete', command = lambda: self.completionFunction(textBox, nwp))
        completeButton.place(x = 130, y = 50, height = 30, width = 100)
        
        correctButton = tk.Button(main, text = 'Correct', command = lambda: self.correctionFunction(textBox, nwp))
        correctButton.place(x = 70, y = 100, height = 30, width = 100)
        
        main.mainloop()


# -----------------------------------------------------------------------------------------     

"""
Driver class to call the API class
"""
class Driver:
    
    Main()
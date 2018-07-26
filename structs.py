#Simple data structures that are used to create parties and data objects

#Created Following Tutorials from Cracking The Coding Interview Version 6

class node(object):
    def __init__(self,d):
        self.next = None
        self.data = d

class queue(object):
    def __init__(self):
        self.head = None
        self.tail = None
        #self.len = 0

    def isEmpty(self):
        return self.head==None

    def peek(self):
        if(self.head!=None):
            return self.head.data
        return None

    def add(self,data):
        print(data)
        tempNode = node(data)
        if(self.head==None):
            self.head = tempNode
        elif(self.tail!=None):
            self.tail.next = tempNode
        self.tail = tempNode
        print("tail",self.tail.data)
        print(self.toArray())
        #self.len+=1

    def remove(self,index=0):
        data = self.head.data
        if(index==0):
            if(self.head!=None):
                self.head=self.head.next
            if(self.head==None):self.tail = None
        elif(index==self.len()-1):
            currentNode = self.head
            for i in range(index - 1):
                currentNode = currentNode.next
            self.tail = currentNode
            currentNode.next = currentNode.next.next
        else:
            currentNode = self.head
            for i in range(index-1):
                currentNode = currentNode.next
            currentNode.next = currentNode.next.next
        #print(self.toArray(),self.head.data,self.tail.data)

    def replace(self,index,value):
        currentNode = self.head
        for i in range(index):
            currentNode = currentNode.next
        currentNode.data = value

    def get(self,index):
        return self.toArray()[index]

    def printQueue(self):
        currentNode = self.head
        while(currentNode!=None):
            print(currentNode.data)
            currentNode = currentNode.next

    def toArray(self):
        array = []
        currentNode = self.head
        while (currentNode != None):
            array.append(currentNode.data)
            currentNode = currentNode.next
        return array

    def len(self):
        #print(self.toArray())
        return len(self.toArray())

class party(queue):
    pass
    def add(self,data):
        #print(self.toArray())
        #print(data)
        old = None
        if(len(self.toArray())<6):
            #print("z")
            tempNode = node(data)
            #print("temp",tempNode.data)
            #print("self",self.head)
            if(self.head==None):
                #print("a")
                self.head = tempNode
                #print("tail",self.tail)
            elif(self.tail!=None):
                #print("b")
                self.tail.next = tempNode
            self.tail = tempNode
        #print(self.toArray())
        #print("")

class data(object):
    pass
            

# -*- coding: utf-8 -*-
"""
Data Structure Implementation Strategy for Bank of Singapore's Queuing System

@author: Zhang Yuanfei, Josie, Jayce, Katherine, Kevin
"""

# Object for customer information.
class CusNode:
    def __init__(self, biz_type, queue_no, email = None):
        self.biz_type = biz_type
        self.queue_no = queue_no
        self.email = email

# Object for counter information, indicating the current serving number.
class Counter:
    def __init__(self, counter_no, biz_type):
        self.counter_no = counter_no
        self.biz_type = biz_type
        self.cur_serve = None
    
    def callNextClient(self, biz_queue, url_biz_name):
        try:
            next_client = biz_queue.queue_list[0]
            if len(biz_queue.queue_list) > 1:
                biz_queue.queue_list = biz_queue.queue_list[1:]
            else:
                biz_queue.queue_list = []
            self.cur_serve = next_client, biz_queue.biz_type
            call_no = [f'[{url_biz_name.split(" ")[0]}] ' + str(self.counter_no), next_client.queue_no]
            biz_queue.call_list.append(call_no)
            if len(biz_queue.call_list) > 3:
                biz_queue.call_list = biz_queue.call_list[-3:]
            return next_client
        except:
            return -1

    def holdNextClient(self, biz_queue):
        try:
            next_client = biz_queue.queue_list[0]
            biz_queue.queue_list = biz_queue.queue_list[1:]
            if len(biz_queue.missed_list) > 5:
                biz_queue.missed_list = biz_queue.missed_list[1:]
            biz_queue.missed_list.append(next_client)
            return next_client
        except:
            return -1
        
        return 1
    
    def reschedule(self, queue_no, biz_queue):
        newCus = CusNode(biz_queue.biz_type, queue_no)
        if len(biz_queue.queue_list) <= 3:
            biz_queue.queue_list.append(newCus)
        else:
            biz_queue.queue_list.insert(3,newCus)
        biz_queue.missed_list = [x for x in biz_queue.missed_list if int(x.queue_no) != int(queue_no)]
        return newCus
# Object for business type and its corresponding queue_list, counter_list, missed_list.
class BizQueue:
    def __init__(self, biz_type):
        self.biz_type = biz_type
        self.status = True
        self.queue_list = []
        self.counter_list = []
        self.missed_list = []
        self.call_list = []
        self.queue_count = 0
    ''' 
        def getLastNode(self):
            try:
                return [x for x in self.queue_list if x.biz_type == self.biz_type][-1].queue_no
            except:
                return 0
    '''
    def addCounter(self, counter_id):
        new_counter = Counter(counter_id, self.biz_type)
        self.counter_list.append(new_counter)
        return 0
    
    def removeCounter(self, counter_id):
        remove_counter = [x for x in self.counter_list if int(x.counter_no) == int(counter_id)][0]
        self.counter_list.remove(remove_counter)
        return 0
    
    def addNode(self, newNode):
        if self.status == True:
            self.queue_list.append(newNode)
            self.queue_count += 1
        else:
            return 'Queue paused due to excessive queue length.'
    
    def stop(self):
        self.status = False
        return 'Queue is stopped.'

    def reInitiate(self):
        self.status = True
        return 'Queue is reinitiated.'
    
    def reset(self):
        self.queue_list = []
        self.status = True
        self.queue_count = 0
        for x in self.counter_list:
            x.cur_serve = None
        self.missed_list = []
        self.call_list = []
        self.queue_count = 0
        return 'Queue is reset.'
    
    def viewQueue(self):
        queue_no_list = []
        for i in self.queue_list:
            queue_no_list.append(str(i.queue_no))
        queue_list = ', '.join(queue_no_list)
        return queue_list
        
# Object for branch level.
class BankMap:
    def __init__(self, branch_no):
        self.branch_no = branch_no
        self.biz_list = []

    def getQueueNo(self, biz_type, email):
        try:
            queue_list = [x for x in self.biz_list if x.biz_type == biz_type][0]
        except:
            return 'Invalid biz type.'
        queue_no = queue_list.getLastNode(biz_type)+1
        newNode = CusNode(biz_type, queue_no, email)
        queue_list.addNode(newNode)
    
    def addList(self, newList):
        self.biz_list.append(newList)

# Test the methods designed.
if __name__ == '__main__':
    c1 = CusNode('A',1,'1@')
    c2 = CusNode('B',1,'2@')
    c3 = CusNode('A',2,'3@')
    c4 = CusNode('A',3,'4@')
    c5 = CusNode('A',4,'5@')
    c6 = CusNode('A',5,'6@')
    c7 = CusNode('A',6,'7@')

    b1 = BizQueue('A')
    b1.addNode(c1)
    b1.addNode(c3)
    b1.addCounter(1)
    b1.addCounter(2)
    b2 = BizQueue('B')
    b2.addNode(c2)
    m1 = BankMap('001')
    m1.addList(b1)
    m1.addList(b2)
    print("queue_no of b1 biz_type")
    print(b1.queue_list[-1].queue_no)
    print(m1.biz_list[0].counter_list)
    print(m1.biz_list[0].counter_list[0].counter_no)
    b1.removeCounter(1)
    print(m1.biz_list[0].counter_list[0].counter_no)

    # print("first element in reschedule list after calling for the next client")
    # print(m1.missed_list[0].queue_no)
    print("queue_no of b1 biz_type after calling for the first client with b1 biz_type")
    # print(b1.queue_list[0].queue_no)

    print("last element of b1 biz_type queue_list")
    print(b1.getLastNode())
    
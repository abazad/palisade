'''
Created on 20.03.2013

@author: bova
'''

import threading
import logging
from  exceptions import Exception
from itertools import ifilter, islice

download_state = {'new': 'NEW',
                  'new1': 'NEW1',
                  'rejected': 'REJECTED',
                  'accepted': 'ACCEPTED',
                  'active': 'ACTIVE',
                  'paused': 'PAUSED',
                  'completed': 'COMPLETED',
                  'error': 'ERROR'}
CLOSED = 1
FINISHED = 2
ERROR = 0
PAUSED = 3
STARTED = 4



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s')

class EmptyQueueError(Exception):
    pass

class Task(object):
    def __init__(self, task):
        super(Task, self).__init__()
        self.id = task.id
        self.url = task.url
        self.size = task.size
        self.state = task.state
        self.created_on = task.created_on
        self.email = task.email
        self.size_completed = task.size_completed
        self.worker = None
    
    def __str__(self, *args, **kwargs):
        return str(self.url)

class Downloads(object):
    '''The dictionary off all downloads in application
    
    Variables:
        self.all is dictionary with format {'task_id': Task(),...)
    
    '''
    def __init__(self):
        super(Downloads, self).__init__()
        self.all = {}
#        self.new = []
#        self.active = {}
#        self.completed = []
        self.lock = threading.Lock()
    
    def log(self):
        logging.debug('%s' % self.all)
        
    
    def update_task_attr(self, task_id, attr, value):
        with self.lock:
            task = self.all[task_id]
            setattr(task, attr, value)
    
    def put(self, task):
        with self.lock:
            self.all[task.id] = Task(task)
            logging.debug('%s' % task)
        self.log()
    
    def get_new(self):
        '''Get only one task, whenever many returned        
        '''
        with self.lock:
            try:
                new_task = [task for task_id,task in ifilter(lambda x: x[1].state==download_state['new'], self.all.iteritems())]
                task = new_task[0]
            except IndexError:
                logging.debug('There are no new tasks in self.all')
                raise EmptyQueueError
            else:
                self.all[task.id].state = download_state['new1']
        return task
    
    def get_url(self, thread_name):        
        with self.lock:
            try:                
                new_tasks = [task for task_id,task in ifilter(lambda x: x[1].state==download_state['accepted'], self.all.iteritems())]
                task = new_tasks[0]                
            except IndexError:
                logging.debug('There are no accepted tasks in self.all')
                raise EmptyQueueError
            else:
                self.all[task.id].state = download_state['active'] 
        self.log()
        return task
    
    def get_completed(self):
        '''Function search completed tasks, and return one at a call.
        Then delete that task from self.all dictionary        
        '''
        with self.lock:
            try:                
                completed_tasks = [task for task_id, task in 
                                   ifilter(lambda x: x[1].state==download_state['completed'], self.all.iteritems())]                    
                task = completed_tasks[0]
                del self.all[task.id]
            except IndexError:
                logging.debug('There are no completed task')
                raise EmptyQueueError
            return task
                
    
    def update(self, task_id, status):
        if status == FINISHED:
            with self.lock:
                self.completed.append(self.active[task_id])
                del self.active[task_id]
        elif status == CLOSED:
            with self.lock:
                del self.completed[task_id]
        self.log()
        

def worker(downloads, l):  
    name = threading.currentThread().getName()  
    d = downloads.get_url(name)
#    d = downloads.get_url(name)
    logging.debug('Task URL before: %s' % d.url)
    d.url = 'new value'
    logging.debug('Task URL before: %s' % d.url)
    downloads.update(name,FINISHED)
    

if __name__ == '__main__':
    downloads = Downloads()
    downloads.put('ya.ru')
    l = threading.Lock()
    t = threading.Thread(target=worker, args=(downloads, l))
    t.start()
    t.join()
            
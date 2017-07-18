from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError

class Project(models.Model):

    name = models.CharField(max_length=100,default='')

    def __str__(self): 
        return self.name

class Note(models.Model):

    parent = models.ForeignKey('self', blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True)

    title = models.CharField(max_length=100)
    content = models.TextField(max_length=100000)

    pub_date = models.DateTimeField('date published')    
    #last_modified = models.DateTimeField('last modified', null=True)
    #due_date = models.DateTimeField('due date', null=True)

    #complete = models.BooleanField(default=False)    

    def __str__(self):
        return self.title

class ToDoTask(models.Model):

    parentTask = models.ForeignKey('self',blank=True,null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,blank=True,null=True)

    title = models.CharField(max_length=100,null=True)

    due_date = models.DateTimeField('due date', null=True)
    complete = models.BooleanField(default=False)    

    def __str__(self):
        if( self.project == None ) :
            return "{0} ({1})".format(self.title,self.parentTask.title)
        else : 
            return "{0} ({1})".format(self.title,self.project.name)

    def TaskKeyValidation( self ) : 

        if( self.parentTask == None and self.project == None ):
            raise ValidationError('Task ({0}) has no primary keys!'.format(self.title))
            return False
        elif( self.parentTask != None and self.project != None ):
            raise ValidationError('Task ({0}) has two primary keys!'.format(self.title))
            return False
        else : 
            return True


    def save( self , *args, **kwargs ) : 
        if not self.TaskKeyValidation() : 
            return 
        else :
            super( ToDoTask , self ).save( *args , **kwargs )


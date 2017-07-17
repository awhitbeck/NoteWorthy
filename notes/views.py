from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone
from django.http import Http404
from django.shortcuts import redirect
from django import forms

import markdown

from .models import *

######################################
# Formatting helper functions
######################################

def formatQuickTip( tipName , tipContent ):

	result=""
	result+="<br>"
	result+="<div id=\"ref-{0}\" class=\"quicktip\">".format(tipName)
	result+="<h4> Useful {0} tip:</h4>".format(tipName)
	result+=tipContent
	result+="</div>"
	result+="<br>"

	return result


#def parseFormatSyntax():


######################################
# Task helper functions
######################################

def FormatTaskTree( taskInput , showAll = False ) : 
	"""
	Given a list of tasks or a project, this function will 
	traverse all of the subtasks and return a string which 
	formats the task tree as an HTML unordered list.

	taskInput can be either an arrary of tasks whose project
	foreign key point to the same project, or it can be
	an instance of a project and the list of tasks will be
	retrieved.  
	""" 

	# Note for this function to be recursive, it must be able
	# to handle a list of task as input.  The ability to pass
	# the parent project initially is just a cute add-on
	if isinstance(taskInput,Project) :
		taskArray = taskInput.todotask_set.all()
	else : 
		taskArray = taskInput

	if taskArray == None : 
		return ""

	retString = "<ul style='list-style-type: none;'>"
	for task in taskArray : 
		if task.complete and showAll : 
			retString += "<li><input type='checkbox' value='{0}' name='task_pk_{1}' checked/>{0}</li>".format(task.title,task.pk)
		elif not task.complete :  
			retString += "<li><input type='checkbox' value='{0}' name='task_pk_{1}'/>{0}</li>".format(task.title,task.pk)
		retString += FormatTaskTree( task.todotask_set.all() )
	retString += "</ul>"

	return retString

def ExpandTaskTree( taskInput ) :
	"""
	Given an input list of tasks or a parent project, 
	this function will tranverse the subtasks of all
	input task (or all task attached to a project).

	taskInput can be either an arrary of tasks whose project
	foreign key point to the same project, or it can be
	an instance of a project and the list of tasks will be
	retrieved.  
	"""

	if isinstance(taskInput,Project) : 
		taskArray = taskInput.todotask_set.all()
	else : 
		taskArray = taskInput

	if taskArray == None : 
		return []

	expandedTaskArray = []
	for task in taskArray :
		expandedTaskArray.extend( [task] )
		expandedTaskArray.extend( ExpandTaskTree( task.todotask_set.all() ) )

	return expandedTaskArray
######################################
######################################

######################################
# Task view functions
######################################
def UpdateToDo( request ):
	print request.POST
	project_pk = request.POST['project_pk'][0]
	project = Project.objects.filter(pk=project_pk)[0] 
	for task in ExpandTaskTree( project ) :
		print task
		print "task_pk_{0}".format(task.pk)
		if "task_pk_{0}".format(task.pk) in request.POST : 
			task.complete = True
			task.save()

	return redirect('/notes/{0}/note-list/'.format(project_pk))

def NewTask( request ):
	if request.method == 'POST' and'title' in request.POST : 

		form = TaskForm(request.POST)
		form.save()

		return redirect('/notes/new-task')

	else : 
		print TaskForm()
		return render( request , 'notes/new_task.html' , {"form":TaskForm()} )

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskForm(forms.ModelForm):
	class Meta: 
		model = ToDoTask
		fields = [ 'due_date' , 'title' , 'project' , 'parentTask' ]
		widgets = {'due_date':DateInput()}
######################################
######################################

######################################
###  Note Views
######################################
def NewNote( request , project_pk ): 

	print "test"
	print project_pk
	if( not 'noteName' in request.POST ) : 
		context = { "project_pk" : project_pk }
		return render( request , 'notes/new-note.html' , context )
	else : 
		postDict = request.POST
		#print postDict

		project = Project.objects.filter(pk=project_pk)[0]
		newNote = Note(title=postDict['noteName'],project=project,pub_date=timezone.now())
		newNote.save()

		notes = project.note_set.all()
		context = { "project_pk" : project_pk , "notes" : notes }
		return render( request , 'notes/note_list.html' , context )	
		#return redirect("note-list")

def ViewNote( request , noteIndex=1 ):

	#print noteIndex

	context = {}
	context['note'] = Note.objects.filter(pk=noteIndex)[0] 
	context['content'] = markdown.markdown( context['note'].content )#, safe_mode="escape" )

	return render( request , 'notes/view-note.html' , context )

def EditNote( request , noteIndex=1 ):

	#print noteIndex

	context = {}

	if( request.POST == {} ):
		context['note'] = Note.objects.filter(pk=noteIndex)[0] 
		context['content'] = markdown.markdown( context['note'].content )#, safe_mode="escape" )
	else : 
		postDict = request.POST
		#print postDict
		context['note'] = Note.objects.filter(pk=int(postDict['pk']))[0]
		context['note'].content = postDict['noteEdits']
		context['content'] = markdown.markdown( context['note'].content )#, safe_mode="escape" )
		context['note'].pub_date = timezone.now()
		context['note'].save()

	return render( request , 'notes/edit_note.html' , context )

def ListNotes( request , projectIndex ):
	project = Project.objects.filter(pk=projectIndex)[0]
	notes = project.note_set.all()
	#tasks = project.todotask_set.all()

	context = { # this is redundant since the project object is 
				# already being sent to the template.  It should
				# be removed. 
				"project_pk" : projectIndex , 
				"notes" : [] , 
				# this seems to be totally unnecessary!!! I should
				# remove it when I get a chance and see if it breaks
				# evertyhing 
				"tasks" : [] ,
				"taskTree" : FormatTaskTree( project ) ,
				"project" : project }

	#for task in tasks : 
	#	context["tasks"].append(task)

	for note in notes : 
		#print note
		context["notes"].append(note)

	return render( request , 'notes/note_list.html' , context )
######################################
######################################

######################################
# Project views
######################################
def NewProject( request ): 

	if( not 'projectName' in request.POST ) : 
		return render( request , 'notes/new-project.html' , {} )
	else : 
		postDict = request.POST
		#print postDict

		newProject = Project(name=postDict['projectName'])
		newProject.save()

		return redirect('/notes/project-list')

def ListProjects( request ) : 

	context = { "projects" : [] }

	projects = Project.objects.all()
	for project in projects : 
		# instead of doing this stupid tuple thing, the task helper
		# functions should be moved into models.py and ExpandTaskTree
		# and FormatTaskTree should become member functions of 
		# the Project model.
		context["projects"].append( ( project , FormatTaskTree( project ) ) )

	# print "context:",context
	return render( request , 'notes/project_list.html' , context )

class ListProjectView(ListView):

    model = Project
    template_name = 'project_list.html'

######################################
######################################

from django.conf.urls import include, url
import notes.views


urlpatterns = [
    #url(r'^project-list$', notes.views.ListProjectView.as_view(),name='project-list',),
    url(r'^project-list$', notes.views.ListProjects,name='project-list',),
    url(r'^(?P<projectIndex>[0-9]+)/note-list/$', notes.views.ListNotes,name='note-list',),
    url(r'^(?P<noteIndex>[0-9]+)/edit-note/$', notes.views.EditNote,name='edit-note',),
    url(r'^(?P<noteIndex>[0-9]+)/view-note/$', notes.views.ViewNote,name='view-note',),
    url(r'^new-project$', notes.views.NewProject,name='new-project',),
    url(r'^(?P<project_pk>[0-9]+)/new-note$', notes.views.NewNote,name='new-note',),
    url(r'^update-todo$', notes.views.UpdateToDo,name='update-todo',),
    url(r'^new-task$', notes.views.NewTask,name='new-task',),
]

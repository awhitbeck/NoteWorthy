import django
django.setup()
from notes.models import *
from django.utils import timezone

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-q", "--query",dest="query", 
                  help="query for searching note content")

parser.add_option("-s", "--showNotes",dest="show", default=False,action="store_true",
                  help="toggle whether or not matching notes are displayed")

(options, args) = parser.parse_args()


notes = Note.objects.filter(content__icontains=options.query)
for n in notes : 
    print n.title
    if options.show :
        print "------------------------"
        print n.content
        print "------------------------"


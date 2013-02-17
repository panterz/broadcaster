# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from voting.models import Area, Poll, Choice, Vote
from broadcaster import settings
from django.core import serializers
from django.db import connection
import json, logging, os

logger = logging.getLogger(__name__)

def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html', c)

def get_poll_details(request):
    logger.debug('get poll')
    choice = Choice.objects.select_related().all()
    logger.debug(choice)
    questions = []
    areas = []
    response_data = {}
    choices = []
    question = ''
    id=0
    i=0
    for c in choice:
        logger.debug("%s, %s, %s" % (c.choice_text, c.poll.question, question))
        
        if question != c.poll.question and question != '':
            questions.append({"id": id, "question": question, "choices": choices})
            choices = []
        choices.append({"id": c.id, "text":c.choice_text})
        question = c.poll.question
        id = c.poll.id
        i=i+1
        if i == len(choice):
            questions.append({"id": c.poll.id, "question": c.poll.question, "choices": choices})
        
    area = Area.objects.all()
    for a in area:
        areas.append({"id": a.id, "name": a.name})
    
    response_data['areas'] = areas
    response_data['questions'] = questions
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def submit_vote(request):
    try:
        area = int(request.REQUEST['area'])
        q1 = int(request.REQUEST['question1'])
        q2 = int(request.REQUEST['question2'])
    except Exception, exc:
        logger.debug(exc)
        return HttpResponse(json.dumps({"error": 1, "msg": "There is an error on submitting your vote!"}), mimetype="application/json")
    
    logger.debug("%s, %s , %s" % (area, q1, q2))
    c = Choice.objects.get(pk=q1)
    a = Area.objects.get(pk=area)
    v = Vote(choice=c, area=a)
    v.save()
    
    c = Choice.objects.get(pk=q2)
    v = Vote(choice=c, area=a)
    v.save()
    
    yes = len(Vote.objects.select_related().filter(choice__choice_text='Yes'))
    no = len(Vote.objects.select_related().filter(choice__choice_text='No'))
    
    cursor = connection.cursor()
    cursor.execute('select count(*) as n, b.choice_text from voting_vote a, voting_choice b, voting_poll c where a.choice_id=b.id and b.poll_id=c.id and c.id=2 group by b.choice_text')
    total_rows = cursor.fetchall()
    logger.debug(total_rows)
    
    results = {"question1": {"yes": yes, "no": no}, "question2" : total_rows}
    
    return HttpResponse(json.dumps({"error": 0, "msg": "Your vote has been saved!", "results": results}), mimetype="application/json")

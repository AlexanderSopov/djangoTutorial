from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """ Exclude any question in the future"""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question":question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResonseRedirect after sucessfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

    return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))

def create(request):
    #render a template
    print("got to create")
    return render(request, "polls/create.html",{})

def createPoll(request):
    #render a template

    try:
        qText=request.POST["question"]
        choices = request.POST.getlist("choice")
        print(choices)

    except(KeyError):
        print("something went wrong at createPoll")
        return render(request, "polls/create.html",{
            "error_message": "You didn't type a question or any choice in.",
        })


    else:
        if len(qText)>0:
            if (len(choices[0]) > 0 and len(choices[1]) > 0):
                q = Question.objects.create(question_text=qText, pub_date=timezone.now())
                q.save()
                for choice in choices:
                    if len(choice) > 0:
                        q.choice_set.create(choice_text=choice, votes=0)
                q.save()
            else:
                return render(request, "polls/create.html",{
                "error_message": "You didn't type ta least 2 choices in.",})
        else:
            return render(request, "polls/create.html",{
            "error_message": "You didn't type a question in.",})



        # Always return an HttpResonseRedirect after sucessfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

    return HttpResponseRedirect(reverse("polls:index"),)

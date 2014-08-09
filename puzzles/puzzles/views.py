from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import timezone

from puzzles.models import Puzzle, Submission

# Create your views here.
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            print 'Authenticated user', user
            login(request, user)
            return HttpResponseRedirect('/puzzles/')
        else:
            print 'Received bad login from user', username
            # somehow mark bad login details
            return HttpResponseRedirect('/login/')
    else:
        return render(request, 'puzzles/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/puzzles/')

def intro(request):
    template = loader.get_template('/intro.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def index(request):
    if request.user.is_authenticated():
        active_puzzles = request.user.get_profile().puzzles.filter(active=True)
    else:
        active_puzzles = []
    template = loader.get_template('puzzles/index.html')
    context = RequestContext(request, {
        'active_puzzles': active_puzzles,
    })
    return HttpResponse(template.render(context))

@login_required
def detail(request, puzzle_display_id):
    try:
        profile = request.user.get_profile()
        p = profile.puzzles.get(display_id=puzzle_display_id)
    except Puzzle.DoesNotExist:
        raise Http404
    if not p.active:
        raise Http404
    return render(request, 'puzzles/detail.html', {'puzzle': p})

@login_required
def submit(request, puzzle_display_id):
    profile = request.user.get_profile()
    print puzzle_display_id
    print profile.puzzles.all()
    p = profile.puzzles.get(display_id=puzzle_display_id)
    try:
        submission = request.POST['submission']
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the puzzle submission form.
        return render(request, 'puzzles/detail.html', {'puzzle': p})
    else:
        p.submission_set.create(answer=submission, timestamp=timezone.now())
        # if correct, activate the next puzzle and get rid of the submit form
        if submission == p.sol:
            if p.next_puzzle:
                p.next_puzzle.active = True
                p.next_puzzle.save()
            p.solved = True
            p.save()
            return HttpResponseRedirect(reverse('puzzles:detail',
                args=(p.display_id,)))
        # if incorrect, redirect to the submit form and display that was wrong
        else:
            p.save()
            # implement messages to report wrong submission
            return HttpResponseRedirect(reverse('puzzles:detail',
                args=(p.display_id,)))

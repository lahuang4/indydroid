from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Puzzle(models.Model):
    name = models.CharField(max_length=2000)
    display_id = models.IntegerField()
    active = models.BooleanField()
    solved = models.BooleanField()
    statement = models.CharField(max_length=2000)  # link for puzzle pdf
                                                   # consider a FileField?
    sol = models.CharField(max_length=2000)
    next_puzzle = models.ForeignKey('self', null=True, blank=True)

    team = models.CharField(max_length=2000, null=True, blank=True)

    search_fields = ['name', 'sol']

    def __unicode__(self):
        return self.name + ' | ' + self.team

class Submission(models.Model):
    puzzle = models.ForeignKey(Puzzle)
    answer = models.CharField(max_length=2000)
    timestamp = models.DateTimeField('time submitted')

    def __unicode__(self):
       return self.answer

    class Meta:
        get_latest_by = 'timestamp'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # optional, just for ease of querying. should match user.username
    name = models.CharField(max_length=2000, null=True, blank=True)

    # many-to-many to allow all team members to access the same puzzles
    puzzles = models.ManyToManyField(Puzzle, null=True, blank=True)
    team = models.CharField(max_length=2000, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

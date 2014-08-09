from django.contrib import admin
from puzzles.models import Puzzle, Submission, UserProfile

# Register your models here.
class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0

class PuzzleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                 {'fields': ['name', 'display_id', 'team']}),
        ('Puzzle information', {'fields': ['statement', 'sol', 'active',
            'solved']}),
        ('Unlocks puzzle',     {'fields': ['next_puzzle']}),
    ]
    inlines = [SubmissionInline]
    list_display = ('name', 'sol', 'team', 'active', 'solved', 'next_puzzle')

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'name', 'team']}),
        ('Puzzles', {'fields': ['puzzles']}),
    ]
    list_display = ('user',  'team')

admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

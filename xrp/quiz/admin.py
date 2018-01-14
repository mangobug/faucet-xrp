from django.contrib import admin

from xrp.quiz.models import Choice, Likert, LikertAnswer, MCQAnswer, MCQuestion, xrpEnded, Quiz, MCQuestionAttempt, LikertAttempt, xrpEndedAttempt


class ChoiceAdmin(admin.ModelAdmin):
    pass


class LikertAdmin(admin.ModelAdmin):
    pass


class LikertAnswerAdmin(admin.ModelAdmin):
    pass


class MCQAnswerAdmin(admin.ModelAdmin):
    pass


class MCQuestionAdmin(admin.ModelAdmin):
    pass


class xrpEndedAdmin(admin.ModelAdmin):
    pass


class QuizAdmin(admin.ModelAdmin):
    pass


class MCQuestionAttemptAdmin(admin.ModelAdmin):
    pass


class LikertAttemptAdmin(admin.ModelAdmin):
    pass


class xrpEndedAttemptAdmin(admin.ModelAdmin):
    pass


admin.site.register(MCQAnswer, MCQAnswerAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Likert, LikertAdmin)
admin.site.register(LikertAnswer, LikertAnswerAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(xrpEnded, xrpEndedAdmin)
admin.site.register(MCQuestionAttempt, MCQuestionAttemptAdmin)
admin.site.register(LikertAttempt, LikertAttemptAdmin)
admin.site.register(xrpEndedAttempt, xrpEndedAttemptAdmin)

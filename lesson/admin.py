from django.contrib import admin
from . import models as m

admin.site.register(m.Grammar)
admin.site.register(m.Reading)
admin.site.register(m.Speaking)
admin.site.register(m.Question)
admin.site.register(m.Answer)
admin.site.register(m.Listening)

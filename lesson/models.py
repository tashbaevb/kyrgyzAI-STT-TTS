from django.db import models


class Grammar(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img = models.ImageField(upload_to='img/')


class Listening(models.Model):
    text = models.TextField()
    answer = models.TextField(null=True)


class Reading(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def check_answers(self, answers):
        questions = self.questions.all()
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            if answers.get(str(question.id)):
                selected_answer_id = int(answers[str(question.id)])
                selected_answer = question.answers.filter(id=selected_answer_id).first()
                if selected_answer and selected_answer.is_correct:
                    correct_answers += 1

        return correct_answers, total_questions


class Question(models.Model):
    reading = models.ForeignKey(Reading, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)


class Speaking(models.Model):
    text = models.TextField(null=True)
    file = models.FileField(upload_to='lesson/speaking')
    subtitles = models.TextField(blank=True, null=True)



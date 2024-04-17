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
    questions_1 = models.CharField(max_length=100)
    answer_1 = models.CharField(max_length=100)
    answer_2 = models.CharField(max_length=100)
    answer_3_right = models.CharField(max_length=100)

    questions_2 = models.CharField(max_length=100)
    answer_2_1 = models.CharField(max_length=100)
    answer_2_2 = models.CharField(max_length=100)
    answer_2_3_right = models.CharField(max_length=100)

    questions_3 = models.CharField(max_length=100)
    answer_3_1 = models.CharField(max_length=100)
    answer_3_2 = models.CharField(max_length=100)
    answer_3_3_right = models.CharField(max_length=100)


class Speaking(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    answer = models.TextField()

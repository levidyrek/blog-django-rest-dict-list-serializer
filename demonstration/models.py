from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='posts')
    blog = models.ForeignKey(
        'Blog', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return '{} - {}'.format(self.blog, self.title)


class User(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.username, self.name)


class Comment(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(
        'BlogPost', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return '{} - {}'.format(self.post, self.comment)

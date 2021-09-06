from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Books(models.Model):
    book_name = models.CharField(max_length=200, null=True)
    author_name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    book_pages = models.BigIntegerField(null=True)
    # quantity = models.BigIntegerField(null=True)
    language = models.CharField(max_length=100, null=True)
    price = models.BigIntegerField(null=True)
    isbn_number = models.CharField(max_length=20)
    doi_number = models.CharField(max_length=100)
    accession_number = models.CharField(max_length=100, null=True)
    publisher_name = models.CharField(max_length=200)
    publisher_date = models.CharField(max_length=100, null=True)
    shelf_number = models.CharField(max_length=20, null=True)
    description = models.TextField(max_length=500, null=True)
    cover_photo = models.ImageField(upload_to='bookCoverPhotos', null=True, blank=True)

    def __str__(self):
        return str(self.book_name)


class IssueBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    issue_date = models.DateField(auto_now_add=True, null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    is_return = models.BooleanField(default=False)
    issue_status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.issue_date)


class wish_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    is_wished = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'book',)

    def __str__(self):
        return str(self.user)


class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_status = models.IntegerField(default=0)
    presentAddress = models.CharField(max_length=400, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=200, null=True)
    profilePic = models.ImageField(upload_to='profilePic', default='profile.png', null=True, blank=True)
    payment = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.user)

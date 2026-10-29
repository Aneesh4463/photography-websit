from django.db import models


class Review(models.Model):
    
    customer_name = models.CharField(max_length=100)
    place = models.CharField(max_length=150)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name


class Portfolio(models.Model):

    CATEGORY_CHOICES = [

        ('wedding', 'Wedding'),
        ('pre_wedding', 'Pre-Wedding / Save the Date'),
        ('candid', 'Candid'),
        ('maternity', 'Maternity'),
        ('kids_photography', 'Kids Photography'),
        ('destination_wedding', 'Destination Wedding'),
        ('model_shoot', 'Model Shoot'),
    ]

    title = models.CharField(max_length=150)

    category = models.CharField(max_length=30,choices=CATEGORY_CHOICES)

    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='portfolio/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return self.title


class FilmTeaser(models.Model):

    CATEGORY_CHOICES = [
        ('wedding', 'Wedding Film'),
        ('pre_wedding', 'Pre-Wedding Film'),
        ('engagement', 'Engagement Film'),
        ('destination_wedding', 'Destination Wedding'),
        ('save_the_date', 'Save the Date'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=150)

    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,default='wedding')
    location = models.CharField(max_length=150, blank=True)
    cover_image = models.ImageField(upload_to='film_teasers/')
    youtube_url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)   
    
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class PhotographyPackage(models.Model):

    cover_image = models.ImageField(upload_to='package_covers/',blank=True,null=True)

    PACKAGE_CHOICES = [
        ('standard', 'Standard'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
        ('platinum', 'Platinum'),
    ]

    name = models.CharField(max_length=20,choices=PACKAGE_CHOICES,unique=True)

    events_covered = models.CharField(max_length=500)

    includes = models.TextField()

    special_offer = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.get_name_display()




class Enquiry(models.Model):

    EVENT_CHOICES = [
        ('wedding', 'Wedding'),
        ('pre_wedding', 'Pre-Wedding'),
        ('engagement', 'Engagement'),
        ('maternity', 'Maternity'),
        ('birthday', 'Birthday'),
        ('other', 'Other'),
    ]

    PACKAGE_CHOICES = [
        ('standard', 'Standard'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
        ('platinum', 'Platinum'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    category = models.CharField(max_length=50,choices=EVENT_CHOICES)

    package = models.CharField(max_length=20,choices=PACKAGE_CHOICES,blank=True)

    event_date = models.DateField(blank=True, null=True)

    event_location = models.CharField(max_length=200, blank=True)

    message = models.TextField(blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

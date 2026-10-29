
from django import forms
from .models import Review,Portfolio,PhotographyPackage,Enquiry


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review
        
        fields = ['customer_name','place','rating','comment',]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name'
            }),
            'place': forms.TextInput(attrs={
                'placeholder': 'Enter your place'
            }),
            'rating': forms.Select(choices=[
                (5, '5 - Excellent'),
                (4, '4 - Very Good'),
                (3, '3 - Good'),
                (2, '2 - Fair'),
                (1, '1 - Poor'),
            ]),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review',
                'rows': 4,
            }),
        }


class PortfolioForm(forms.ModelForm):

    description = forms.CharField(required=False,widget=forms.Textarea)

    class Meta:

        model = Portfolio
        
        fields = ['title','category','description','image',]

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            max_size = 10 * 1024 * 1024  # 5 MB

            if image.size > max_size:
                raise forms.ValidationError(
                    "Image size must be less than 5 MB."
                )

        return image


from .models import FilmTeaser

class FilmTeaserForm(forms.ModelForm):

    class Meta:
        model = FilmTeaser
        fields = ['title','category','location','cover_image','youtube_url','description','is_featured','is_active',]


class PhotographyPackageForm(forms.ModelForm):

    class Meta:
        model = PhotographyPackage

        fields = ['name','cover_image','events_covered','includes','special_offer','is_active',]

        widgets = {
            'events_covered': forms.TextInput(attrs={
                'placeholder': 'Wedding Eve + Wedding Day'
            }),
            'includes': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Enter all package inclusions...'
            }),
            'special_offer': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter special offer (optional)'
            }),
        }

class EnquiryForm(forms.ModelForm):

    class Meta:

        model = Enquiry

        fields = ['name','email','phone','category','package','event_date','event_location','message',]

        widgets = {
            'event_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'message': forms.Textarea(
                attrs={'rows': 4}
            ),
        }

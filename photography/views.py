from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm

from photography.forms import ReviewForm,PortfolioForm,FilmTeaserForm,PhotographyPackageForm
from photography.models import Review,Portfolio,FilmTeaser,PhotographyPackage

from django.conf import settings

class HomeView(View):

    def get(self, request,*args,**kwargs):

        approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')

        portfolios = Portfolio.objects.all().order_by('-created_at')

        films = FilmTeaser.objects.filter(is_active=True).order_by('-created_at')

        packages = PhotographyPackage.objects.filter(is_active=True)

        featured_film = FilmTeaser.objects.filter(is_active=True,is_featured=True).first()

        return render(request, 'photography/home.html',{'reviews': approved_reviews,'featured_film': featured_film,'portfolios': portfolios,'films': films,'packages': packages,'whatsapp_number': settings.WHATSAPP_NUMBER,'contact_phone': settings.CONTACT_PHONE,})

class ReviewSubmitView(View):

    def get(self, request, *args, **kwargs):

        form = ReviewForm()

        return render(request,'photography/review_form.html',{'form': form})

    def post(self, request, *args, **kwargs):

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.is_approved = False

            review.save()

            return redirect('home')

        return render(request,'photography/review_form.html',{'form': form})


class OwnerLoginView(View):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user.is_superuser:
                login(request, user)
                return redirect('owner_dashboard')

            else:
                form.add_error(
                    None,
                    'You are not authorized to access the owner dashboard.'
                )

        return render(request, 'accounts/login.html', {'form': form})



class OwnerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not request.user.is_superuser:

            return redirect('home')

        return super().dispatch(request, *args, **kwargs)


class OwnerDashboardView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        context = {
            'total_enquiries': Enquiry.objects.count(),

            'pending_enquiries': Enquiry.objects.filter(status='pending').count(),

            'in_progress_enquiries': Enquiry.objects.filter(status='in_progress').count(),

            'completed_enquiries': Enquiry.objects.filter(status='completed').count(),
        }

        return render(request,'owner/dashboard.html',context)

class OwnerLogoutView(View):

    def post(self, request, *args, **kwargs):

        logout(request)

        return redirect('home')






class OwnerReviewListView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        pending_reviews = Review.objects.filter(is_approved=False).order_by('-created_at')

        approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')

        context = {

            'pending_reviews': pending_reviews,

            'approved_reviews': approved_reviews,
            
        }

        return render(request, 'owner/reviews.html', context)


class ApproveReviewView(OwnerRequiredMixin, View):

    def post(self, request, review_id, *args, **kwargs):

        try:
            review = Review.objects.get(
                id=review_id,
                is_approved=False
            )
            
        except Review.DoesNotExist:
            return redirect('owner_reviews')

        review.is_approved = True
        review.save()

        return redirect('owner_reviews')


class OwnerReviewDeleteView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        review = get_object_or_404(Review,pk=kwargs['review_id'],is_approved=True)

        return render(request,'owner/review_delete.html',{'review': review})

    def post(self, request, *args, **kwargs):

        review = get_object_or_404(Review,pk=kwargs['review_id'],is_approved=True)

        review.delete()

        return redirect('owner_reviews')


class PortfolioUploadView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        form = PortfolioForm()

        return render(request,'owner/portfolio_upload.html',{'form': form})

    def post(self, request, *args, **kwargs):

        form = PortfolioForm(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            return redirect('owner_portfolio')

        return render(request,'owner/portfolio_upload.html',{'form': form})


from django.core.paginator import Paginator

class PortfolioListView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        search_query = request.GET.get('search', '').strip()

        portfolios = Portfolio.objects.all().order_by('-created_at')

        if search_query:

            portfolios = portfolios.filter(title__icontains=search_query)

        paginator = Paginator(portfolios, 10)  # divides the portfolio list into pages of 10 items.
        page_number = request.GET.get('page')  # reads the selected page number from the URL.
        page_obj = paginator.get_page(page_number)

        return render(request,'owner/portfolio_list.html',{'portfolios': portfolios,'page_obj': page_obj,'search_query': search_query,})



class PortfolioEditView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        portfolio = get_object_or_404(Portfolio,id=kwargs['pk'])

        form = PortfolioForm(instance=portfolio)

        return render(request,'owner/portfolio_edit.html',{'form': form,'portfolio': portfolio})

    def post(self, request, *args, **kwargs):

        portfolio = get_object_or_404(Portfolio,id=kwargs['pk'])

        form = PortfolioForm(request.POST,request.FILES,instance=portfolio)

        if form.is_valid():

            form.save()

            return redirect('owner_portfolio')

        return render(request,'owner/portfolio_edit.html',{'form': form,'portfolio': portfolio})




class PortfolioDeleteView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        portfolio = get_object_or_404(Portfolio,pk=kwargs['pk'])

        return render(request,'owner/portfolio_delete.html',{'portfolio': portfolio})

    def post(self, request, *args, **kwargs):

        portfolio = get_object_or_404(Portfolio,pk=kwargs['pk'])

        image = portfolio.image

        portfolio.delete()

        if image and image.name:

            image.storage.delete(image.name)

        return redirect('owner_portfolio')

from django.db import transaction

class FilmTeaserUploadView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        form = FilmTeaserForm()

        return render(request,'owner/film_upload.html',{'form': form})

    def post(self, request, *args, **kwargs):

        form = FilmTeaserForm(request.POST, request.FILES)

        if form.is_valid():

            with transaction.atomic():
                film = form.save(commit=False)

            if film.is_featured:
                
                FilmTeaser.objects.filter(is_featured=True).update(is_featured=False)

            film.save()

        return redirect('owner_films')


        return render(request,'owner/film_upload.html',{'form': form})


class FilmTeaserListView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        films = FilmTeaser.objects.all().order_by('-created_at')

        return render(request,'owner/film_list.html',{'films': films})



class FilmTeaserEditView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        film = get_object_or_404(FilmTeaser, pk=kwargs['pk'])

        form = FilmTeaserForm(instance=film)

        return render(request,'owner/film_edit.html',{'form': form, 'film': film})

    def post(self, request, *args, **kwargs):

        film = get_object_or_404(FilmTeaser, pk=kwargs['pk'])

        form = FilmTeaserForm(request.POST,request.FILES,instance=film)

        if form.is_valid():

            form.save()

            return redirect('owner_films')

        return render(request,'owner/film_edit.html',{'form': form, 'film': film})


class FilmTeaserDeleteView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        film = get_object_or_404(FilmTeaser, pk=kwargs['pk'])

        return render(request,'owner/film_delete.html',{'film': film})

    def post(self, request, *args, **kwargs):

        film = get_object_or_404(FilmTeaser, pk=kwargs['pk'])

        cover_image = film.cover_image

        film.delete()

        if cover_image and cover_image.name:

            cover_image.storage.delete(cover_image.name)

        return redirect('owner_films')


# package session 


class PhotographyPackageCreateView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        form = PhotographyPackageForm()

        return render(request,'owner/package_form.html',{'form': form, 'page_title': 'Add Photography Package'})

    def post(self, request, *args, **kwargs):

        form = PhotographyPackageForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect('owner_packages')

        return render(request,'owner/package_form.html',{'form': form, 'page_title': 'Add Photography Package'})


class PhotographyPackageListView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        packages = PhotographyPackage.objects.all().order_by('name')

        return render(request,'owner/package_list.html',{'packages': packages})


class PhotographyPackageUpdateView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        package = get_object_or_404(PhotographyPackage,pk=kwargs['pk'])

        form = PhotographyPackageForm(instance=package)

        return render(request,'owner/package_form.html',{'form': form,'package': package,'page_title': 'Edit Photography Package'})

    def post(self, request, *args, **kwargs):

        package = get_object_or_404(PhotographyPackage,pk=kwargs['pk'])

        form = PhotographyPackageForm(request.POST, request.FILES, instance=package)

        if form.is_valid():

            form.save()

            return redirect('owner_packages')

        return render(request,'owner/package_form.html',{'form': form,'package': package,'page_title': 'Edit Photography Package'})


class PhotographyPackageDeleteView(OwnerRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        package = get_object_or_404(PhotographyPackage,pk=kwargs['pk'])

        return render(request,'owner/package_delete.html',{'package': package})

    def post(self, request, *args, **kwargs):

        package = get_object_or_404(PhotographyPackage,pk=kwargs['pk'])

        package.delete()

        return redirect('owner_packages')





from django.contrib import messages

from .forms import EnquiryForm
from .models import Enquiry


class SubmitEnquiryView(View):

    def get(self, request):

        form = EnquiryForm()

        return render(request, 'home.html', {'enquiry_form': form})

    def post(self, request):

        form = EnquiryForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your enquiry has been registered successfully! '
                'Our team will contact you soon.'
            )
            return redirect('home')

        messages.error(
            request,
            'Please check your details and try again.'
        )

        return render(request, 'home.html', {'enquiry_form': form})


class OwnerEnquiriesView(OwnerRequiredMixin,View):

    def get(self, request):

        enquiries = Enquiry.objects.all().order_by('-created_at')

        return render(request, 'owner/enquiries.html', {'enquiries': enquiries})


class UpdateEnquiryStatusView(OwnerRequiredMixin,View):

    def post(self, request, enquiry_id):

        enquiry = get_object_or_404(Enquiry, id=enquiry_id)

        new_status = request.POST.get('status')

        valid_statuses = ['pending', 'in_progress', 'completed']

        if new_status in valid_statuses:

            enquiry.status = new_status

            enquiry.save(update_fields=['status'])

        return redirect('owner_enquiries')

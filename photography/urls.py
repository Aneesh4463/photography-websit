from django.urls import path
from photography import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('owner/dashboard/',views.OwnerDashboardView.as_view(), name='owner_dashboard'),

    path('accounts/login/',views.OwnerLoginView.as_view(),name='login'),

    path('owner/logout/',views.OwnerLogoutView.as_view(),name='owner_logout'),

    path('submit-review/',views.ReviewSubmitView.as_view(),name='submit_review'),

    path('owner/reviews/',views.OwnerReviewListView.as_view(),name='owner_reviews'),
   
    path('owner/reviews/<int:review_id>/approve/',views.ApproveReviewView.as_view(),name='approve_review'),

    path('owner/reviews/<int:review_id>/delete/',views.OwnerReviewDeleteView.as_view(),name='owner_review_delete'),

    path('owner/portfolio/upload/',views.PortfolioUploadView.as_view(),name='owner_portfolio_upload'),

    path('owner/portfolio/',views.PortfolioListView.as_view(),name='owner_portfolio'),

    path('owner/portfolio/<int:pk>/edit/',views.PortfolioEditView.as_view(),name='owner_portfolio_edit'),

    path('owner/portfolio/<int:pk>/delete/',views.PortfolioDeleteView.as_view(),name='owner_portfolio_delete'),

    path('owner/films/add/',views.FilmTeaserUploadView.as_view(),name='owner_film_add'),

    path('owner/films/',views.FilmTeaserListView.as_view(),name='owner_films'),

    path('owner/films/<int:pk>/edit/',views.FilmTeaserEditView.as_view(),name='owner_film_edit'),

    path('owner/films/<int:pk>/delete/',views.FilmTeaserDeleteView.as_view(),name='owner_film_delete'),

  
    path('owner/packages/add/',views.PhotographyPackageCreateView.as_view(),name='owner_package_add'),

    path('owner/packages/',views.PhotographyPackageListView.as_view(),name='owner_packages'),

    path('owner/packages/<int:pk>/edit/',views.PhotographyPackageUpdateView.as_view(),name='owner_package_edit'),

    path('owner/packages/<int:pk>/delete/',views.PhotographyPackageDeleteView.as_view(),name='owner_package_delete'),

    path('submit-enquiry/',views.SubmitEnquiryView.as_view(),name='submit_enquiry'),
    
    path('owner/enquiries/', views.OwnerEnquiriesView.as_view(), name='owner_enquiries'),

    path('owner/enquiries/<int:enquiry_id>/update-status/',views.UpdateEnquiryStatusView.as_view(),name='update_enquiry_status'),


]
from datetime import datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from contacts.models import Contact


# Create your views here.
def contact(request):
    if request.method == 'POST':
        listings = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contact_date = datetime.now
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already contacted the realtor to this listing")
                return redirect('/listings/' + listing_id)
        record = Contact(listings=listings, listing_id=listing_id, name=name, email=email, phone=phone,
                         message=message, user_id=user_id)
        record.save()
        send_mail(
            'Property Listing Inquiry',
            f'There has been an inquiry for {listings}. Sign into admin panel for more info',
            'walter@gmail.com',
            [email, realtor_email],
            fail_silently=False
        )
        messages.success(request, "Your request has been successfully added")
        return redirect('/listings/' + listing_id)
    else:
        return redirect('listings')

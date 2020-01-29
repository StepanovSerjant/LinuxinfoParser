from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import AboutMaster, PricePart, FeedbackItem, GalleryPhoto


# Create your views here.
def eweindex(request):
    if request.method == 'POST':
        return render(request, 'manicure/helloworld')

    return render(request, 'manicure/nicezapis.html')


def index(request):
    sent = False

    if request.method == 'POST':
        form = ContactForm( request.POST )
        if form.is_valid():
            to = 'stpnvlks@gmail.com'
            form.save()
            cd = form.cleaned_data
            subject = 'Запись'
            message = '{} {} желает к вам записаться. Номер телефона для связи: {}'.format( cd['name'], cd['last_name'], cd['phone_number'], cd['message'] )
            send_mail( subject, message, 'lekseylanding@yandex.ru', [to])
            sent = True

            return redirect ('s/')
        else:
            form_errors = form.errors

            priceparts = PricePart.objects.all()

            about = AboutMaster.objects.all().last()

            all_feeds = FeedbackItem.objects.all()

            all_gallery = GalleryPhoto.objects.all()

            return render( request, 'manicure/helloworld.html', {
                'priceparts': priceparts,
                'about': about,
                'all_feeds': all_feeds,
                'all_gallery': all_gallery,
                'form': form,
                'form_errors': form_errors
            } )

    else:

        # Очистка формы
        form = ContactForm()

        priceparts = PricePart.objects.all()

        about = AboutMaster.objects.all().last()

        all_feeds = FeedbackItem.objects.all()

        all_gallery = GalleryPhoto.objects.all()

        return render(request, 'manicure/helloworld.html', {
        'priceparts': priceparts,
        'about': about,
        'all_feeds': all_feeds,
        'all_gallery': all_gallery,
        'form': form,
        'sent': sent
    })



# отправка сообщения через форму
# https://evileg.com/ru/post/54/
# https://codengineering.ru/q/how-to-send-email-via-django-18910/

# карусель
# https://stackoverflow.com/questions/25314489/dynamic-carousel-with-django-and-bootstrap
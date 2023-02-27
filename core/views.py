from django.core.mail import send_mail
from django.shortcuts import reverse
from .forms import ContactForm
from django.views import generic
from django.contrib import messages
from django.conf import settings

class HomeView(generic.TemplateView):
    template_name = 'index.html'


class ContactView(generic.FormView):
    form_class=ContactForm
    template_name='contact.html'

    def get_success_url(self):
        return reverse("contact")
    
    def form_valid(self, form):
        messages.info(self.request, "연락해주셔서 감사합니다. 가능한 빨리 답변드리겠습니다.")
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')


        full_message = f"""
            Received message below from {name}, {email}
            ________________________
            {message}
            """

        send_mail(
            subject="고객으로 부터 메일이 도착했습니다",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        
        return super(ContactView, self).form_valid(form)
from django.template.loader import render_to_string

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.email import send_email

from .serializers import EmailContactFormSerializer


class EmailContactAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailContactFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        subject = "Mail from Contact Form @ Supplers.com"

        # Prepare the template context
        context = {
            "payload": payload,
        }
        # Render the email content using the template
        template = "email/contact_form.html"
        to_email = "info@supplers.se"
        reply_to = payload.get("email")

        try:
            send_email(context, template, to_email, subject, reply_to=[reply_to])
            return Response({"message": "Email sent successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

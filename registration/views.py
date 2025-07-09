from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils import timezone
from django.http import HttpResponse
from .models import DelegateCardRegistration, EventRegistration, PassPurchase
from .serializers import DelegateCardRegistrationSerializer, EventRegistrationSerializer, PassPurchaseSerializer
import openpyxl
from openpyxl.utils import get_column_letter
from registration.utils.email import send_smtp_email


### 1. EXEMPTIONS AND PASS LOGIC ###
EXEMPT_EVENTS = {
    'snap_saga', 'verse', 'reel_realm',
    'junior_mediquiz', 'senior_mediquiz',
    'case_presentation', 'poster_presentation',
    'research_paper', 'mediquiz', 'clinico_pathological_conference',
}

SPORTS_EVENTS = {'football', 'cricket', 'badminton', 'volleyball', 'table_tennis', 'throwball'}
CULT_EVENTS = {'solo_dance', 'duet_dance', 'mono_act', 'street_play', 'meme_making', 'face_painting'}
CULT_MAJOR_EVENTS = {'chorea', 'alaap', 'tinnitus', 'dernier_cri'}
LIT_EVENTS = {'debate', 'poetry', 'essay', 'elocution'}
QUIZ_EVENTS = {'medical_quiz', 'general_quiz'}

### 2. DELEGATE CARD REGISTRATION ###
class DelegateCardRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DelegateCardRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            reg = serializer.save()
            return Response({
                "message": "Registration submitted",
                "registration": DelegateCardRegistrationSerializer(reg).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        self.check_permissions(request)
        regs = DelegateCardRegistration.objects.all()
        serializer = DelegateCardRegistrationSerializer(regs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def verify_registration(request, pk):
    try:
        reg = DelegateCardRegistration.objects.get(pk=pk)
    except DelegateCardRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)

    reg.is_verified = True
    reg.verified_at = timezone.now()
    reg.save()

    send_smtp_email(
        to_email=reg.email,
        subject="✅ Delegate Card Verified – Spandan 2025",
        message=f"Hi {reg.name},\n\nYour delegate card (Tier: {reg.tier}) has been verified.\nThank you for registering!"
    )

    return Response({'message': 'Registration verified successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def export_verified_delegate_cards(request):
    regs = DelegateCardRegistration.objects.filter(is_verified=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Verified Delegate Cards"

    headers = ["Name", "Email", "Phone", "Tier", "Amount", "Verified At"]
    ws.append(headers)

    for reg in regs:
        ws.append([
            reg.name,
            reg.email,
            str(reg.phone),
            reg.tier,
            reg.amount,
            reg.verified_at.strftime("%Y-%m-%d %H:%M:%S") if reg.verified_at else ""
        ])

    for i, header in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 22

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=verified_delegate_cards.xlsx'
    wb.save(response)
    return response


### 3. EVENT REGISTRATION ###
class EventRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data.copy()
        raw_events = data.get("events", [])
        email = data.get("email")

        # Normalize event input
        if isinstance(raw_events, str):
            selected_events = set(e.strip() for e in raw_events.split(",") if e.strip())
        elif isinstance(raw_events, list):
            selected_events = set(raw_events)
        else:
            return Response({"error": "Invalid event format."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine if delegate card or pass is required
        needs_delegate = False
        invalid_cult_major = False

        for event in selected_events:
            if event in EXEMPT_EVENTS:
                continue
            elif event in CULT_MAJOR_EVENTS:
                needs_delegate = True
                invalid_cult_major = True
            elif event in SPORTS_EVENTS:
                has_pass = PassPurchase.objects.filter(email=email, pass_type='sports', is_verified=True).exists()
                if not has_pass:
                    needs_delegate = True
            elif event in CULT_EVENTS:
                has_pass = PassPurchase.objects.filter(email=email, pass_type='cult', is_verified=True).exists()
                if not has_pass:
                    needs_delegate = True
            elif event in LIT_EVENTS:
                has_lit = PassPurchase.objects.filter(email=email, pass_type__in=['lit', 'lit_premium'], is_verified=True).exists()
                if not has_lit:
                    needs_delegate = True
            elif event in QUIZ_EVENTS:
                has_quiz = PassPurchase.objects.filter(email=email, pass_type__in=['quiz', 'lit_premium'], is_verified=True).exists()
                if not has_quiz:
                    needs_delegate = True
            else:
                needs_delegate = True

        if needs_delegate:
            has_delegate = DelegateCardRegistration.objects.filter(email=email, is_verified=True).exists()
            if not has_delegate:
                return Response({"error": "Delegate card or valid pass required."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventRegistrationSerializer(data=data)
        if serializer.is_valid():
            reg = serializer.save()
            return Response({
                "message": "Event registration submitted",
                "registration": EventRegistrationSerializer(reg).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        self.check_permissions(request)
        regs = EventRegistration.objects.all()
        serializer = EventRegistrationSerializer(regs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def verify_event_registration(request, pk):
    try:
        reg = EventRegistration.objects.get(pk=pk)
    except EventRegistration.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)

    reg.is_verified = True
    reg.verified_at = timezone.now()
    reg.save()

    send_smtp_email(
        to_email=reg.email,
        subject="✅ Event Registration Verified – Spandan 2025",
        message=f"Hi {reg.name},\n\nYour registration has been verified for the following events:\n" +
                "\n".join(f"• {e}" for e in reg.events) +
                f"\n\nTotal paid: ₹{reg.amount}\nSee you at Spandan!"
    )

    return Response({'message': 'Event registration verified successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def export_verified_event_registrations(request):
    regs = EventRegistration.objects.filter(is_verified=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Verified Event Registrations"

    headers = ["Name", "Email", "Phone", "Events", "Amount", "Verified At"]
    ws.append(headers)

    for reg in regs:
        ws.append([
            reg.name,
            reg.email,
            reg.phone,
            ", ".join(reg.events),
            reg.amount,
            reg.verified_at.strftime("%Y-%m-%d %H:%M:%S") if reg.verified_at else ""
        ])

    for i, header in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 22

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=verified_event_registrations.xlsx'
    wb.save(response)
    return response


### 4. PASS PURCHASE ###
class PassPurchaseView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PassPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            reg = serializer.save()
            return Response({
                "message": "Pass purchase submitted",
                "purchase": PassPurchaseSerializer(reg).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        self.check_permissions(request)
        regs = PassPurchase.objects.all()
        serializer = PassPurchaseSerializer(regs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def verify_pass(request, pk):
    try:
        reg = PassPurchase.objects.get(pk=pk)
    except PassPurchase.DoesNotExist:
        return Response({'error': 'Pass not found'}, status=status.HTTP_404_NOT_FOUND)

    reg.is_verified = True
    reg.verified_at = timezone.now()
    reg.save()

    send_smtp_email(
        to_email=reg.email,
        subject=f"✅ {reg.get_pass_type_display()} Verified – Spandan 2025",
        message=f"Hi {reg.name},\n\nYour {reg.get_pass_type_display()} pass has been verified.\nYou're now eligible to register for supported events. Thank you!"
    )

    return Response({'message': 'Pass verified successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def export_verified_passes(request):
    regs = PassPurchase.objects.filter(is_verified=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Verified Pass Purchases"

    headers = ["Name", "Email", "Phone", "Pass Type", "Amount", "Verified At"]
    ws.append(headers)

    for reg in regs:
        ws.append([
            reg.name,
            reg.email,
            reg.phone,
            reg.get_pass_type_display(),
            reg.amount,
            reg.verified_at.strftime("%Y-%m-%d %H:%M:%S") if reg.verified_at else ""
        ])

    for i, header in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 22

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=verified_passes.xlsx'
    wb.save(response)
    return response

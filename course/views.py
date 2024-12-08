from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsModer, IsOwner
from .models import Course, Lesson, Subscription, Payment
from .paginators import CustomPagination
from .serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PaymentSerializer
from .serveces import create_product, create_price, create_checkout_session
from .tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = (~IsModer,)
    #     elif self.action in ['update', 'retrieve']:
    #         self.permission_classes = (IsModer | IsOwner,)
    #     elif self.action == 'destroy':
    #         self.permission_classes = (IsOwner | ~IsModer,)
    #     return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (~IsModer, AllowAny)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, IsModer | IsOwner)

class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, IsModer | IsOwner)

class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = (IsAuthenticated, IsModer | IsOwner)


class SubscriptionAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            message = 'Subscription already exists'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Subscription added'

        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Subscription removed'
        else:
            message = 'Subscription does not exist'

        return Response({"message": message})


class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        amount = int(course.price * 100)

        product = create_product(course.name)
        price = create_price(product.id, amount)
        session = create_checkout_session(price.id, 'https://127.1.0.1:8000/', 'https://example.com/cancel')

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            stripe_product_id=product.id,
            stripe_price_id=price.id,
            stripe_session_id=session.id,
            amount=course.price,
            link=session.url
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# views.py


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_update(self, serializer):
        course = serializer.save()
        users = course.subscriptions.all().values_list('user__email', flat=True)
        for user_email in users:
            send_course_update_email.delay(user_email, course.name)

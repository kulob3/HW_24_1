from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from course.models import Course, Lesson
from .validators import validate_youtube_url
from .models import Subscription


class LessonSerializer(ModelSerializer):
    video = serializers.URLField(validators=[validate_youtube_url])
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    video = serializers.URLField(validators=[validate_youtube_url])
    class Meta:
        model = Course
        fields = '__all__'

class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'



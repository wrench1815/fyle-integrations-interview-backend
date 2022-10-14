from rest_framework import serializers

from apps.students.models import Assignment, GRADE_CHOICES


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    '''
        Teacher Assignment Serializer
    '''

    class Meta:
        model = Assignment
        fields = '__all__'


class TeacherAssignmentGradeSerializer(serializers.Serializer):
    '''
        Teacher Assignment Grading Serializer
    '''

    id = serializers.IntegerField()
    grade = serializers.ChoiceField(choices=GRADE_CHOICES)

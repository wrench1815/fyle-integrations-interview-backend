from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import TeacherAssignmentSerializer, TeacherAssignmentGradeSerializer

from apps.students.models import Assignment


class TeacherListCreateAPIView(generics.GenericAPIView):
    '''
        allowed methods: GET PATCH

        GET:
            - List all the Assignments of the Teacher
        
        PATCH:
            - Grade an Assignment of a student
            payload:
                {
                    "id": <assignment_id>,
                    "grade": <grade>
                }
    '''
    serializer_class = TeacherAssignmentSerializer

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)

        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        if 'content' in request.data:
            return Response(
                data={
                    'non_field_errors':
                    ['Teacher cannot change the content of the assignment']
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if 'student' in request.data:
            return Response(
                data={
                    'non_field_errors': [
                        'Teacher cannot change the student who submitted the assignment'
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TeacherAssignmentGradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment = None

        try:
            assignment = Assignment.objects.get(id=serializer.data['id'])
        except Assignment.DoesNotExist:
            return Response(
                data={
                    'error': 'Assignment does not exist',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if assignment.teacher.user != request.user:
            return Response(
                data={
                    'non_field_errors':
                    ['Teacher cannot grade for other teacher'
                     's assignment']
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if assignment.state == 'SUBMITTED':
            try:
                assignment.grade = serializer.data['grade']
                assignment.state = 'GRADED'
                assignment.save()

            except Exception as ex:
                return Response(
                    data={
                        'Failed to Grade Assignment. Try Again.',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif assignment.state == 'GRADED':
            return Response(
                data={
                    'non_field_errors':
                    ['GRADED assignments cannot be graded again']
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            return Response(
                data={
                    'non_field_errors':
                    ['SUBMITTED assignments can only be graded']
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=self.serializer_class(assignment).data,
            status=status.HTTP_200_OK,
        )

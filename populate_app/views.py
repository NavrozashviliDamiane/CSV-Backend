import codecs
import csv

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Question


fs = FileSystemStorage(location='tmp/')


# Serializer
class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


# Viewset
class QuestionViewSet(viewsets.ModelViewSet):
   
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        """Upload data from CSV"""
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)
        
        question_list = []
        for id_, row in enumerate(reader):
            (
                
                name,
                type,
                description,
                answer, 
                count,
                percentage,
               
                
                        
                
            ) = row
            question_list.append(
                Question(
                   
                    percentage=percentage,
                    count=count,
                    answer=answer,
                    name=name,
                    description=description,
                    type=type,
                )
            )

        Question.objects.bulk_create(question_list)

        return Response("Successfully upload the data")

    @action(detail=False, methods=['POST'])
    def upload_data_with_validation(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("file")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)

        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        question_list = []
        for row in serializer.data:
            question_list.append(
                Question(
                    
                    name=row["Question"],
                    type=row["Segment Type"],
                    description=row["Segment Description"],
                    answer=row["Answer"],
                    count=row["Count"],
                    percentage=row["Percentage"],   
                    
                    
                )
            )

        Question.objects.bulk_create(question_list)

        return Response("Successfully upload the data")
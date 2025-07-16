from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import status

import json
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from datetime import datetime
from .kafka_producer import send_kafka_event

class processView(APIView):
    parser_classes=(MultiPartParser, FormParser)
    def get(self,request):
        return Response("GET Request")
    def post(self,request):
        file_obj=request.FILES.get('pdf',None)
        pages=request.POST.get('pages','').split(',')

        if not file_obj:
            return Response({"error":"PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not pages:
            return Response({"error":"PDF file page list is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        pages=list(map(int,pages))

        try:
            assert isinstance(pages,list)
        except Exception:
            return Response({"error":"Invalid pages data"}, status=status.HTTP_400_BAD_REQUEST)

        send_kafka_event(
            event='pdf_uploaded',
            metadata={
                'file_name': str(file_obj),
                'timestamp': datetime.now().isoformat(),
            }
        )

        try:
            reader=PdfReader(file_obj)
            writer=PdfWriter()

            pages.sort()
            for page in pages:
                if 0<=page and page<len(reader.pages):
                    writer.add_page(reader.pages[page])
                else:
                    return Response({'error':f'Page {page} out of range.'},status=status.HTTP_400_BAD_REQUEST)

            output_stream = BytesIO()
            writer.write(output_stream)
            output_stream.seek(0)

            response = HttpResponse(output_stream.getvalue(), content_type='application/pdf', status=201)
            response['Content-Disposition']='attachment; filename="extracted_pages.pdf"'
            return response
        except Exception as e:
            return Response({'error':f'Processing Failed: {str(e)}'},status=500)
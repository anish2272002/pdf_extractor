import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from pypdf import PdfWriter
from pypdf import PdfReader
from io import BytesIO

@pytest.mark.django_db
def test_process_pdf_view():
    client = APIClient()

    # Create a fake pdf with 3 pages
    buffer = BytesIO()
    writer = PdfWriter()
    for i in range(3):
        writer.add_blank_page(width=72, height=72)
    writer.write(buffer)
    buffer.seek(0)

    # simulate file upload
    pdf_file = buffer
    pdf_file.name = "sample.pdf"
    data = {
        "pdf": pdf_file,
        "pages": "0,2"
    }

    # call the endpoint
    url = reverse("pdfprocessor:process_pdf")
    response = client.post(url, data, format='multipart')

    # Validate response
    assert response.status_code == 201
    assert response['Content-Type'] == 'application/pdf'

    # Read returned PDF and verify page count
    returned_pdf = BytesIO(response.content)
    reader = PdfReader(returned_pdf)

    assert len(reader.pages)==2
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Document
from .forms import DocumentForm
import requests
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
#from PyPDF2 import PdfReader, PdfWriter
import io

def index(request):
    return HttpResponse("Hello, world!")

def spdf(request):
    sdocuments = Document.objects.all()
    for obj in sdocuments:
        title = obj.description
        baseurls = obj.document
    print(baseurls)
    print(title)
    filepath = './media/'+str(baseurls)
    print(filepath)
    images = convert_from_path(filepath)
    pdf_writer = PyPDF2.PdfFileWriter()
    for image in images:
        page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
        pdf_writer.addPage(pdf.getPage(0))
    with open("./media/output.pdf", "wb") as f:
        pdf_writer.write(f)
    print('ok')
    return render(request, 'searchpdf.html', { 'sdocuments': sdocuments })

def pdf_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #func_obj = form
            #func_obj.sourceFile = form.cleaned_data['sourceFile']
            form.save()
            #print(form.Document.document)
            #form.save()
            return redirect('spdf')
    else:
        form = DocumentForm()
        documents = Document.objects.all().order_by('-id')
    return render(request, 'pdf_upload.html', {
        'form': form, 'documents': documents
    })

def delete_document(request,id):
    if request.method == 'POST':
        document = Document.objects.get(id=id)
        document.delete()
        return redirect('pdf_upload')
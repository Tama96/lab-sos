from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from mahasiswa.models import Pkl
from catatan import models, forms
from forum.models import Forum
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string, get_template
from weasyprint import HTML
import tempfile
from django.views import View

def index(req):
    group = req.user.groups.first()
    tasks = models.Catatan.objects.filter(owner=req.user)
    form_catatan = forms.CatatanForm()
    form_gambar = forms.GambarForm()
    # forum = models.Forum.objects.all()

    if req.method == 'POST':
        form_catatan = forms.CatatanForm(req.POST)
        if form_catatan.is_valid():
            form_catatan.instance.owner=req.user
            form_catatan.save()
        images = []
        files = req.FILES.getlist('upload_img')
        for file in files:
            images.append(models.Gambar.objects.create(upload_img=file,catatan=form_catatan.instance))
        return redirect('/')

    if group is not None and group.name == 'dosen':
        return render(req, 'dosen/index.html')
    elif group is not None and group.name == 'staf':
        tasks = models.Catatan.objects.all()
        return render(req, 'staf/index.html')
    else:
        return render(req, 'home/index.html', {
            'data': tasks,
            'form_catatan' : form_catatan,
            'form_gambar' : form_gambar,
            # 'forum': forum,
        })
        
    return render(req, 'staf/index.html')

def delete_catatan(req, id):
    models.Catatan.objects.filter(pk=id).delete()
    return redirect('/')

def forum_mhs(req):
    forum = models.tasks.objects.filter(pk=id)
    return render(req, 'home/index.html',{
        'forum': forum,
    })

def cetak(req):
    cetak = models.Catatan.objects.all()
    print(cetak)
    return render(req, 'home/cetak.html',{
        'cetak': cetak,
    })

# #def cetak(req):
#     # ambil data
#     catatan = models.Catatan.objects.all()

#     # render pdf
#     html_string = render_to_string('static/pdf.html', {'catatan':catatan})
#     html = HTML(string=html_string)
#     result = html.write_pdf()

#     #buat http response
#     response = HttpResponse(content_type='static/pdf')
#     response['Content-Disposition'] = 'inline; filename=catatan.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name,'r')
#         response.write(output.read())
#     return response

# def render_to_pdf(template_src, context_dict={}):
# 	template = get_template(template_src)
# 	html  = template.render(context_dict)
# 	result = BytesIO()
# 	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# 	if not pdf.err:
# 		return HttpResponse(result.getvalue(), content_type='application/pdf')
# 	return None


# data = {
# 	"Nama": "Aldy",
# 	"NIM": "14522174",
#     "Lokasi LabSos" : "Praxis Academy",
# 	}

# # #Opens up page as PDF
# class ViewPDF(View):
# 	def get(self, request, *args, **kwargs):

# 		pdf = render_to_pdf('home/pdf_template.html', data)
# 		return HttpResponse(pdf, content_type='application/pdf')


# #Automaticly downloads to PDF file
# class DownloadPDF(View):
# 	def get(self, request, *args, **kwargs):
		
# 		pdf = render_to_pdf('app/pdf_template.html', data)

# 		response = HttpResponse(pdf, content_type='application/pdf')
# 		filename = "Invoice_%s.pdf" %("12341231")
# 		content = "attachment; filename='%s'" %(filename)
# 		response['Content-Disposition'] = content
# 		return response
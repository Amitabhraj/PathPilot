from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from PathPilot.decorators import login_required

@login_required
def generate_ats_pdf(request):
    resume = request.user.current_resume
    template = get_template('resume_template.html')
    html = template.render({'resume': resume})
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
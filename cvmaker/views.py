from django.shortcuts import render

# Create your views here.
def cvmaker(request):
    return render(request, 'htmlfiles/base.html')

def form(request):
    return render(request, 'htmlfiles/form.html')


from django.http import JsonResponse

from django.shortcuts import render

def cv_view(request):
    if request.method == 'POST':
        # Extract personal information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Extract education information
        education_degrees = request.POST.getlist('education_degree[]')
        education_institutions = request.POST.getlist('education_institution[]')
        education_start_dates = request.POST.getlist('education_start_date[]')
        education_end_dates = request.POST.getlist('education_end_date[]')

        education_entries = [
            {
                "degree": degree,
                "institution": institution,
                "start_date": start_date,
                "end_date": end_date,
            }
            for degree, institution, start_date, end_date in zip(
                education_degrees, education_institutions, education_start_dates, education_end_dates
            )
        ]

        # Extract work experience
        experience_titles = request.POST.getlist('experience_title[]')
        experience_companies = request.POST.getlist('experience_company[]')
        experience_start_dates = request.POST.getlist('experience_start_date[]')
        experience_end_dates = request.POST.getlist('experience_end_date[]')
        experience_responsibilities = request.POST.getlist('experience_responsibilities[]')

        # Format responsibilities to include bullet points
# Format responsibilities without adding extra bullets
        formatted_experience_entries = [
            {
                "title": title,
                "company": company,
                "start_date": start_date,
                "end_date": end_date,
                "responsibilities": responsibility  # Keep plain text
            }
            for title, company, start_date, end_date, responsibility in zip(
                experience_titles, experience_companies, experience_start_dates, experience_end_dates, experience_responsibilities
            )
        ]


        # Extract other fields
        skills = request.POST.get('skills')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # Prepare data for rendering
        context = {
            "personal_info": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
            },
            "education": education_entries,
            "experience": formatted_experience_entries,
            "skills": skills,
            "contact_info": {
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
            },
        }

        return render(request, 'htmlfiles/temp1.html', context)

    return render(request, 'htmlfiles/form.html')

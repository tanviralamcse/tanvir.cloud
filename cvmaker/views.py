from django.shortcuts import render
import base64
from io import BytesIO
from datetime import datetime
# Create your views here.
def cvmaker(request):
    return render(request, 'htmlfiles/base.html')

def form(request):
    return render(request, 'htmlfiles/form.html')

def cv_view(request):
    if request.method == 'POST':
        # Extract personal information
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Handle photo upload (do not store it)
        photo = request.FILES.get('photo')  # assuming 'photo' is the name attribute of the file input
        photo_base64 = None
        if photo:
            # Encode the photo to base64
            photo_file = BytesIO(photo.read())
            photo_base64 = base64.b64encode(photo_file.getvalue()).decode('utf-8')

        # Helper function to format date
        def format_date(date_str):
            try:
                # Assuming the input format is YYYY-MM-DD
                return datetime.strptime(date_str, '%Y-%m-%d').strftime('%m/%d/%Y')
            except (ValueError, TypeError):
                return date_str  # Return the original value if formatting fails

        # Extract education information
        education_degrees = request.POST.getlist('education_degree[]')
        education_institutions = request.POST.getlist('education_institution[]')
        education_location = request.POST.getlist('education_location[]')
        education_start_dates = request.POST.getlist('education_start_date[]')
        education_end_dates = request.POST.getlist('education_end_date[]')

        education_entries = [
            {
                "degree": degree,
                "institution": institution,
                "location": location,
                "start_date": format_date(start_date),
                "end_date": format_date(end_date),
            }
            for degree, institution, location, start_date, end_date in zip(
                education_degrees, education_institutions, education_location, education_start_dates, education_end_dates
            )
        ]

        # Extract work experience
        experience_titles = request.POST.getlist('experience_title[]')
        experience_companies = request.POST.getlist('experience_company[]')
        experience_location = request.POST.getlist('experience_location[]')
        experience_start_dates = request.POST.getlist('experience_start_date[]')
        experience_end_dates = request.POST.getlist('experience_end_date[]')
        experience_responsibilities = request.POST.getlist('experience_responsibilities[]')

        # Format responsibilities without adding extra bullets
        formatted_experience_entries = [
            {
                "title": title,
                "company": company,
                "location": location,
                "start_date": format_date(start_date),
                "end_date": format_date(end_date),
                "responsibilities": responsibility  # Keep plain text
            }
            for title, company, location, start_date, end_date, responsibility in zip(
                experience_titles, experience_companies, experience_location, experience_start_dates, experience_end_dates, experience_responsibilities
            )
        ]
        skills = request.POST.get('skills', '')
        skill_list = [skill.strip() for skill in skills.split(',')]
        # Extract other fields
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        context = {
            "personal_info": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "photo_base64": photo_base64,  # Pass base64-encoded photo to the next page
            },
            "education": education_entries,
            "experience": formatted_experience_entries,
            "skills": skill_list,
            "contact_info": {
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
            },
        }

        return render(request, 'htmlfiles/temp1.html', context)

    return render(request, 'htmlfiles/form.html')
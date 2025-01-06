from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Calculate dynamic start and end dates
            today = datetime.today()
            next_month = today + relativedelta(months=1)
            internship_start_date = datetime(next_month.year, next_month.month, 1).strftime('%d %B %Y')  # 1st day of next month
            internship_end_date = (datetime(next_month.year, next_month.month, 1) + relativedelta(months=1)).strftime('%d %B %Y')  # 1st day of the month after next

            # Generate the Fusion Tech internship message
            internship_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }}
        .header {{
            background-color: #f4f4f4;
            padding: 10px 20px;
            text-align: center;
            border-radius: 5px;
        }}
        .header h1 {{
            color: #333;
        }}
        .content {{
            margin: 20px;
            color: #555;
        }}
        .content h2 {{
            color: #007BFF;
        }}
        .link {{
            color: #007BFF;
            text-decoration: none;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #999;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎉 Congratulations, {name}! 🎉</h1>
        <p>Welcome to the <strong>Fusion Tech Internship Program</strong>.</p>
    </div>
    <div class="content">
        <h2>Your Internship Details</h2>
        <p><strong>Start Date:</strong> {internship_start_date}</p>
        <p><strong>End Date:</strong> {internship_end_date}</p>
        <p>We are thrilled to have you join us! During this internship, you will work on exciting projects, gain valuable experience, and showcase your skills.</p>

        <h2>Important Links</h2>
        <ul>
            <li><strong>Offer Letter:</strong> <a class="link" href="https://fusiontech.com/offer-letter" target="_blank">Download Here</a></li>
            <li><strong>Tasks/Projects:</strong>
                <ul>
                    <li><a class="link" href="https://t.me/fusiontech" target="_blank">Join Fusion Tech Telegram Group</a></li>
                    <li><a class="link" href="https://linkedin.com/company/fusiontech" target="_blank">Follow us on LinkedIn</a></li>
                    <li><a class="link" href="https://instagram.com/fusiontech" target="_blank">Follow us on Instagram</a></li>
                </ul>
            </li>
        </ul>

        <h2>Guidelines for Success</h2>
        <ol>
            <li>Update your LinkedIn profile with all your achievements (e.g., Offer Letter, Completion Certificate) and tag @FusionTech. Use #FusionTech in your posts.</li>
            <li>Maintain originality in your work; copied projects or code will result in termination.</li>
            <li>Share a video of your completed tasks on LinkedIn. Tag @FusionTech and use #FusionTech.</li>
            <li>Maintain a GitHub repository named <strong>FusionTech</strong> for your tasks and share the link in the task submission form.</li>
        </ol>

        <p>If you have any questions, feel free to reach out to your team leader or email us directly.</p>
    </div>
    <div class="footer">
        <p>Best Regards,<br><strong>Team Fusion Tech</strong></p>
        <p>Email: <a class="link" href="contact@fusiontech.com">contact@fusiontech.com</a> | Website: <a class="link" href="https://www.fusiontech.com" target="_blank">www.fusiontech.com</a> | Telegram: <a class="link" href="https://t.me/fusiontech" target="_blank">https://t.me/fusiontech</a></p>
    </div>
</body>
</html>
"""

            # Generate PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 800, "Fusion Tech Internship Program")
            p.drawString(100, 780, f"Dear {name},")
            p.drawString(100, 760, f"Congratulations on being selected for the Fusion Tech Internship Program!")
            p.drawString(100, 740, f"Your internship starts on {internship_start_date} and ends on {internship_end_date}.")
            p.drawString(100, 720, "Please check the email for detailed instructions.")
            p.drawString(100, 700, "Best Regards,")
            p.drawString(100, 680, "Team Fusion Tech")
            p.showPage()
            p.save()
            buffer.seek(0)

            # Send Email
            mail = EmailMessage(
                subject="🎉 Welcome to Fusion Tech Internship Program! 🎉",
                body=internship_message,
                from_email="your_email@gmail.com",
                to=[email],
            )
            mail.content_subtype = "html"  # Set email format to HTML
            mail.attach("FusionTechDetails.pdf", buffer.getvalue(), "application/pdf")
            mail.send()

            return HttpResponse("Thank you! Your internship details have been sent.")
    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})

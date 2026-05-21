from django.db import migrations


TESTIMONIALS = [
    {
        "quote": "Man, I used to sit around truck stops for days waiting on a decent load. Since switching to Nestway, my dispatcher actually listens. If I tell them I want to run hard, they keep the miles coming.",
        "author_name": "Marcus T.",
        "author_subtitle": "3 years with Nestway",
        "initials": "MT",
        "order": 0,
        "is_active": True,
    },
    {
        "quote": "A lot of companies promise you the world and then short your paycheck. With these guys, the settlements are clean, no hidden fees, and the money is in my account every single Friday. Period.",
        "author_name": "Dave R.",
        "author_subtitle": "1.5 years with Nestway",
        "initials": "DR",
        "order": 1,
        "is_active": True,
    },
    {
        "quote": "The best part is they don't force dispatch. If a lane doesn't make sense for my bottom line, I say no and we move on to the next one. They treat me like a business partner, not a steering wheel holder.",
        "author_name": "Jason K.",
        "author_subtitle": "4 years with Nestway",
        "initials": "JK",
        "order": 2,
        "is_active": True,
    },
]

FAQS = [
    {
        "question": "What routes are available?",
        "answer": "We operate nationwide across all 48 contiguous states with consistent OTR freight and optimized load planning. Our network is built for long-haul efficiency and high-volume lanes.",
        "order": 0,
        "is_active": True,
    },
    {
        "question": "How often do I get home?",
        "answer": "Home time depends on your preferred schedule, freight availability, and how long you choose to stay out. Drivers who stay on the road longer typically maximize weekly earnings and load opportunities.",
        "order": 1,
        "is_active": True,
    },
    {
        "question": "What does the pay package look like?",
        "answer": "$0.65–$0.72/mile with an average of $0.68 CPM. Transparent, weekly direct deposit. Zero holdbacks.",
        "order": 2,
        "is_active": True,
    },
    {
        "question": "What's the truck age and condition?",
        "answer": "Our fleet averages 2.3 years old. All trucks are 2021 or newer — maintained, clean, and ready to roll.",
        "order": 3,
        "is_active": True,
    },
    {
        "question": "How do I apply and how long does it take?",
        "answer": "3 minutes online. We review within 24 hours and will call you directly to walk through next steps.",
        "order": 4,
        "is_active": True,
    },
    {
        "question": "How many miles can drivers expect weekly?",
        "answer": "Most OTR drivers average 2,500–3,200 miles per week depending on lanes and time out. Drivers who prioritize staying loaded consistently hit the higher end of that range.",
        "order": 5,
        "is_active": True,
    },
    {
        "question": "Is there forced dispatch?",
        "answer": "No forced dispatch. Our dispatchers work with you to find loads that fit your direction and timing. The goal is to keep you moving efficiently, not to push loads that don't make sense for your operation.",
        "order": 6,
        "is_active": True,
    },
    {
        "question": "How quickly are drivers reloaded?",
        "answer": "Our dispatch team actively pre-plans the next load before you deliver. Most drivers are reloaded same-day or within a few hours of dropping. Minimizing dead time is a core part of how we operate.",
        "order": 7,
        "is_active": True,
    },
    {
        "question": "How does dispatch support drivers?",
        "answer": "You have a dedicated dispatcher who knows your lanes and preferences. They handle load planning, check calls, and are reachable when you need support on the road. Communication is direct, not through a call center.",
        "order": 8,
        "is_active": True,
    },
]


def seed_testimonials_and_faqs(apps, schema_editor):
    Testimonial = apps.get_model('core', 'Testimonial')
    FAQ = apps.get_model('core', 'FAQ')

    for t in TESTIMONIALS:
        Testimonial.objects.get_or_create(author_name=t['author_name'], defaults=t)

    for f in FAQS:
        FAQ.objects.get_or_create(question=f['question'], defaults=f)


def reverse_seed(apps, schema_editor):
    Testimonial = apps.get_model('core', 'Testimonial')
    FAQ = apps.get_model('core', 'FAQ')
    Testimonial.objects.all().delete()
    FAQ.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_add_testimonial_faq_aboutphoto'),
    ]

    operations = [
        migrations.RunPython(seed_testimonials_and_faqs, reverse_seed),
    ]

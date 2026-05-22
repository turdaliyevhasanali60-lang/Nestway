from django.db import migrations


def seed_data(apps, schema_editor):
    # ── US Team Members ──────────────────────────────────────────────────────
    USTeamMember = apps.get_model('core', 'USTeamMember')
    us_team = [
        {
            'name': 'Marcus T.',
            'role': 'Director of US Operations',
            'bio': 'Over 15 years in the trucking industry across the Eastern US corridor. Marcus oversees all dispatch coordination, carrier relations, and compliance across our US-based fleet.',
            'order': 1,
        },
        {
            'name': 'Angela R.',
            'role': 'Driver Success Manager',
            'bio': 'Angela is the first point of contact for all driver onboarding. With a background in logistics and HR, she ensures every driver feels supported from day one on the road.',
            'order': 2,
        },
        {
            'name': 'James O.',
            'role': 'Fleet Safety & Compliance',
            'bio': 'FMCSA-certified safety specialist with deep expertise in DOT regulations, HOS compliance, and carrier risk management. James keeps every truck running clean and compliant.',
            'order': 3,
        },
        {
            'name': 'Carla M.',
            'role': 'Freight Coordinator',
            'bio': 'Carla works directly with brokers and shippers to secure premium loads for our drivers. Her relationships with top-tier carriers ensure consistent high-paying freight for our fleet.',
            'order': 4,
        },
    ]
    for member in us_team:
        USTeamMember.objects.get_or_create(
            name=member['name'],
            defaults=member
        )

    # ── Awards ───────────────────────────────────────────────────────────────
    Award = apps.get_model('core', 'Award')
    awards = [
        {
            'title': 'Top Dispatch Service',
            'issuer': 'American Trucking Excellence Awards',
            'year': '2025',
            'description': 'Recognized as one of the top-performing dispatch services in the continental US for outstanding carrier support and load efficiency.',
            'icon_name': 'award',
            'order': 1,
        },
        {
            'title': 'FMCSA Safety Standard Certified',
            'issuer': 'Federal Motor Carrier Safety Administration',
            'year': '2024',
            'description': 'Achieved full FMCSA compliance certification, demonstrating our unwavering commitment to road safety and regulatory excellence.',
            'icon_name': 'shield',
            'order': 2,
        },
        {
            'title': 'Premium Carrier Alliance',
            'issuer': 'DAT Freight & Analytics',
            'year': '2024',
            'description': 'Awarded Premium Carrier status on DAT One — recognizing our consistently high performance scores, on-time delivery rate, and broker satisfaction ratings.',
            'icon_name': 'star',
            'order': 3,
        },
        {
            'title': 'Outstanding Partner of the Year',
            'issuer': 'Coyote Logistics',
            'year': '2023',
            'description': 'Selected as Outstanding Carrier Partner for exceptional load acceptance rates, professional communication, and consistent on-time performance across high-volume lanes.',
            'icon_name': 'truck',
            'order': 4,
        },
    ]
    for award in awards:
        Award.objects.get_or_create(
            title=award['title'],
            defaults=award
        )

    # ── Partner Reviews ───────────────────────────────────────────────────────
    PartnerReview = apps.get_model('core', 'PartnerReview')
    reviews = [
        {
            'quote': "Working with Khamidjon and the Nestway team has been a game changer for our freight network. Their dispatchers are professional, fast, and never leave a load hanging. We've moved hundreds of loads together and the reliability is unmatched.",
            'author_name': 'David K.',
            'company_name': 'BlueStar Brokerage LLC',
            'relationship': 'Primary Broker Partner',
            'initials': 'DK',
            'order': 1,
        },
        {
            'quote': "Kim runs a tight, professional operation. Every time we book with Nestway, the driver shows up on time, communicates clearly, and delivers without issues. In this industry, that kind of reliability is rare — and we are proud to call them partners.",
            'author_name': 'Sarah M.',
            'company_name': 'FastLane Freight Solutions',
            'relationship': 'Freight Broker',
            'initials': 'SM',
            'order': 2,
        },
        {
            'quote': "I've worked with dozens of dispatch services over the years. Nestway is in a different league. Kim personally oversees complex loads and their team is available around the clock. Highly recommend for any broker looking for a dependable carrier.",
            'author_name': 'Robert T.',
            'company_name': 'Keystone Logistics Group',
            'relationship': 'Senior Freight Broker',
            'initials': 'RT',
            'order': 3,
        },
        {
            'quote': "Nestway's drivers are always well-prepared, compliant, and professional. Their back-office support team under Khamidjon's leadership makes booking easy and stress-free. One of our top-rated carrier partners year over year.",
            'author_name': 'Linda P.',
            'company_name': 'Coyote Logistics',
            'relationship': 'Carrier Relationship Manager',
            'initials': 'LP',
            'order': 4,
        },
    ]
    for review in reviews:
        PartnerReview.objects.get_or_create(
            author_name=review['author_name'],
            company_name=review['company_name'],
            defaults=review
        )

    # ── Driver Requirements ───────────────────────────────────────────────────
    DriverRequirement = apps.get_model('core', 'DriverRequirement')
    requirements = [
        # Shared (both)
        {'requirement_text': 'Valid Class A Commercial Driver\'s License (CDL)', 'driver_type': 'both', 'order': 1},
        {'requirement_text': 'Clean Motor Vehicle Record (MVR) for the past 3 years', 'driver_type': 'both', 'order': 2},
        {'requirement_text': 'Minimum 23 years of age', 'driver_type': 'both', 'order': 3},
        {'requirement_text': 'No DUI/DWI convictions in the past 5 years', 'driver_type': 'both', 'order': 4},
        {'requirement_text': 'Able to pass DOT pre-employment drug screen', 'driver_type': 'both', 'order': 5},
        # Company Drivers only
        {'requirement_text': 'Minimum 1 year OTR or regional driving experience', 'driver_type': 'company', 'order': 6},
        {'requirement_text': 'Valid Medical Examiner\'s Certificate (DOT Physical)', 'driver_type': 'company', 'order': 7},
        {'requirement_text': 'No more than 2 preventable accidents in the last 3 years', 'driver_type': 'company', 'order': 8},
        # Owner Operators only
        {'requirement_text': 'Minimum 2 years OTR experience as a professional driver', 'driver_type': 'owner_operator', 'order': 6},
        {'requirement_text': 'Truck must be 2015 model year or newer', 'driver_type': 'owner_operator', 'order': 7},
        {'requirement_text': 'Must carry $1M liability and $100K cargo insurance', 'driver_type': 'owner_operator', 'order': 8},
        {'requirement_text': 'Active MC/DOT authority or willing to lease under Nestway\'s', 'driver_type': 'owner_operator', 'order': 9},
        {'requirement_text': 'ELD device compliant (Samsara or Motive preferred)', 'driver_type': 'owner_operator', 'order': 10},
    ]
    for req in requirements:
        DriverRequirement.objects.get_or_create(
            requirement_text=req['requirement_text'],
            driver_type=req['driver_type'],
            defaults=req
        )


def unseed_data(apps, schema_editor):
    USTeamMember = apps.get_model('core', 'USTeamMember')
    Award = apps.get_model('core', 'Award')
    PartnerReview = apps.get_model('core', 'PartnerReview')
    DriverRequirement = apps.get_model('core', 'DriverRequirement')
    USTeamMember.objects.all().delete()
    Award.objects.all().delete()
    PartnerReview.objects.all().delete()
    DriverRequirement.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_award_driverrequirement_partnerreview_usteammember_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]

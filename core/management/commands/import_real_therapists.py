from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Specialty, Therapist
import json

class Command(BaseCommand):
    help = 'Import real therapists from provided data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Importing real therapists...')
            
            # Real therapists data
            therapists_data = [
                {
                    "id": "21",
                    "name": "Consolata Mathari Hospital Psychiatric Clinic (Nyeri)",
                    "location": "Consolata Mathari Hospital, Nyeri",
                    "county": "Nyeri County",
                    "town": "Nyeri",
                    "phone": "+254 721 358 137",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Psychiatric clinic in Nyeri offering mental health support.",
                    "full_bio": "Consolata Mathari Hospital Psychiatric Clinic provides mental health services in Nyeri. An additional contact number provided is +254 702 697 344.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "12",
                    "name": "Dr. Catherine Munanie Syengo Mutisya",
                    "location": "KMA Centre, Upper Hill, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254714 972228",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Consultant Psychiatrist specializing in general psychiatry, family therapy, and mental health service leadership.",
                    "full_bio": "Consultant Psychiatrist (MBChB and MMed Psychiatry from University of Nairobi) with extensive experience in leadership, advocacy, and clinical practice. Specializes in general psychiatry and family therapy.",
                    "qualifications": ["MBChB", "MMed Psychiatry (University of Nairobi)"],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Family Therapy"]
                },
                {
                    "id": "15",
                    "name": "Dr. Daniel Waiganjo Kinyanjui",
                    "location": "Eldoret",
                    "county": "Uasin Gishu County",
                    "town": "Eldoret",
                    "phone": "+254774 248 196",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Psychiatrist providing general psychiatric services in Eldoret.",
                    "full_bio": "Psychiatrist based in Eldoret providing psychiatric consultations and care.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "2",
                    "name": "Dr. David Kagwi Wairoto",
                    "location": "Chiromo Lane Doctors Plaza, Muthangari Road, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 745 113 866",
                    "whatsapp": None,
                    "email": "info@neurowellnessclinic.co.ke",
                    "bio": "Consultant Psychiatrist focusing on adult mental health including depression, stress, anxiety, and related conditions.",
                    "full_bio": "Consultant Psychiatrist with qualifications including MBChB and MMed Psychiatry (University of Nairobi), plus AIMIS (Strathmore). Runs Neuro Wellness Clinic, focusing on general adult psychiatry including depression, stress, anxiety, and related conditions.",
                    "qualifications": ["MBChB", "MMed Psychiatry (University of Nairobi)", "AIMIS (Strathmore)"],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression", "Stress Management", "Anxiety"]
                },
                {
                    "id": "18",
                    "name": "Dr. Erica Adagala",
                    "location": "AFC House Building, Nakuru",
                    "county": "Nakuru County",
                    "town": "Nakuru",
                    "phone": "+254 713 046 424",
                    "whatsapp": None,
                    "email": "pristonhealthcareltd@gmail.com",
                    "bio": "KPA Consultant Psychiatrist offering general psychiatric care in Nakuru.",
                    "full_bio": "KPA Consultant Psychiatrist offering general psychiatric care, including stress, depression, and anxiety management in Nakuru.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression", "Stress Management", "Anxiety"]
                },
                {
                    "id": "4",
                    "name": "Dr. J M M'Ndegwa 'MBS'",
                    "location": "Integrated Clinical Services (NICS), Nairobi (P.O. Box 22486-00400)",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 769 075 962",
                    "whatsapp": None,
                    "email": "ndegwa@nics.co.ke",
                    "bio": "Consultant Psychiatrist with special interest in addiction medicine, psychotrauma, and adult psychiatry.",
                    "full_bio": "Consultant Psychiatrist (also known as Dr. Japheth Mwenda M'Ndegwa) with special interest in addiction medicine, psychotrauma, and adult psychiatry. Practices at Integrated Clinical Services (NICS).",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Addiction", "Trauma"]
                },
                {
                    "id": "11",
                    "name": "Dr. Jackline Ochieng'",
                    "location": "Menelik Medical Centre, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 720 291 232",
                    "whatsapp": None,
                    "email": "frontdesk@gileadmh.com",
                    "bio": "Specialist Psychiatrist providing diagnosis, treatment, and support for general mental health concerns.",
                    "full_bio": "Specialist Psychiatrist at Gilead Mental Health Consultants / Menelik Medical Centre (MBChB Makerere, MMed Psychiatry Nairobi). Provides general psychiatric care, focusing on diagnosis, treatment, and support for adults.",
                    "qualifications": ["MBChB (Makerere)", "MMed Psychiatry (University of Nairobi)"],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression", "Stress Management", "Anxiety"]
                },
                {
                    "id": "17",
                    "name": "Dr. Kevin Wamula",
                    "location": "Pandya Hospital, Dedan Kimathi Avenue, Mombasa",
                    "county": "Mombasa County",
                    "town": "Mombasa",
                    "phone": "+254 734 600 663",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Psychiatrist at Pandya Hospital with interests including treatment-resistant depression and ketamine therapy.",
                    "full_bio": "Psychiatrist at Pandya Hospital (Mombasa) specializing in treatment-resistant depression, ketamine therapy, and general mental health concerns.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression"]
                },
                {
                    "id": "9",
                    "name": "Dr. Kingi K Mochache",
                    "location": "Fortis Suites, Upperhill, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 741 668 020",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Consultant Psychiatrist providing general psychiatric care and medication management.",
                    "full_bio": "Consultant Psychiatrist (MBChB 2007, MMed Psychiatry 2016 from University of Nairobi) running a specialist psychiatry clinic and providing general psychiatric care.",
                    "qualifications": ["MBChB (2007)", "MMed Psychiatry (University of Nairobi, 2016)"],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "14",
                    "name": "Dr. Lina Akello",
                    "location": "Oasis Doctor Plaza, Kakamega (also Aga Khan Kisumu)",
                    "county": "Kakamega County",
                    "town": "Kakamega",
                    "phone": "+254 710 292 903",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Consultant Psychiatrist providing general psychiatric services across Western Kenya and Kisumu.",
                    "full_bio": "Consultant Psychiatrist providing general psychiatric services across Oasis and Aga Khan facilities in Western Kenya and Kisumu.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "19",
                    "name": "Dr. Linda N. Nyamute",
                    "location": "Jaramogi Oginga Odinga Teaching & Referral Hospital (Kisumu area)",
                    "county": "Kisumu County",
                    "town": "Kisumu",
                    "phone": "+254737 879 077",
                    "whatsapp": None,
                    "email": "mentalsphereke@gmail.com",
                    "bio": "Psychiatrist focused on general adult psychiatry and community mental health.",
                    "full_bio": "Psychiatrist at Jaramogi Oginga Odinga Teaching & Referral Hospital (Kisumu area), focused on general adult psychiatry and community mental health.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "7",
                    "name": "Dr. Margaret Othieno Makanyengo",
                    "location": "Greenhouse Mall, Ngong Road, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 782 829 509",
                    "whatsapp": None,
                    "email": "info@oasishealthcaregroup.com",
                    "bio": "Consultant Psychiatrist with 21+ years of experience, formerly at Kenyatta National Hospital.",
                    "full_bio": "Esteemed Consultant Psychiatrist with over 21 years of experience (formerly at Kenyatta National Hospital, where she pioneered HIV psychiatry and gender-based violence services). Now at Oasis Healthcare Group, providing specialized care for HIV-related issues, trauma, and general psychiatry.",
                    "qualifications": [],
                    "experience": "21+ years",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "HIV Psychiatry", "Trauma"]
                },
                {
                    "id": "3",
                    "name": "Dr. Neema Araka",
                    "location": "FITAHI CONSULTANCY CLINIC, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254704 453 316",
                    "whatsapp": None,
                    "email": "fitahi254@gmail.com",
                    "bio": "Psychiatrist specializing in preventive and promotive mental health, psychotherapy, and resilience-building.",
                    "full_bio": "Psychiatrist at FITAHI CONSULTANCY CLINIC specializing in preventive and promotive mental health. Expertise in behavioral therapy, psychotherapy, stress & anger management, insomnia, self-esteem issues, social anxiety, emotion regulation, grief, loss, and loneliness.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Stress Management", "Anxiety", "Anger Management", "Sleep / Insomnia", "Grief & Loss", "Self-Esteem", "Emotion Regulation"]
                },
                {
                    "id": "10",
                    "name": "Dr. Pauline Ng'ang'a",
                    "location": "University of Nairobi Dept of Psychiatry / Chiromo Hospital Group, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254115 876 000",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Dual-trained in clinical psychology and psychiatry, providing integrated care.",
                    "full_bio": "Consultant Psychiatrist at Chiromo Hospital Group (also affiliated with University of Nairobi Department of Psychiatry). Dual-trained in clinical psychology and psychiatry (MBChB, MSc Clin. Psy, MMed Psych) and handles a broad range of mental health issues.",
                    "qualifications": ["MBChB", "MSc Clinical Psychology", "MMed Psychiatry"],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression", "Stress Management", "Anxiety"]
                },
                {
                    "id": "5",
                    "name": "Dr. Rajab Saddam",
                    "location": "UpperHill Medical Center / H.S Medical Centre (KNH affiliated), Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 113 799 016",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Consultant Psychiatrist specializing in adult psychiatry.",
                    "full_bio": "Consultant Psychiatrist specializing in adult psychiatry. Works at UpperHill Medical Center / H.S Medical Centre and is affiliated with Kenyatta National Hospital.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression", "Anxiety"]
                },
                {
                    "id": "13",
                    "name": "Dr. Samuel Kamoche",
                    "location": "Laric Heart Centre, near Quickmart, Kakamega",
                    "county": "Kakamega County",
                    "town": "Kakamega",
                    "phone": "+254 714 965 619",
                    "whatsapp": "+254 714 965 619",
                    "email": None,
                    "bio": "Psychiatrist treating adults and children with a focus that includes addiction, stress, depression, and anxiety.",
                    "full_bio": "Psychiatrist treating adults and children in Western Kenya (Laric Heart Centre, Kakamega). Serves Kakamega, Bungoma, Busia, Kitale, and Vihiga.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry", "Depression", "Stress Management", "Anxiety", "Addiction"]
                },
                {
                    "id": "8",
                    "name": "Dr. Susan Hinga",
                    "location": "Mater Hospital, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 711 328 181",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Psychiatrist at Mater Hospital focusing on general adult psychiatry.",
                    "full_bio": "Psychiatrist at Mater Hospital with qualifications from Makerere (MBChB) and University of Nairobi (MMed Psychiatry). Focuses on general adult psychiatry.",
                    "qualifications": ["MBChB (Makerere)", "MMed Psychiatry (University of Nairobi)"],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "6",
                    "name": "Dr. Susan Wangeci Kuria",
                    "location": "Mathari National Teaching and Referral Hospital, Nairobi",
                    "county": "Nairobi County",
                    "town": "Nairobi",
                    "phone": "+254 751 180 101",
                    "whatsapp": None,
                    "email": "mental.health.care.swk@gmail.com",
                    "bio": "Consultant Psychiatrist at Mathari National Teaching and Referral Hospital with expertise in adult psychiatry.",
                    "full_bio": "Consultant Psychiatrist at Mathari National Teaching and Referral Hospital, with expertise in adult psychiatry. Experienced in clinical care, research, and managing complex psychiatric conditions.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "22",
                    "name": "Nyeri County Referral Hospital Mental Health Outpatient",
                    "location": "Nyeri County Referral Hospital, Nyeri",
                    "county": "Nyeri County",
                    "town": "Nyeri",
                    "phone": "+254724 249 693",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Mental health outpatient services at Nyeri County Referral Hospital.",
                    "full_bio": "Nyeri County Referral Hospital provides mental health outpatient services. Contact the facility for appointment details.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "20",
                    "name": "Oasis Branches (Kisii Hospital & Siaya Hospital)",
                    "location": "Oasis Healthcare Group branches (Kisii & Siaya)",
                    "county": "Kisii County / Siaya County",
                    "town": "Kisii / Siaya",
                    "phone": "+254 111 161400",
                    "whatsapp": None,
                    "email": None,
                    "bio": "Psychiatry services available through Oasis Healthcare Group branches in Kisii and Siaya.",
                    "full_bio": "Oasis Healthcare Group provides psychiatry services via its Kisii and Siaya branches. Contact the facility to confirm clinician availability.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                },
                {
                    "id": "16",
                    "name": "Oasis Doctors Plaza Eldoret (Psychology & Psychiatry dept)",
                    "location": "Oasis Doctors Plaza, Eldoret",
                    "county": "Uasin Gishu County",
                    "town": "Eldoret",
                    "phone": "+254 111 161400",
                    "whatsapp": None,
                    "email": "info@oasishealthcaregroup.com",
                    "bio": "Psychology and psychiatry services available through Oasis Healthcare Group in Eldoret.",
                    "full_bio": "Oasis Doctors Plaza Eldoret offers psychology and psychiatry services. Contact the facility for appointments and service availability.",
                    "qualifications": [],
                    "experience": "",
                    "license_number": None,
                    "price": None,
                    "availability": None,
                    "specialization": ["Psychiatry"]
                }
            ]
            
            # Import therapists
            for therapist_data in therapists_data:
                specializations = therapist_data.pop('specialization', [])
                therapist_id = therapist_data.pop('id', None)
                
                # Get or create specialties
                specialty_objects = []
                for spec_name in specializations:
                    specialty, created = Specialty.objects.get_or_create(name=spec_name)
                    specialty_objects.append(specialty)
                
                # Create therapist
                therapist, created = Therapist.objects.update_or_create(
                    id=therapist_id,
                    defaults=therapist_data
                )
                
                if created:
                    therapist.specialization.set(specialty_objects)
                    self.stdout.write(f'Created therapist: {therapist.name}')
                else:
                    therapist.specialization.set(specialty_objects)
                    self.stdout.write(f'Updated therapist: {therapist.name}')
            
            self.stdout.write(self.style.SUCCESS('Successfully imported real therapists!'))

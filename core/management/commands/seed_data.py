from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Country, County, Specialty, Therapist, TherapistReview
import json
import os

class Command(BaseCommand):
    help = 'Seed initial data for the mental health support system'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Seeding initial data...')
            
            # Seed countries
            self.seed_countries()
            
            # Seed counties for Kenya
            self.seed_counties()
            
            # Seed specialties
            self.seed_specialties()
            
            # Seed sample therapists
            self.seed_therapists()
            
            self.stdout.write(self.style.SUCCESS('Successfully seeded initial data'))

    def seed_countries(self):
        countries = [
            {'name': 'Kenya', 'code': 'KE'},
            {'name': 'Uganda', 'code': 'UG'},
            {'name': 'Tanzania', 'code': 'TZ'},
        ]
        
        for country_data in countries:
            country, created = Country.objects.get_or_create(
                name=country_data['name'],
                defaults={'code': country_data['code']}
            )
            if created:
                self.stdout.write(f'Created country: {country.name}')

    def seed_counties(self):
        kenya = Country.objects.get(name='Kenya')
        
        counties = [
            'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
            'Kisii', 'Thika', 'Kitale', 'Garissa', 'Kakamega',
            'Nyeri', 'Machakos', 'Bungoma', 'Meru', 'Kericho'
        ]
        
        for county_name in counties:
            county, created = County.objects.get_or_create(
                name=county_name,
                country=kenya
            )
            if created:
                self.stdout.write(f'Created county: {county.name}')

    def seed_specialties(self):
        specialties = [
            'Clinical Psychology', 'Counseling Psychology', 'Psychiatry',
            'Child Psychology', 'Marriage & Family Therapy', 'Addiction Counseling',
            'Trauma Therapy', 'Cognitive Behavioral Therapy', 'Group Therapy',
            'Art Therapy', 'Music Therapy', 'Occupational Therapy'
        ]
        
        for specialty_name in specialties:
            specialty, created = Specialty.objects.get_or_create(name=specialty_name)
            if created:
                self.stdout.write(f'Created specialty: {specialty.name}')

    def seed_therapists(self):
        """Therapists should be added manually through Django admin or GraphQL API"""
        self.stdout.write('Therapists seeding skipped - add therapists through Django admin or API')
        pass

    def create_sample_reviews(self, therapist):
        reviews_data = [
            {
                'author': 'John M.',
                'rating': 5,
                'date': '2024-01-15',
                'comment': 'Excellent therapist. Very professional and understanding.'
            },
            {
                'author': 'Mary K.',
                'rating': 4,
                'date': '2024-02-20',
                'comment': 'Great experience. Helped me through a difficult time.'
            },
            {
                'author': 'David O.',
                'rating': 5,
                'date': '2024-03-10',
                'comment': 'Highly recommend! Very knowledgeable and compassionate.'
            }
        ]
        
        for review_data in reviews_data:
            TherapistReview.objects.get_or_create(
                therapist=therapist,
                author=review_data['author'],
                defaults=review_data
            )

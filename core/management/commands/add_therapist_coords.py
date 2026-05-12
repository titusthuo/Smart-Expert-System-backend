# core/management/commands/add_therapist_coords.py

from django.core.management.base import BaseCommand
from core.models import Therapist
import json

# Coordinates for major Kenyan towns/cities
# These are approximate coordinates for town centers
KENYAN_COORDS = {
    # Nairobi
    "nairobi": {"lat": -1.2921, "lng": 36.8219},
    "karen": {"lat": -1.3182, "lng": 36.7588},
    "westlands": {"lat": -1.2655, "lng": 36.8090},
    "hurlingham": {"lat": -1.2569, "lng": 36.8195},
    "upper hill": {"lat": -1.2827, "lng": 36.8219},
    "muthangari": {"lat": -1.2921, "lng": 36.8219},
    "chiromo": {"lat": -1.2827, "lng": 36.8219},
    "kileleshwa": {"lat": -1.2589, "lng": 36.8804},
    
    # Mombasa
    "mombasa": {"lat": -4.0435, "lng": 39.6682},
    "nyali": {"lat": -4.0535, "lng": 39.6738},
    
    # Nyeri
    "nyeri": {"lat": -0.4167, "lng": 36.9500},
    "nyeri county": {"lat": -0.4167, "lng": 36.9500},
    "consolata mathari": {"lat": -0.4167, "lng": 36.9500},
    
    # Kisumu
    "kisumu": {"lat": -0.0917, "lng": 34.7680},
    
    # Eldoret
    "eldoret": {"lat": 0.5143, "lng": 35.2698},
    
    # Nakuru
    "nakuru": {"lat": -0.3030, "lng": 36.0635},
    
    # Kakamega
    "kakamega": {"lat": 0.2843, "lng": 34.8188},
    
    # Kisii
    "kisii": {"lat": -0.6843, "lng": 34.7771},
    
    # Siaya
    "siaya": {"lat": 0.0564, "lng": 34.2041},
}

class Command(BaseCommand):
    help = 'Add coordinates to therapists based on their location/town names'

    def handle(self, *args, **options):
        therapists = Therapist.objects.all()
        updated_count = 0
        
        for therapist in therapists:
            coords = self._get_coords_for_location(therapist.location, therapist.town, therapist.county)
            if coords:
                therapist.lat = coords['lat']
                therapist.lng = coords['lng']
                therapist.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated {therapist.name} with coordinates: {coords}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Could not determine coordinates for: {therapist.location} ({therapist.town}, {therapist.county})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} therapists with coordinates'
            )
        )

    def _get_coords_for_location(self, location, town, county):
        """Try to find coordinates based on location, town, or county"""
        location_lower = location.lower() if location else ""
        town_lower = town.lower() if town else ""
        county_lower = county.lower() if county else ""
        
        # Direct town matches
        if town_lower in KENYAN_COORDS:
            return KENYAN_COORDS[town_lower]
        
        # County matches
        if county_lower in KENYAN_COORDS:
            return KENYAN_COORDS[county_lower]
        
        # Location name matches (extract town from location string)
        for key, coords in KENYAN_COORDS.items():
            if key in location_lower:
                return coords
        
        # Try to extract town from location string
        words = location_lower.split()
        for word in words:
            if word in KENYAN_COORDS:
                return KENYAN_COORDS[word]
        
        return None

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from taggit.managers import TaggableManager

GENDER_OPTION = (
    ('M', 'ذكر'),
    ('F', 'انثى'),
)

BLOOD_GROUP_OPTION = (
    ('A-', 'A-'),
    ('A+', 'A+'),
    ('B-', 'B-'),
    ('B+', 'B+'),
    ('AB-', 'AB-'),
    ('AB+', 'AB+'),
    ('O-', 'O-'),
    ('O+', 'O+'),
)

class Client_Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    name = models.CharField(_("الاسم"), max_length=50)
    image = models.ImageField(_("الصوره الشخصيه"), upload_to='client/profile/', null=True, blank=True)
    address = models.CharField(_("العنوان"), max_length=50, null=True, blank=True)
    address_detail = models.CharField(_("تفاصيل العنوان"), max_length=500, null=True, blank=True)
    number_phone = models.CharField(_("رقم الهاتف"), max_length=11)
    gender = models.CharField(_("الجنس"), max_length=10, choices=GENDER_OPTION)
    blood_group = models.CharField(_("فصيله الدم"), max_length=5, choices=BLOOD_GROUP_OPTION)
    date_of_birth = models.DateField(_("تاريخ الميلاد"), auto_now=False, auto_now_add=False, null=True, blank=True)
    zip_code = models.IntegerField(_("Zip Code"), null=True, blank=True)
    slug = models.SlugField(_("الاسم التعريفي"), null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Client_Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'

def create_profile(sender, instance, created, **kwargs):
    if created:
        Client_Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)


from django.db import models
from django.contrib.auth.models import User
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import os
from django.conf import settings
from PIL import Image
import joblib

class MedicalCondition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    
    def __str__(self):
        return self.name

class PatientAnalysis(models.Model):
    patient = models.ForeignKey(Client_Profile, on_delete=models.CASCADE)
    analysis_date = models.DateTimeField(auto_now_add=True)
    pdf_report = models.FileField(upload_to='medical_reports/')
    facial_analysis_image = models.ImageField(upload_to='facial_analysis/', null=True, blank=True)
    is_healthy = models.BooleanField(default=False)
    conditions = models.ManyToManyField(MedicalCondition, blank=True)
    analysis_results = models.JSONField(default=dict)
    recommendations = models.TextField()
    
    def analyze_pdf_report(self):
        # Load pre-trained models
        blood_model = load_model(os.path.join(settings.BASE_DIR, 'ai_models/blood_analysis_model.h5'))
        stool_model = load_model(os.path.join(settings.BASE_DIR, 'ai_models/stool_analysis_model.h5'))
        
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(self.pdf_report.path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        # Process text data
        results = self._extract_values_from_text(text)
        
        # Analyze blood results
        blood_features = self._prepare_blood_features(results)
        blood_prediction = blood_model.predict(np.array([blood_features]))
        
        # Analyze stool results if available
        stool_features = self._prepare_stool_features(results)
        if stool_features:
            stool_prediction = stool_model.predict(np.array([stool_features]))
        else:
            stool_prediction = None
            
        # Save analysis results
        self.analysis_results = {
            'blood_analysis': blood_prediction.tolist(),
            'stool_analysis': stool_prediction.tolist() if stool_prediction else None,
            'extracted_values': results
        }
        
        # Determine conditions
        self._determine_conditions()
        self.save()
    
    def analyze_facial_features(self, image_path):
        # Load facial analysis model
        face_model = load_model(os.path.join(settings.BASE_DIR, 'ai_models/facial_analysis_model.h5'))
        
        # Process image
        img = Image.open(image_path)
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        prediction = face_model.predict(img_array)
        
        # Update analysis results
        if 'facial_analysis' not in self.analysis_results:
            self.analysis_results['facial_analysis'] = {}
            
        self.analysis_results['facial_analysis'].update({
            'jaundice': float(prediction[0][0]),
            'pallor': float(prediction[0][1]),
            'cyanosis': float(prediction[0][2]),
            'hydration': float(prediction[0][3])
        })
        
        self._determine_conditions()
        self.save()
    
    def _extract_values_from_text(self, text):
        # This would be more sophisticated in production
        results = {}
        lines = text.split('\n')
        
        # Common blood test patterns
        blood_tests = {
            'hgb': ['hemoglobin', 'hgb'],
            'rbc': ['red blood cells', 'rbc'],
            'wbc': ['white blood cells', 'wbc'],
            # Add more test mappings
        }
        
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                key = parts[0].strip().lower()
                value = parts[1].strip()
                
                # Try to convert to float if numeric
                try:
                    value = float(value)
                except ValueError:
                    pass
                    
                # Map to standard keys
                for std_key, aliases in blood_tests.items():
                    if any(alias in key for alias in aliases):
                        results[std_key] = value
                        break
                else:
                    results[key] = value
                    
        return results
    
    def _prepare_blood_features(self, results):
        # Normalize and prepare features for blood model
        features = []
        
        # Standard blood test features in specific order
        blood_features_order = [
            'hgb', 'rbc', 'wbc', 'hct', 'mcv', 'mch', 'mchc', 
            'platelets', 'neutrophils', 'lymphocytes'
        ]
        
        for feature in blood_features_order:
            features.append(results.get(feature, 0))  # 0 or other default for missing
            
        return np.array(features)
    
    def _prepare_stool_features(self, results):
        # Check if we have stool test results
        stool_features_order = [
            'color', 'consistency', 'mucus', 'blood', 'ph', 
            'fat_content', 'white_blood_cells', 'bacteria'
        ]
        
        if any(key in results for key in stool_features_order):
            features = []
            for feature in stool_features_order:
                # Convert categorical to numerical if needed
                value = results.get(feature, 0)
                if isinstance(value, str):
                    # Simple encoding for demo - would be more sophisticated
                    value = len(value)  
                features.append(value)
            return np.array(features)
        return None
    
    def _determine_conditions(self):
        # Clear existing conditions
        self.conditions.clear()
        
        # Get blood analysis results
        blood_prediction = self.analysis_results.get('blood_analysis')
        if blood_prediction:
            blood_prediction = np.array(blood_prediction)
            
            # Example conditions based on prediction
            if blood_prediction[0][0] > 0.7:  # Anemia
                anemia = MedicalCondition.objects.get_or_create(
                    name="Anemia",
                    defaults={
                        'description': "Low red blood cell count or hemoglobin",
                        'symptoms': "Fatigue, weakness, pale skin",
                        'treatment': "Iron supplements, dietary changes"
                    }
                )[0]
                self.conditions.add(anemia)
                
            if blood_prediction[0][1] > 0.7:  # Infection
                infection = MedicalCondition.objects.get_or_create(
                    name="Infection",
                    defaults={
                        'description': "Elevated white blood cell count indicating infection",
                        'symptoms': "Fever, inflammation, pain",
                        'treatment': "Antibiotics or antiviral medication"
                    }
                )[0]
                self.conditions.add(infection)
        
        # Get facial analysis results if available
        facial = self.analysis_results.get('facial_analysis', {})
        if facial.get('jaundice', 0) > 0.7:
            jaundice = MedicalCondition.objects.get_or_create(
                name="Jaundice",
                defaults={
                    'description': "Yellowing of skin and eyes due to liver issues",
                    'symptoms': "Yellow skin/eyes, dark urine, fatigue",
                    'treatment': "Address underlying liver condition"
                }
            )[0]
            self.conditions.add(jaundice)
            
        # Determine if healthy
        self.is_healthy = self.conditions.count() == 0
        
        # Generate recommendations
        if self.is_healthy:
            self.recommendations = "All test results appear normal. No specific recommendations."
        else:
            conditions_list = ", ".join([c.name for c in self.conditions.all()])
            self.recommendations = f"Based on analysis, potential conditions detected: {conditions_list}. " \
                                 "Recommend consultation with appropriate specialist."
    
    def __str__(self):
        return f"Analysis for {self.patient.name} on {self.analysis_date}"
from django.db import models

# Create your models here.
class Vehicle(models.Model):
    Vehicle_id = models.AutoField
    Vehicle_name = models.CharField(max_length=60)
    Vehicle_company = models.CharField(max_length=60)
    Vehicle_model = models.CharField(max_length=60)
    Vehicle_type = models.CharField(max_length=20)
    Vehicle_fuel = models.CharField(max_length=10)
    Vehicle_No_of_Seats = models.IntegerField()
    Vehicle_color = models.CharField(max_length=20)
    Vehicle_license_plate = models.CharField(max_length=30)
    Vehicle_uploaded_by = models.CharField(max_length=100)
    Vehicle_image1 = models.ImageField(upload_to='img/Vehicle_images/')
    Vehicle_image2 = models.ImageField(upload_to='img/Vehicle_images/')
    Vehicle_image3 = models.ImageField(upload_to='img/Vehicle_images/')
    isGeared = models.BooleanField()
    Vehicle_description = models.CharField(max_length=1500)
    Vehicle_price = models.IntegerField()

    def save(self, *args, **kwargs):
        # Capitalize the first letter of each word in the Vehicle_company field
        if self.Vehicle_company:
            self.Vehicle_company = self.Vehicle_company.title()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.Vehicle_license_plate + " : " + str(self.Vehicle_name)
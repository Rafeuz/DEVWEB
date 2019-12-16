from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Perfil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	foto = models.ImageField(default='default.jpg', upload_to='fotos_perfil')

	def __str__(self):
		return f'Perfil de {self.user.username}'

	def save(self):
		super().save()

		img = Image.open(self.foto.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.foto.path)
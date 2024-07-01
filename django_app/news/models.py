from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class News(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key_phrase = models.CharField(max_length=255)
    api_response = models.JSONField(null=True)

    def __str__(self):
        return self.key_phrase
    
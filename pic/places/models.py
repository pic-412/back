from django.db import models
from django.conf import settings


class PlaceQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(
            models.Q(place__icontains=query) |
            models.Q(adress__icontains=query)
        )


class PlaceManager(models.Manager):
    def get_queryset(self):
        return PlaceQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Place(models.Model):
    id = models.BigAutoField(primary_key=True)
    place = models.CharField(max_length=100)
    adress = models.CharField(max_length=200, null=False)
    time = models.CharField(max_length=200, default="별도 운영시간 없음")
    image_url = models.CharField(max_length=512, null=True, blank=True)
    naver_url = models.CharField(max_length=512, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,  null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,  null=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Like',
        related_name='liked_places'
    )

    objects = PlaceManager()

    class Meta:
        db_table = "places"


class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"
        unique_together = ('account', 'place')

    def __str__(self):
        return f"{self.account.nickname} likes {self.place.place}"

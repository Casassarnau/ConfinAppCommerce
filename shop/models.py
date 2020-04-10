import uuid

from django.db import models

from user.models import User

SCH_DAYS = [
    (0, 'Dilluns'),
    (1, 'Dimarts'),
    (2, 'Dimecres'),
    (3, 'Dijous'),
    (4, 'Divendres'),
    (5, 'Dissabte'),
    (6, 'Diumenge'),
]


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class PrimaryCategory(Category):

    def get_secondaries(self):
        return self.secondary


class SecondaryCategory(Category):
    primary = models.ForeignKey(to=PrimaryCategory, related_name='secondary', on_delete=models.DO_NOTHING)


class Service(Category):
    pass


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CIF = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    meanTime = models.FloatField(null=True, blank=True)

    latitude = models.DecimalField(decimal_places=7, max_digits=11, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=11, null=True, blank=True)

    owner = models.ForeignKey(to=User, related_name='my_shop', on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, blank=True, related_name='shop')
    secondaryCategories = models.ManyToManyField(to=SecondaryCategory)
    services = models.ManyToManyField(to=Service, blank=True)

    photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    description = models.CharField(max_length=256)

    def __str__(self):
        return '%s__%s' % (self.name, self.CIF)

    class Meta:
        unique_together = (('CIF', 'name'),)


class Schedule(models.Model):
    shop = models.ForeignKey(to=Shop, related_name='schedule', on_delete=models.CASCADE)
    day = models.IntegerField(choices=SCH_DAYS)
    startHour = models.TimeField()
    endHour = models.TimeField()

    class Meta:
        unique_together = (("day", "startHour", 'shop'),)

    def get_day_name(self):
        return SCH_DAYS[self.day][1]


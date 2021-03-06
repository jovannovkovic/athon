import datetime
import hashlib
import random
import re

from exceptions import FollowingHimselfError
from signals import user_registered

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models, transaction
from django_enumfield import enum
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import int_to_base36
from django.utils.translation import gettext_lazy as _

from uuid_upload_path.storage import upload_to
from enums import Gender, FollowStatus, Unit as EnumUnit,\
        ChallengeResponse as ChallengeResponseEnum

from djorm_pgarray.fields import IntegerArrayField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class FollowUsersManager(models.Manager):

    def get_queryset(self):
        return super(FollowUsersManager, self).get_queryset().select_related(
                'follower__user', 'followed_user__user')


class FollowUsers(models.Model):
    """ Plan je sledeci. Kada nekog dodas, upises tvog usera prvo, posle njega.
    Onda proveris da li postoji unos gde je on prvi, a ti drugi. Ako postoji,
    na oba unosa stavis fallow_status na Fallowing, u suprotnom nista.

    Ako hocemo da zapratimo korisnika koji je privatan, onda upisemo sopstvenog usera prvo,
    njegovog drugo, request_status stavimo na True i fallow_status na Fallow.

    #Nisam siguran za sledecu recenicu
    Probamo da pronadjemo suprotan par (privatan, ja) i ako postoji njemu stavimo request_status na
    True isto.
    #

    Kada se zahtev odobri, probamo da nadjemo par (privatni, ja).
    SLUCAJ 1: AKo takav par postoji, stavljamo mu fallow_status na Fallowing i
    request_status na False.
    Onda nalazimo isti par (ja, privatni profil), stavljamo request_status na False,
    i fallow_status na Fallowing.
    SLUCAJ 2: Takav par ne postoji i onda samo paru (ja, privatni profil)
    stavljamo request_status na False.

    """
    objects = FollowUsersManager()

    follower = models.ForeignKey('Profile', related_name="following")
    followed_user = models.ForeignKey('Profile', related_name="followers")
    follow_status = enum.EnumField(FollowStatus)
    request_status = models.BooleanField(default=False)
    date_started = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        if self.follower == self.followed_user:
            raise FollowingHimselfError(
                    _("User cannot follow himself"))
        # else
        return super(FollowUsers, self).save(*args, **kwargs)

    def __unicode__(self):
        return "follower %s - followed %s" % (self.follower, self.followed_user)


class ProfileManager(models.Manager):

    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related(
                'user').prefetch_related('athlete_histories')

    def follow(self, follower, followed_user):
        if followed_user.is_public_profile:
            relationship, created = FollowUsers.objects.get_or_create(
                follower=follower,
                followed_user=followed_user
            )
            if created:
                self.update_counter_up(follower, followed_user)
            if self.update_status_to_following(followed_user, follower):
                relationship.follow_status = FollowStatus.FOLLOWING
                relationship.save()
            return True
        return False

    def update_status_to_following(self, user, following_user):
        try:
            relationship = FollowUsers.objects.get(follower=user, followed_user=following_user)
            relationship.fallow_status = FollowStatus.FOLLOWING
            relationship.save()
            return True
        except FollowUsers.DoesNotExist:
            return False

    def unfollow(self, follower, followed_user):
        try:
            FollowUsers.objects.get(follower=follower, followed_user=followed_user).delete()
            self.update_status_to_unfollow(followed_user, follower)
            self.update_counter_down(follower, followed_user)
            return True
        except FollowUsers.DoesNotExist:
            return False

    def update_status_to_unfollow(self, follower, followed_user):
        FollowUsers.objects.filter(follower=follower, followed_user=followed_user).update(
                follow_status=FollowStatus.FOLLOW
        )

    def request_to_follow(self, follower, followed_user):
        if not followed_user.is_public_profile:
            relationship, created = FollowUsers.objects.get_or_create(
                follower=follower,
                followed_user=followed_user,
                request_status=True
            )
            return True
        return False

    def remove_request(self, follower, followed_user):
        try:
            FollowUsers.objects.get(follower=follower, followed_user=followed_user).delete()
            return True
        except FollowUsers.DoesNotExist:
            return False

    def accept_request(self, follower, followed_user):
        try:
            relationship = FollowUsers.objects.get(follower=follower, followed_user=followed_user)
            relationship.request_status = False
            if self.update_accepted_request(followed_user, follower):
                relationship.fallow_status = FollowStatus.FOLLOWING
            relationship.save()
            self.update_counter_up(follower, followed_user)
            return True
        except FollowUsers.DoesNotExist:
            return False

    def update_accepted_request(self, follower, followed_user):
        try:
            relationship = FollowUsers.objects.get(follower=follower, followed_user=followed_user)
            relationship.fallow_status = FollowStatus.FOLLOWING
            relationship.save()
            return True
        except FollowUsers.DoesNotExist:
            return False

    def update_counter_up(self, follower, followed_user):
        follower.following_number = models.F('following_number') + 1
        follower.save()
        followed_user.followers_number = models.F('followers_number') + 1
        followed_user.save()

    def update_counter_down(self, follower, followed_user):
        follower.following_number = models.F('following_number') - 1
        follower.save()
        followed_user.followers_number = models.F('followers_number') - 1
        followed_user.save()


class Profile(models.Model):
    """ Dodatna polja za user-a.

    """
    objects = ProfileManager()

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name="profile")
    gender = enum.EnumField(Gender)
    birthday = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=225, null=True, blank=True)
    unit = enum.EnumField(EnumUnit)
    profile_photo = models.ImageField(upload_to=upload_to,
                                      null=True, blank=True)
    is_public_profile = models.BooleanField(default=True)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    follow_users = models.ManyToManyField('self', through='FollowUsers',
                symmetrical=False, related_name='related_to_following')
    following_number = models.PositiveIntegerField(default=0)
    # fallowers_user = models.ManyToManyField('self', through='Fallowers')
    followers_number = models.PositiveIntegerField(default=0)
    # fallowers_requests = models.ManyToManyField('self', through='FallowRequests')
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s profile" % self.user

    @classmethod
    def create_empty(cls, user):
        return cls.objects.create(user=user)


class Sport(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % self.name


class AthleteHistory(models.Model):
    """ User sport history and achievements.

    """
    profile = models.ForeignKey(Profile, null=True, blank=True, related_name='athlete_histories')
    sport = models.ForeignKey(Sport, null=True, blank=True)
    from_date = models.IntegerField(null=True, blank=True)
    until_date = models.IntegerField(null=True, blank=True)


class Achievement(models.Model):
    """ User achievements in sport.

    """
    athlete_history = models.ForeignKey(AthleteHistory, null=True, blank=True, related_name='achievements')
    title = models.CharField(max_length=225, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)


class Unit(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True,
                verbose_name='Npr. Kilometri')
    metric = models.CharField(max_length=10, null=True, blank=True,
                verbose_name='Npr. km')
    imperial = models.CharField(max_length=10, null=True, blank=True,
                verbose_name='Npr. mi')

    def __unicode__(self):
        return "Jedinica %s" % self.name


class TaggedMuscleWork(TaggedItemBase):
    content_object = models.ForeignKey('ExerciseType')


class TaggedSynonyms(TaggedItemBase):
    content_object = models.ForeignKey('ExerciseType')


class ExerciseTypeManager(models.Manager):

    def get_queryset(self):
        return super(ExerciseTypeManager, self).get_queryset().select_related(
                'unit', 'synonyms', 'muscle_work')


class ExerciseCategory(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True)


class ExerciseType(models.Model):
    objects = ExerciseTypeManager()

    name = models.CharField(max_length=125, null=True, blank=True)
    synonyms = TaggableManager(through=TaggedSynonyms, blank=True,
            related_name='exercise_synonyms')
    unit = models.ForeignKey(Unit, null=True, blank=True)
    quantity = models.BooleanField(default=False)
    repetition = models.BooleanField(default=False)
    body_weight = models.BooleanField(default=False)
    weighted = models.BooleanField(default=False)
    exercise_category = models.ForeignKey(ExerciseCategory, null=True, blank=True)
    muscle_work = TaggableManager(through=TaggedMuscleWork, blank=True,
            related_name='exercise_muscle')

    def __unicode__(self):
        return "Vezba %s" % self.name


class ActivityDetails(models.Model):
    rounds = models.CharField(max_length=125, null=True, blank=True)
    series = models.CharField(max_length=125, null=True, blank=True)
    interval = models.CharField(max_length=125, null=True, blank=True)
    for_time = models.CharField(max_length=125, null=True, blank=True)
    pace = models.CharField(max_length=125, null=True, blank=True)
    amrap = IntegerArrayField()


class ChallengeType(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True,
                verbose_name='Npr. DO, ili SPORT')


class Challenge(models.Model):
    post = models.ForeignKey('Post', related_name='challenge')
    deadline = models.DateTimeField()
    description = models.TextField()
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    type = models.ForeignKey(ChallengeType, null=True, blank=True)


class ChallengeResponse(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='responses')
    response = enum.EnumField(ChallengeResponseEnum)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_responded = models.DateTimeField(blank=True, null=True)
    result = models.FloatField(default=0)


class PostManager(models.Manager):

    def get_queryset(self):
        return super(PostManager, self).get_queryset().select_related(
            'activity_details', 'exercises').filter(hidden=False)


class Post(models.Model):

    objects = PostManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    title = models.CharField(max_length=125, null=True, blank=True)
    activity_name = models.CharField(max_length=225, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_to,
                null=True, blank=True)
    time = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    hidden = models.BooleanField(default=False)
    activity_details = models.ForeignKey(ActivityDetails, null=True, blank=True, default=None)
    like_number = models.PositiveIntegerField(default=0)
    comment_number = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s - %s" % (self.user, self.title, self.created_at)


class Exercise(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True, related_name='exercises')
    type = models.ForeignKey(ExerciseType)


class Repetition(models.Model):
    exercise = models.ForeignKey(Exercise, null=True, blank=True, related_name='reps')
    unit = models.ForeignKey(Unit, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    repetition = models.PositiveSmallIntegerField(default=0, null=True, blank=True)


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('user', 'post')


class PostComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)









""" USER REGISTRATION MODELS
"""


class RegistrationManager(models.Manager):
    def activate_user(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False

            if not profile.activation_key_expired():
                user = profile.user
                user_profile = user.profile
                user_profile.is_active = True
                user.save()
                user.backend = settings.AUTHENTICATION_BACKENDS[0]
                profile.activation_key = self.model.ACTIVATED
                profile.save()

                return user

        return False

    def create_inactive_user(self, username, email, password,
                             site):
        user_model = get_user_model()
        user = user_model.objects.create_user(username, email, password)
        profile = self.create_profile(user)
        profile.send_activation_email(site)

        return user

    create_inactive_user = transaction.atomic(create_inactive_user)

    def create_profile(self, user):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt + username).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key)


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.

    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.

    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.

    """
    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= timezone.now())

    activation_key_expired.boolean = True

    def send_activation_email(self, site):
        """
        Send an activation email to the user associated with this
        ``RegistrationProfile``.

        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site}
        subject = render_to_string('account/email_messages/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('account/email_messages/activation_email.txt',
                                   ctx_dict)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class PasswordResetManager(models.Manager):
    """ Password Reset Manager """

    def create_for_user(self, user):
        """ create password reset for specified user """
        # support passing email address too
        if type(user) is unicode:
            user = get_user_model().objects.get(email=user)

        temp_key = token_generator.make_token(user)

        # save it to the password reset model
        password_reset, created = PasswordReset.objects.get_or_create(user=user,
                temp_key=temp_key, reset=False)
        cs = Site.objects.get_current()
        # send the password reset email
        subject = _("Password reset email sent")
        message = render_to_string("account/email_messages/password_reset_key_message.txt", {
            "user": user,
            "uid": int_to_base36(user.id),
            "temp_key": temp_key,
            "site": cs
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return password_reset


class PasswordReset(models.Model):
    """
    Password reset Key
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))

    temp_key = models.CharField(_("temp_key"), max_length=100)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    reset = models.BooleanField(_("reset yet?"), default=False)

    objects = PasswordResetManager()

    class Meta:
        verbose_name = _('password reset')
        verbose_name_plural = _('password resets')
        app_label = 'athon'

    def __unicode__(self):
        return "%s (key=%s, reset=%r)" % (
            self.user.username,
            self.temp_key,
            self.reset
        )


def create_profile(sender, user=None, **kwargs):
    Profile.create_empty(user)


user_registered.connect(create_profile)
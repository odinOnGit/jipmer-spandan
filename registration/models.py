from django.db import models
from django.utils import timezone

TIERS = (
  ('tier1', 'Issue #1'),
  ('tier2', 'Deluxe Edition'),
  ('tier3', 'Collectors Print'),
)

TIER_PRICES = {
  'tier1' : 375,
  'tier2' : 650,
  'tier3' : 850,
}

class DelegateCardRegistration(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  phone = models.CharField(max_length=15)
  tier = models.CharField(max_length=10, choices=TIERS)
  amount = models.IntegerField()
  payment_screenshot = models.ImageField(upload_to='delegate_payments/')
  is_verified = models.BooleanField(default=False)
  verified_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    self.amount = TIER_PRICES.get(self.tier, 0)
    super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.name} - {self.tier}"
  

EVENT_FEES = {
    # Fine Arts & Culturals
    'face_painting': 100,
    'pot_painting': 100,
    'mehendi': 100,
    'sketching': 100,
    'painting': 100,
    'solo_dance': 125,
    'duet_dance': 125,
    'chorea': 150,
    'tinnitus': 200,
    'alaap': 250,
    'show_down': 150,
    'euphony': 150,
    'raag_rangmanch': 150,
    'solo_singing': 150,
    'solo_instrumental': 150,
    'play': 125,
    'skit': 125,
    'mime': 125,
    'adzap': 125,
    'variety': 125,
    'dernier_cri': 250,

    # Sports
    'cricket': 300,
    'football': 300,
    'basketball_men': 300,
    'basketball_women': 300,
    'volleyball_men': 300,
    'volleyball_women': 300,
    'hockey_men': 300,
    'hockey_women': 300,
    'futsal': 300,
    'chess_bullet': 150,
    'chess_rapid': 200,
    'chess_blitz': 200,
    'chess_team': 200,
    'carroms': 250,
    'throwball_men': 300,
    'throwball_women': 300,
    'tennis': 300,
    'aquatics': 200,
    'badminton': 250,
    'table_tennis': 250,
    'athletics': 200,

    # Literary
    'malarkey': 150,
    'shipwrecked': 150,
    'turncoat': 150,
    'scrabble': 150,
    'formal_debate': 150,
    'cryptic_crossword': 150,
    'ppt_karaoke': 150,
    'potpourri': 150,
    'india_quiz': 150,
    'fandom_quiz': 150,
    'sports_quiz': 150,
    'rewind_quiz': 150,

    'formal_debate': 250,
    'tj_jaishankar_memorial_quiz': 250,
    'jam': 250,

    # Academics
    'junior_mediquiz': 600,
    'senior_mediquiz': 600,

    # Photography
    'snap_saga': 100,
    'verse': 125,
    'reel_realm': 100,

    # Informals (free)
    'treasure_hunt': 0,
    'eatathon': 0,
}

class EventRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    events = models.JSONField(help_text="List of selected events")
    amount = models.PositiveIntegerField(blank=True)
    payment_screenshot = models.ImageField(upload_to='event_payments/')
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        total = 0
        for event in self.events:
            total += EVENT_FEES.get(event, 0)
        self.amount = total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {', '.join(self.events)}"

PASS_AMOUNTS = {
  'sports': 250,
  'cult': 250,
  'lit_quiz': 500,
  'lit_lit': 500,
  'lit_premium': 750,
}

class PassPurchase(models.Model):
   PASS_CHOICES = [
        ('sports', 'Nexus Arena (Sports Pass)'),
        ('cult', 'Nexus Spotlight (Cult Pass)'),
        ('lit_quiz', 'Nexus Forum - Quiz'),
        ('lit_lit', 'Nexus Forum - Literary/Debate'),
        ('lit_premium', 'Nexus Forum - Premium'),
   ]

   name = models.CharField(max_length=100)
   email = models.EmailField()
   phone = models.CharField(max_length=15)
   pass_type = models.CharField(max_length=20, choices= PASS_CHOICES)
   amount = models.IntegerField()
   payment_screenshot = models.ImageField(upload_to='pass_screenshots/', null=True, blank=True)
   is_verified = models.BooleanField(default=False)
   verified_at = models.DateTimeField(null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def save(self, *args, **kwargs):
      self.amount = PASS_AMOUNTS.get(self.pass_type, 0)
      super().save(*args, **kwargs)

   def __str__(self):
      return f"{self.name} - {self.pass_type}"
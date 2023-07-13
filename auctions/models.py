from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', related_name="watchlist")
    pass

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(max_length=200)
    image = models.URLField(
        default='https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png')
    created_at = models.DateTimeField(default=timezone.now)
    categories= (
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Sports", "Sports"),
    )
    category = models.CharField(max_length=100, choices=categories, default="Fashion")
    is_active =models.BooleanField(default=True)
    winner = models.CharField(max_length=100, blank=True, null=True)
    bids_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def is_expired(self):
        return self.created_at < timezone.now()
    
    def highest_bid(self):
        return self.bids.order_by("bidding_price").first()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update highest bid before saving the auction
        self.highest_bid = self.bids.order_by("-bidding_price").first()
        super().save(*args, **kwargs)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidding_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bidding_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bidding_user.username} : ${self.bidding_price}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

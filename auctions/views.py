from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.http import require_http_methods

from .models import User, Auction, Bid, Comment
from .forms import AuctionForm, CommentForm

def index(request):
    auctions = Auction.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        'auctions' : auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def createlisting(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)

        # save the auction
        if form.is_valid():
            auction = Auction(user=request.user, **form.cleaned_data)
            auction.user = request.user
            auction.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/createlisting.html", {
            "form": AuctionForm()
        })


@require_http_methods(["GET"])
def closedlistings(request):
    auctions = Auction.objects.filter(is_active=False)
    return render(request, "auctions/closedlistings.html", {
        'auctions' : auctions
    })


@require_http_methods(["GET"])
def getlisting(request, name):

    auction = Auction.objects.get(name=name)
    comments = auction.comments.all()

    # if it's a user,
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        if auction in watchlist:
            added = True
        else:
            added = False
        return render(request, "auctions/listing.html", {
            "auction" : auction,
            "comments" : comments,
            "added" : added,
            "comment" : CommentForm()
        })
        
    # if it's a visitor, listing should be only viewable
    else:
        return render(request, "auctions/listing.html", {
        "auction" : auction,
        "comments" : comments
        })
        


@require_http_methods(["POST"])
@login_required
def placebid(request, name):

    name = request.POST["name"]
    auction = Auction.objects.get(name=name)
    comments = auction.comments.all()
    bid = float(request.POST["bid"])
    current_price = auction.starting_bid
    #if a bid is placed and bid is higher than starting bid,save bid, else show error message#
     
    if auction.bids_count >= 1:
        current_price = auction.highest_bid().bidding_price
    
    if bid > current_price:
        bidding = Bid(auction=auction, bidding_user=request.user, bidding_price=bid)
        bidding.save()
        auction.bids_count += 1
        auction.save()
        return render(request, "auctions/listing.html", {
            "auction": auction,
            "comments": comments
        })
    else:
        error_message = "Your bid must be higher than the current highest bid."
        return render(request, "auctions/listing.html", {
            "error_message": error_message, 
            "auction": auction,                
            "comments": comments
        })


@require_http_methods(["POST"])
@login_required
def closelisting(request, name):
    name = request.POST["close_auction"]
    auction = Auction.objects.get(name=name)
    comments = auction.comments.all()

    #if auction owner closes the bid, listing is no longer active highest bidder becomes the winner, return closed listings page
    auction.is_active = False
    if auction.bids_count >= 1:
        bidding_winner = auction.highest_bid().bidding_user
        auction.winner = bidding_winner.username
    else:
        auction.winner = ""
    auction.save()
    auctions = Auction.objects.filter(is_active=False)
    return render(request, "auctions/closedlistings.html", {
        'auctions' : auctions,
        'comments' : comments
    })


@require_http_methods(["POST"])
@login_required
def comment(request, name):
    auction = Auction.objects.get(name=name)
    
    # if a comment is added, save the comment and return listing
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(
                commentor=request.user,
                auction=auction,
                **form.cleaned_data
            )
        comment.auction = auction  # Assign the auction object to the comment's auction field since form does not contain those
        comment.commentor = request.user
        comment.save()
        comments = auction.comments.all()
        return render(request, "auctions/listing.html", { 
            "auction": auction,                
            "comments": comments,
            "comment" : CommentForm()
        })
    else:
        # Form is not valid, handle the error case
        return HttpResponseRedirect(reverse("getlisting", args=(auction.name,)))


@require_http_methods(["GET","POST"])
@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()

    # add or remove from watchlist
    if request.method == "POST":
        auction_name = request.POST["name"]
        method = request.POST["add/remove"]
        auction = Auction.objects.get(name=auction_name)
        
        # adding an auction to watchlist
        if method == "add":
            request.user.watchlist.add(auction)
        # removing an auction from watchlist
        elif method == "remove":
            request.user.watchlist.remove(auction)
        return HttpResponseRedirect(reverse("watchlist"))

    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })


@require_http_methods(["GET"])
def categories(request):
    categories_types = Auction.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories_types
    })


@require_http_methods(["GET"])
def category(request, category_type):
    category_list = Auction.objects.filter(category=category_type, is_active=True)
    return render(request, "auctions/category.html", {
        "category_list": category_list,
        "category_type": category_type
    })
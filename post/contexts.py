import datetime

from account.models import Profile
from post.models import Post


def main_context(request):
    active_users = Profile.objects.filter(week_posts_count__gt=0).order_by('-week_posts_count')[:7]

    today = datetime.date.today()
    month = today - datetime.timedelta(days=30)
    hot_posts = Post.objects.filter(active=True, created_on__gt=month). \
                    filter(like_count__gt=4).order_by('-like_count')[:7]

    random_posts = Post.objects.filter(text__regex=r'.{100}.*').order_by('?')[:7]

    return {'active_users': active_users, 'hot_posts': hot_posts, 'random_posts': random_posts}

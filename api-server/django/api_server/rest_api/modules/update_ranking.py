from rest_api.models import User


# 전체 user의 ranking 갱신
def update_ranking():
    users = User.objects.order_by('-best_score')
    for rank, user in enumerate(users, start=1):
        user.ranking = rank
        user.save()

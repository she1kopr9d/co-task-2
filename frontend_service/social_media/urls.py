import django.urls

import social_media.views.info
import social_media.views.profile


urlpatterns = [
    django.urls.path(
        "feed/",
        social_media.views.info.feed_view,
        name="feed",
    ),
    django.urls.path(
        "profile/create/",
        social_media.views.profile.CreateProfileView.as_view(),
        name="profile-create",
    ),
]

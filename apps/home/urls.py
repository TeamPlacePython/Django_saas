from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.index_view, name="home-index"),
    path(
        "member-role/<tenant_id>", views.tenant_member_role, name="member-role"
    ),
]

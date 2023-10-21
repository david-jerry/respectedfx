from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from config.sitemaps import StaticViewSitemap
from respectedfx.blog.views import PostDetailView, PostListView
from respectedfx.fxrates.views import create_fx_request, create_fx_local_request, create_internationa_transfer_request
from respectedfx.newsletter.views import apply_news_letter
sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("faq/", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),
    path("contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
    path("terms/", TemplateView.as_view(template_name="legal/terms_of_use.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="legal/privacy_policy.html"), name="privacy"),
    path("cookie/", TemplateView.as_view(template_name="legal/cookie_policy.html"), name="cookie"),
    path("blogs/", PostListView.as_view(), name="post_List"),
    path("blogs/<slug>/", PostDetailView.as_view(), name="post_Detail"),


    path('create_fx_request/', create_fx_request, name='create_fx_request'),
    path('create_fx_local_request/', create_fx_local_request, name='create_fx_local_request'),
    path('create_internationa_transfer_request/', create_internationa_transfer_request, name="create_internationa_transfer_request"),
    path('apply_news_letter/', apply_news_letter, name="apply_news_letter"),


    # Django Admin, use {% url 'admin:index' %}
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('backend/', include('admin_honeypot.urls', namespace='admin_backend_honeypot')),
    path('portal/', include('admin_honeypot.urls', namespace='admin_portal_honeypot')),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("respectedfx.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path('tinymce/', include('tinymce.urls')),
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

handler404 = 'admin_honeypot.views.handler404'

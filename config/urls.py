from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import ObtainTokenPairViewWithUserType
# from notes.views import Notes, PatientNotes


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/telePsycRxMeeting/', include('meetings.urls')),
    path('api/notes/', include('notes.urls')),
    path('api/telepsycrx_billing/', include('telepsycrx_billing.urls')),
    path('api/telepsycrx_hr/', include('telepsycrx_hr.urls')),
    path('api/telepsycrx_marketing/', include('telepsycrx_marketing.urls')),
    path('api/personal_journal/', include('personal_journal.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/token/', ObtainTokenPairViewWithUserType.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-auth/', include('rest_framework.urls')),
]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)),
urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

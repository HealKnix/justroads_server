from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from justroads.views import (
    DefectStatusViewSet,
    DefectViewSet,
    MarkViewSet,
    MarkAnnotationViewSet,
)

router = DefaultRouter()
router.register(r'defects', DefectViewSet)
router.register(r'defect-statuses', DefectStatusViewSet)
router.register(r'marks', MarkViewSet)
router.register(r'mark-annotations', MarkAnnotationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

"""Flow Binding API Views"""
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from authentik.flows.api.stages import StageSerializer
from authentik.flows.models import FlowStageBinding


class FlowStageBindingSerializer(ModelSerializer):
    """FlowStageBinding Serializer"""

    stage_obj = StageSerializer(read_only=True, source="stage")

    class Meta:

        model = FlowStageBinding
        fields = [
            "pk",
            "policybindingmodel_ptr_id",
            "target",
            "stage",
            "stage_obj",
            "evaluate_on_plan",
            "re_evaluate_policies",
            "order",
            "policies",
        ]


class FlowStageBindingViewSet(ModelViewSet):
    """FlowStageBinding Viewset"""

    queryset = FlowStageBinding.objects.all()
    serializer_class = FlowStageBindingSerializer
    filterset_fields = "__all__"

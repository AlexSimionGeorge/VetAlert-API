from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.TreatmentLog import TreatmentLog
from api.repository.TreatmentLogRepository import TreatmentLogRepository


class TreatmentLogView(APIView):
    def get(self, request, aid=None):
        uid = request.user.to_dict()['uid']

        if aid:
            treatment_logs = TreatmentLogRepository.get_treatment_log_for_animal(aid)
            return Response([tl.to_response() for tl in treatment_logs], status=status.HTTP_200_OK)
        else:
            treatment_logs = TreatmentLogRepository.find_by_veterinarian_id(uid)
            return Response([tl.to_response() for tl in treatment_logs], status=status.HTTP_200_OK)



    def post(self, request):
        uid = request.user.to_dict()['uid']
        try:
            data = request.data
            treatment_log = TreatmentLog.from_post_request(data)

            if not TreatmentLogRepository.is_valid_animal(treatment_log.animal, uid):
                return Response({"error": "Invalid or inaccessible animal ID."}, status=status.HTTP_400_BAD_REQUEST)
            if not TreatmentLogRepository.is_valid_item(treatment_log.item, uid):
                return Response({"error": "Invalid or inaccessible item ID."}, status=status.HTTP_400_BAD_REQUEST)

            treatment_log = TreatmentLogRepository.add_treatment_log(treatment_log)
            return Response(treatment_log.to_response(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, tlid):
        uid = request.user.to_dict()['uid']

        try:
            data = request.data
            new_treatment_log = TreatmentLog.from_post_request(data)

            if not TreatmentLogRepository.is_valid_animal(new_treatment_log.animal, uid):
                return Response({"error": "Invalid or inaccessible animal ID."}, status=status.HTTP_400_BAD_REQUEST)
            if not TreatmentLogRepository.is_valid_item(new_treatment_log.item, uid):
                return Response({"error": "Invalid or inaccessible item ID."}, status=status.HTTP_400_BAD_REQUEST)

            old_treatment_log = TreatmentLogRepository.get_treatment_log(tlid)
            if not old_treatment_log:
                return Response({"error": "Treatment log not found."}, status=status.HTTP_404_NOT_FOUND)

            TreatmentLogRepository.update_treatment_log(tlid, new_treatment_log)
            return Response(new_treatment_log.to_response(), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tlid):
        uid = request.user.to_dict()['uid']

        try:
            treatment_log = TreatmentLogRepository.get_treatment_log(tlid)
            if not treatment_log:
                return Response({"error": "Treatment log not found."}, status=status.HTTP_404_NOT_FOUND)

            if not TreatmentLogRepository.is_valid_animal(treatment_log.animal, uid) or not TreatmentLogRepository.is_valid_item(treatment_log.item, uid):
                return Response({"error": "You can't delete treatment logs for animals/items that aren't yours."},
                                status=status.HTTP_403_FORBIDDEN)

            TreatmentLogRepository.delete_treatment_log(tlid)
            return Response({"message": "Treatment log deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

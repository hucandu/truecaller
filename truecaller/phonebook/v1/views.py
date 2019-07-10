
from rest_framework.views import APIView
from phonebook.v1.response import StandardResponse
from phonebook.v1.services.search_service import SearchService
from phonebook.v1.services.spam_service import NumberSpamService
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SearchView(APIView):
    """
    Deals with searching and sorting of results based on query params.
    user needs to be authenticated to perform this task
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        name = request.query_params.get('name')
        phone_number = request.query_params.get('phone_number')
        standard_response = StandardResponse()

        if name and phone_number:
            return Response(standard_response.failed_response(400, "cannot search name and phone at once"), status=400)

        search_service = SearchService()
        if name:
            result_list_name = search_service.search_by_name(name)
            response_data = []
            if result_list_name:
                response_data = list(
                    map(lambda x: x.get_profile, result_list_name))
            return Response(standard_response.success_response(response_data), status=200)

        if phone_number:
            result_list_phone = search_service.search_by_phone(phone_number)
            response_data = []
            if result_list_phone:
                response_data = list(
                    map(lambda x: x.get_profile, result_list_phone))
            return Response(standard_response.success_response(response_data), status=200)

        return Response(standard_response.failed_response(403, "No query params provided to search"), status=403)


class MarkSpamView(APIView):
    """
    Mark a number as spam
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        standard_response = StandardResponse()
        phone = request.data.get("phone_number")
        if phone:
            numberspamservice = NumberSpamService.mark_given_number_as_spam(
                user, phone)
            if numberspamservice:
                return Response(standard_response.success_response())

        return Response(standard_response.failed_response(403,reason="No phone numbers were given"), status=403)

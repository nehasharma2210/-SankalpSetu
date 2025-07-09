import sys
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .mentor_utils import process_mentor_chat
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mentor_chatbot(request):
    print("RAW BODY:", request.body, file=sys.stderr)
    print("HEADERS:", request.headers, file=sys.stderr)
    query = request.data.get("query")

    if not query:
        return Response({"error": "Message is required."}, status=400)

    result = process_mentor_chat(query)
    return Response({"response": result})

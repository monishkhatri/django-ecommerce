from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getProductData(request):
    person = {'name' : 'Webster', 'ager' : 42}
    return Response(person)

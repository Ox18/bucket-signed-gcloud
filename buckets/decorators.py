import jwt
from django.http import JsonResponse
from functools import wraps
from buckets.settings import JWT_SECRET

def jwt_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)

        token = auth_header.split(" ")[1]
        try:
            # Decodifica el JWT
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = payload  # Almacena el usuario o datos en el objeto request
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Si el token es válido, procede con la vista
        return view_func(request, *args, **kwargs)

    return wrapped_view

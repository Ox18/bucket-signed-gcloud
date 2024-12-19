import jwt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from buckets.decorators import jwt_required
from buckets.gcloud import generate_signed_url
from buckets.settings import JWT_SECRET
import os

@csrf_exempt  # Desactiva temporalmente la protección CSRF para pruebas
def login(request):
    if request.method == "POST":
        try:
            # Leer los datos enviados como JSON
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            # Validar las credenciales
            if username == "admin" and password == "admin":
                payload = {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expira en 1 hora
                }
                token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

                # Devolver el token en formato JSON
                return JsonResponse({"token": token}, status=200)
            else:
                # Credenciales inválidas
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            # Error al decodificar el JSON
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        # Método no permitido
        return JsonResponse({"error": "Method not allowed"}, status=405)


@jwt_required
def verify(request):
    return JsonResponse({"success": True}, status=200)

@jwt_required
def signedUrl(request):
    if (request.method == "POST"):
        data = json.loads(request.body)
        filename = data.get("filename")

        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual del archivo views.py
        service_account_file = os.path.join(base_dir, "../service-account-key.json")  # Ajustar según la ubicación real

        signedUrl = generate_signed_url(service_account_file, "conauti-bucket", filename)

        return JsonResponse({"signedUrl": signedUrl}, status=200)
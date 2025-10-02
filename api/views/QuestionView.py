from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from api.repository.ItemRepository import ItemRepository
import os

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
MODEL_NAME = "mistral"


class QuestionView(APIView):
    def post(self, request):
        try:
            uid = request.user.to_dict()['uid']
            data = request.data

            question = data.get("question")
            if not question:
                return Response({"error": "Missing 'question' field"}, status=status.HTTP_400_BAD_REQUEST)

            # 1. Preluăm medicamentele userului curent
            items = ItemRepository.find_by_veterinarian_id(uid)
            if not items:
                return Response({"error": "No items found for this user"}, status=status.HTTP_404_NOT_FOUND)

            # 2. Construim contextul din medicamente
            context_lines = []
            for item in items:
                line = f"- {item.name} (cod {item.code_number}, expira {item.expiration_date}): {item.notes or 'fara notite'}"
                context_lines.append(line)

            context = "\n".join(context_lines)

            # 3. Construim promptul pentru LLM
            prompt = f"""
Avem următoarele medicamente disponibile în cabinet:
{context}

Întrebare: {question}

Răspunde care medicament este cel mai potrivit și explică de ce, pe baza descrierilor de mai sus.
"""

            # 4. Apelăm Ollama API
            payload = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(OLLAMA_API_URL, json=payload)
            if response.status_code != 200:
                return Response({"error": "LLM service error", "details": response.text}, status=500)

            llm_output = response.json().get("response", "").strip()

            # 5. Returnăm răspunsul ca JSON
            return Response({"response": llm_output}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

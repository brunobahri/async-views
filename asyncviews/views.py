import asyncio
import httpx
from django.http import JsonResponse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("http://127.0.0.1:8000/api/")
        print(r)


@csrf_exempt
async def print_sum(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            num1 = data.get('num1')
            num2 = data.get('num2')
            sum_result = num1 + num2
            print(f"Soma resultante: {sum_result}")
            return JsonResponse({"result": sum_result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)


async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())

    html_content = """
    <html>
    <body>
        <h2>Soma de Dois Números</h2>
        <input id="num1" type="number" placeholder="Número 1">
        <input id="num2" type="number" placeholder="Número 2">
        <button onclick="sumNumbers()">Somar</button>
        <p id="result"></p>
        <script>
            async function sumNumbers() {
                var num1 = parseInt(document.getElementById('num1').value);
                var num2 = parseInt(document.getElementById('num2').value);
                const response = await fetch('/print-sum/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({num1: num1, num2: num2}),
                });
                const data = await response.json();
                console.log("Resultado enviado ao servidor: " + data.result); // Isto será impresso no console do navegador
                document.getElementById('result').textContent = "Resultado: " + data.result;}
        </script>
    </body>
    </html> 
    """
    return HttpResponse(html_content)






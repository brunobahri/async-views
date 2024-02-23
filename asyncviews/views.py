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
async def calculate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            operation = data.get('operation')
            num1 = data.get('num1')
            num2 = data.get('num2')

            if operation == 'sum':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                result = num1 / num2 if num2 != 0 else 'Erro: Divisão por zero'
            else:
                return JsonResponse({"error": "Operação não suportada"}, status=400)

            print(f"{operation}: {result}")
            return JsonResponse({"result": str(result)})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)


async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())

    html_content = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Operações</title>
    <script>
        async function performOperation() {
            var num1 = parseInt(document.getElementById('num1').value);
            var num2 = parseInt(document.getElementById('num2').value);
            var operation = document.getElementById('operation').value;

            try {
                const response = await fetch('/calculate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({operation: operation, num1: num1, num2: num2}),
                });
                const data = await response.json();
                if (data.result) {
                    console.log("Resultado enviado ao servidor: " + data.result); 
                    document.getElementById('result').textContent = "Resultado: " + data.result; 
                } else {
                    console.error("Erro: " + data.error);
                    document.getElementById('result').textContent = "Erro: " + data.error; 
                }
            } catch (error) {
                console.error("Erro ao enviar solicitação: ", error);
                document.getElementById('result').textContent = "Erro ao enviar solicitação: " + error; 
            }
        }
    </script>
</head>
<body>
    <h2>Operações</h2>
    <input id="num1" type="number" placeholder="Número 1">
    <input id="num2" type="number" placeholder="Número 2">
    <select id="operation">
        <option value="sum">Soma</option>
        <option value="subtract">Subtração</option>
        <option value="multiply">Multiplicação</option>
        <option value="divide">Divisão</option>
    </select>
    <button onclick="performOperation()">Calcular</button>
    <div id="result"></div> <!-- Local para exibir o resultado -->
</body>
</html>
    """
    return HttpResponse(html_content)






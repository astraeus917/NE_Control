import csv
import io
from django.shortcuts import render, redirect
from .models import NoteNE, Responsible

def list(request):
    return render(request, 'ne_control/list.html')

def show(request):
    return render(request, 'ne_control/show.html')

def index(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith(".csv"):
            return render(request, "ne_control/index.html", {"error": "Arquivo inválido."})

        # Leitura do CSV
        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        for row in reader:
            # Busca ou cria o responsável
            responsavel_nome = row["responsavel"].strip()
            responsavel_obj, _ = Responsible.objects.get_or_create(name=responsavel_nome)

            # Atualiza ou cria a NoteNE
            NoteNE.objects.update_or_create(
                cod_ne=row["cod_ne"],
                defaults={
                    "ug": int(row["ug"]),
                    "pi": float(row["pi"]),
                    "nd": int(row["nd"]),
                    "dias": int(row["dias"]),
                    "a_liquidar": row["a_liquidar"].replace(",", "."),
                    "liquidado_pagar": row["liquidado_pagar"].replace(",", "."),
                    "total_pagar": row["total_pagar"].replace(",", "."),
                    "pago": row["pago"].replace(",", "."),
                    "responsavel": responsavel_obj,
                    "data_contato": row["data_contato"],  # deve estar no formato YYYY-MM-DD
                }
            )

        return redirect("list")  # redireciona após sucesso

    return render(request, "ne_control/index.html")




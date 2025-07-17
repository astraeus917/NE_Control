import csv
import io
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import NoteNE
from decimal import Decimal

def parse_brl(value):
    """Converte valor em formato brasileiro para Decimal."""
    return Decimal(value.replace(".", "").replace(",", "."))


@login_required
def list(request):
    notes_ne = NoteNE.objects.all()
    return render(request, 'ne_control/list.html', {'notes_ne': notes_ne})


@login_required
def show(request):
    return render(request, 'ne_control/show.html')


@login_required
def index(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # Verifica se um arquivo .csv foi anexado para importação.
        if not csv_file.name.endswith(".csv"):
            return render(request, "ne_control/index.html", {"error": "Arquivo inválido."})

        # Faz a leitura do .csv para importar pro Banco de Dados.
        decoded_file = csv_file.read().decode("utf-8-sig")
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        for row in reader:
            # Codigo para buscar o responsavel no csv.
            # responsavel_nome = row["responsavel"].strip()

            # responsavel_name = 'Gestão'
            # Ele busca o responsavel no Banco de Dados e cria se não existir.
            # responsavel_obj, _ = Responsible.objects.get_or_create(name=responsavel_name)

            # Atualiza ou cria a NE.
            # Verificar necessidade de apagar NE se ela estiver fora do csv.
            NoteNE.objects.update_or_create(
                cod_ne=row["NE"],
                defaults={
                    "ug": int(row["UG"]),
                    "pi": row["PI"],
                    "nd": int(row["ND"]),
                    "dias": int(row["DIAS"]),
                    "a_liquidar": parse_brl(row["A LIQUIDAR"]),
                    "liquidado_pagar": parse_brl(row["LIQUIDADO A PAGAR"]),
                    "total_pagar": parse_brl(row["TOTAL A PAGAR"]),
                    "pago": parse_brl(row["PAGO"]),
                    "responsavel": None,
                    "data_contato": row["DATA"], # esta como CharField e não como DataField.
                }
            )

        return redirect("list")  # Redireciona para a lista de NEs.

    return render(request, "ne_control/index.html")




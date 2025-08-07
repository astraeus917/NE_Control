import csv
import io
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import NoteNE, ActionTaken, Claim
from .forms import ActionTakenForm
from decimal import Decimal

User = get_user_model()

def parse_brl(value):
    """Converte valor em formato brasileiro para Decimal."""
    return Decimal(value.replace(".", "").replace(",", "."))

@login_required
def general_list(request):
    notes_ne = NoteNE.objects.filter(responsavel__isnull=True)

    if request.method == 'POST':
        cod_ne = request.POST.get('cod_ne')

        try:
            user = request.user
            note_ne = NoteNE.objects.get(pk=cod_ne)

            # verifica se ja não existe uma solicitação pendente.
            if Claim.objects.filter(user=user, cod_ne=note_ne, status=True).exists():
                messages.warning(request, "Já existe uma solicitação para reivindicar essa NE.")

            else:
                Claim.objects.create(user=user, cod_ne=note_ne)
                messages.success(request, "Reivindicação enviada com sucesso!")

        except Exception as error:
            messages.error(request, f"Erro ao reivindicar! {str(error)}")

    return render(request, 'ne_control/general_list.html', {'notes_ne': notes_ne})

@login_required
def list(request):
    notes_ne = NoteNE.objects.filter(responsavel=request.user).prefetch_related('actions_taken')
    return render(request, 'ne_control/list.html', {'notes_ne': notes_ne})


@login_required
def show(request, pk):
    note_ne = get_object_or_404(NoteNE, pk=pk)

    # tbm pode ser usado related_name, para um codigo mais reutilizavel e organizado, porem sem tanto controle.
    action_taken = ActionTaken.objects.filter(cod_ne=note_ne)

    if request.method == 'POST':
        form = ActionTakenForm(request.POST)
        if form.is_valid():
            cod_ne = note_ne
            date = form.cleaned_data['date']
            responsible = request.user
            previ_date = form.cleaned_data['previ_date']
            description = form.cleaned_data['description']

            ActionTaken.objects.create(
                cod_ne=cod_ne,
                date=date,
                responsible=responsible,
                previ_date=previ_date,
                description=description
            )

            messages.success(request, "Nova medida registrada com sucesso!")
            return redirect('show', pk=pk)

        else:
            messages.error(request, "Erro ao cadastrar medida!")

    else:
        form = ActionTakenForm()

    return render(request, 'ne_control/show.html', {'note_ne': note_ne, 'action_taken': action_taken, 'form': form})


@login_required
def manage(request):
    if not request.user.role == 'admin':
        raise PermissionDenied

    if request.method == 'POST' and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # Verifica se um arquivo .csv foi anexado para importação.
        if not csv_file.name.endswith(".csv"):
            return render(request, "ne_control/import.html", {"error": "Arquivo inválido."})

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

        return redirect("list")  # redireciona para a lista de NEs.

    return render(request, "ne_control/manage.html")




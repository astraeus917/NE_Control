import csv
import io
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import NoteNE, ActionTaken, Claim
from .forms import ActionTakenForm
from decimal import Decimal
from datetime import datetime

# Seta o User do get_user_model, por conta de ser um modelo personalizado.
User = get_user_model()

# Função para verificar se usuário é ativo.
def is_user_active(user):
    return user.is_active


def parse_brl(value):
    """Converte valor em formato brasileiro para Decimal."""
    return Decimal(value.replace(".", "").replace(",", "."))


@user_passes_test(is_user_active)
@login_required
def list(request):
    # Busca informações no banco de dados para o contexto.
    notes_ne = NoteNE.objects.filter(responsavel__isnull=True)
    context = {
        'notes_ne': notes_ne
    }

    if request.method == 'POST':
        cod_ne = request.POST.get('cod_ne')

        try:
            user = request.user
            note_ne = NoteNE.objects.get(pk=cod_ne)

            # verifica se ja não existe uma solicitação pendente.
            if Claim.objects.filter(user=user, cod_ne=note_ne, status=True).exists():
                messages.warning(request, "Aguardando autorização do Gestor!")
                return redirect('list')

            else:
                Claim.objects.create(user=user, cod_ne=note_ne)
                messages.success(request, f"{note_ne} Reivindicada com sucesso!")
                return redirect('list')

        except Exception as error:
            messages.error(request, f"Erro ao reivindicar! {str(error)}")
            return redirect('list')

    return render(request, 'ne_control/list.html', context)


@user_passes_test(is_user_active)
@login_required
def control(request):
    notes_ne = NoteNE.objects.filter(responsavel=request.user).prefetch_related('actions_taken')
    context = {
        'notes_ne': notes_ne,
        'active_page': 'control'
    }
    
    return render(request, 'ne_control/control.html', context)


@user_passes_test(is_user_active)
@login_required
def show(request, pk):
    # Busca informações no Banco de Dados para passar no contexto.
    form = ActionTakenForm()
    note_ne = get_object_or_404(NoteNE, pk=pk)
    action_taken = ActionTaken.objects.filter(cod_ne=note_ne)

    context = {
        'form': form,
        'note_ne': note_ne,
        'action_taken': action_taken
    }

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
            messages.error(request, "Erro ao registrar medida!")
            return redirect('show')

    return render(request, 'ne_control/show.html', context)


@user_passes_test(is_user_active)
@login_required
def manage(request):
    # Informações necessarias para passar no contexto.
    claim_list = Claim.objects.filter(status=True)
    user_list = User.objects.filter(is_active=False)

    # Contagem de usuarios e claims.
    user_count = user_list.count()
    claim_count = claim_list.count()
    
    context = {
        'claim_list': claim_list,
        'user_list': user_list,
        'claim_count': claim_count,
        'user_count': user_count
    }

    if not request.user.role == 'admin':
        raise PermissionDenied
    
    if request.method == 'POST':
        # Trata o formulario de importação do CSV.
        if request.POST.get('form_type') == 'form1' and request.FILES.get("csv_file"):
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

                # Converter a data para salvar no banco de dados.
                data_csv = row['DATA']
                data_for_db = datetime.strptime(data_csv, "%d/%m/%y").date()

                NoteNE.objects.update_or_create(
                    cod_ne=row["NE"],
                    defaults={
                        "ug": int(row["UG"]),
                        "pi": row["PI"],
                        "nd": int(row["ND"]),
                        "data": data_for_db,
                        "a_liquidar": parse_brl(row["A LIQUIDAR"]),
                        "liquidado_pagar": parse_brl(row["LIQUIDADO A PAGAR"]),
                        "total_pagar": parse_brl(row["TOTAL A PAGAR"]),
                        "pago": parse_brl(row["PAGO"]),
                        "responsavel": None,
                    }
                )
            messages.success(request, "Importação concluída com sucesso!")
            return redirect('manage')

            # return redirect("list")  # redireciona para a lista de NEs.

        # Trata o formulario de confirmação de reivindicação.
        elif request.POST.get('form_type') == 'form2':
            cod_ne = request.POST.get('cod_ne')
            claim_id = request.POST.get('claim_id')

            claim = get_object_or_404(Claim, id=claim_id)

            try:
                note_ne = NoteNE.objects.get(pk=cod_ne)

                note_ne.responsavel = claim.user
                note_ne.save()

                claim.status = False
                claim.save()

                messages.success(request, "Solicitação autorizada!")
                return redirect('manage')

            except Exception as error:
                messages.error(request, error)
                return redirect('manage')

        # Negar a solicitação.
        elif request.POST.get('form_type') == 'form3':
            claim_id = request.POST.get('claim_id')
            claim = get_object_or_404(Claim, id=claim_id)

            try:
                claim.status = False
                claim.save()
                messages.warning(request, "Solicitação negada!")
                return redirect('manage')

            except Exception as error:
                messages.error(request, error)
                return redirect('manage')

        # Autorizar usuario.
        elif request.POST.get('form_type') == 'form4':
            user_id = request.POST.get('user_id')

            try:
                user = User.objects.get(pk=user_id)
                user.is_active = True
                user.save()
                messages.success(request, f"Usuário {user} autorizado!")
                return redirect('manage')

            except Exception as error:
                messages.error(request, error)
                return redirect('manage')


        # Negar usuario.
        elif request.POST.get('form_type') == 'form5':
            user_id = request.POST.get('user_id')

            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                messages.success(request, f"Usuário {user} negado e deletado!")
                return redirect('manage')

            except Exception as error:
                messages.error(request, error)
                return redirect('manage')

    return render(request, "ne_control/manage.html", context)




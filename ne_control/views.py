import csv
import io
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import NoteNE, ActionTaken, Claim
from accounts.models import Workplace
from .forms import ActionTakenForm
from decimal import Decimal
from datetime import datetime

# Seta o User do get_user_model, por conta de ser um modelo personalizado.
User = get_user_model()

# Função para verificar se usuário é ativo.
def is_user_active(user):
    return user.is_authenticated and user.is_active


def parse_brl(value):
    """Converte valor em formato brasileiro para Decimal."""
    return Decimal(value.replace(".", "").replace(",", "."))


@user_passes_test(is_user_active, login_url='login')
def list(request):
    # Busca informações no banco de dados para o contexto.
    notes_ne = NoteNE.objects.filter(responsavel__isnull=True)
    users = User.objects.filter(is_active=True)
    context = {
        'notes_ne': notes_ne,
        'active_page': 'list',
        'users': users
    }

    if request.method == 'POST':
        cod_ne = request.POST.get('cod_ne')
        pi = request.POST.get('pi')
        btn_action = request.POST.get('btn_action')
        note_ne = NoteNE.objects.get(pk=cod_ne)

        if btn_action == 'delegar':
            try:
                # Pega o id do usuario selecionado.
                responsible_id = request.POST.get('responsible')
                if responsible_id == 'none':
                    messages.warning(request, "Você precisar selecionar um responsável")
                
                else:
                    responsible = User.objects.get(id=responsible_id)
                    note_ne = NoteNE.objects.get(pk=cod_ne)
                    note_ne.responsavel = responsible
                    note_ne.save()
                    messages.success(request, "NE delegada com sucesso!")

            except Exception as error:
                messages.error(request, "Erro ao delegar NE!")

        else:
            try:
                # Pega o username do usuario que solicitou a reivindicação.
                user = request.user

                # verifica se ja não existe uma solicitação pendente.
                if Claim.objects.filter(user=user, cod_ne=note_ne, pi=pi, status=True).exists():
                    messages.warning(request, "Aguardando autorização do Gestor!")
                    return redirect('list')

                else:
                    Claim.objects.create(user=user, cod_ne=note_ne, pi=pi)
                    messages.success(request, f"{note_ne} Reivindicada com sucesso!")
                    return redirect('list')

            except Exception as error:
                messages.error(request, f"Erro ao reivindicar! {str(error)}")
                return redirect('list')

    return render(request, 'ne_control/list.html', context)


@user_passes_test(is_user_active, login_url='login')
def control(request):
    if request.user.role == 'admin':
        notes_ne = NoteNE.objects.filter(responsavel__isnull=False).prefetch_related('actions_taken')
    else:
        notes_ne = NoteNE.objects.filter(responsavel=request.user).prefetch_related('actions_taken')
    
    context = {
        'notes_ne': notes_ne,
        'active_page': 'control'
    }
    
    return render(request, 'ne_control/control.html', context)


@user_passes_test(is_user_active, login_url='login')
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


@user_passes_test(is_user_active, login_url='login')
def manage(request):
    # Informações necessarias para passar no contexto.
    claim_list = Claim.objects.filter(status=True)
    user_list = User.objects.filter(is_active=False)

    # Contagem de usuarios e claims.
    user_count = user_list.count()
    claim_count = claim_list.count()

    # Usuários ativos e Seções.
    users = User.objects.filter(is_active=True)
    workplaces = Workplace.objects.all()
    
    context = {
        'claim_list': claim_list,
        'user_list': user_list,
        'claim_count': claim_count,
        'user_count': user_count,
        'users': users,
        'workplaces': workplaces,
        'active_page': 'manage'

    }

    if not request.user.role == 'admin':
        raise PermissionDenied
    
    if request.method == 'POST':
        # Trata o formulario de importação do CSV.
        if request.POST.get('form_type') == 'form1' and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            # Faz a leitura do .csv para importar pro Banco de Dados.
            print(">>> TYPE REQUEST:", type(request))
            decoded_file = csv_file.read().decode("utf-8-sig")
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            # Lista das NEs do csv.
            csv_ne_list = []

            for row in reader:
                required_fields = ["UG", "PI", "ND", "NE", "DATA", "A LIQUIDAR", "LIQUIDADO A PAGAR", "TOTAL A PAGAR", "PAGO"]

                # Pula linhas que não são dados reais de NE (como a linha de totais)
                if not row.get("NE") or row["NE"].startswith("Σ") or row["NE"].strip() == "NE":
                    continue

                if not all(row.get(field) and row[field].strip() for field in required_fields):
                    messages.error(request, "Faltam ou contêm campos errados no .csv!")
                    return redirect('manage')

                csv_ne_list.append(row['NE']) # Adiciona na lista, para dps comparar e deletar NEs antigas.

                data_csv = row['DATA']
                data_for_db = datetime.strptime(data_csv, "%d/%m/%y").date()

                note, created = NoteNE.objects.update_or_create(
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
                    }
                )

                # Se a NE for criada agora, o usuário é Null.
                if created:
                    note.responsavel = None
                    note.save()

            NoteNE.objects.exclude(cod_ne__in=csv_ne_list).delete()

            messages.success(request, "Importação concluída com sucesso!")
            return redirect('manage')

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
        
        # Adicionar nova seção.
        elif request.POST.get('form_type') == 'form6':
            workplace = request.POST.get('workplace')

            workplace, created = Workplace.objects.get_or_create(
                workplace = workplace
            )

            if created:
                messages.success(request, "Seção criada com sucesso!")
                return redirect('manage')
            
            else:
                messages.error(request, "Essa seção já existe!")
                return redirect('manage')

        # Deletar usuário do sistema.
        elif request.POST.get('form_type') == 'form7':
            user_id = request.POST.get('user_id')

            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                messages.success(request, "Usuário deletado com sucesso!")
                return redirect('manage')

            except Exception as error:
                messages.error(request, "Erro ao deletar usuário!")
                return redirect('manage')
            
        # Deletar seção do sistema.
        elif request.POST.get('form_type') == 'form8':
            workplace_id = request.POST.get('workplace_id')

            try:
                workplace = Workplace.objects.get(pk=workplace_id)
                workplace.delete()
                messages.success(request, "Seção deletada com sucesso!")
                return redirect('manage')

            except Exception as error:
                messages.error(request, "Erro ao deletar seção!")
                return redirect('manage')

    return render(request, "ne_control/manage.html", context)

@user_passes_test(is_user_active, login_url='login')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    workplaces = Workplace.objects.all()
    roles = User.ROLE_CHOICES

    context = {
        'user': user,
        'workplaces': workplaces,
        'roles': roles,
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        workplace_id = request.POST.get('workplace')

        try:
            user.username = username
            if password != '':
                user.set_password(password)
            user.role = role
            if workplace_id:
                user.workplace = get_object_or_404(Workplace, pk=workplace_id)
            user.save()

            messages.success(request, "Alterações salvas com sucesso!")
            return redirect('manage')
        
        except Exception as error:
            messages.error(request, "Não foi possível salvar as alterações!")
            return redirect('user-edit')
            
    return render(request, 'ne_control/user_edit.html', context)

@user_passes_test(is_user_active, login_url='login')
def workplace_edit(request, pk):
    workplace = get_object_or_404(Workplace, pk=pk)

    context = {
        'workplace': workplace,
    }

    if request.method == 'POST':
        workplace_name = request.POST.get('workplace')

        try:
            workplace.workplace = workplace_name
            workplace.save()

            messages.success(request, "Alterações salvas com sucesso!")
            return redirect('manage')
        
        except Exception as error:
            messages.error(request, "Não foi possível salvar as alterações!")
            return redirect('workplace-edit')
            
    return render(request, 'ne_control/workplace_edit.html', context)

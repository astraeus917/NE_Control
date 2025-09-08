# Sistema de Controle de Notas de Empenho

Este projeto é um sistema web desenvolvido com **Python**, **Django** e **Tailwind CSS**, com o objetivo de facilitar o controle e a gestão de **notas de empenho** dentro de uma organização militar.

## 📌 Sobre o Projeto

O sistema foi idealizado para atender às necessidades administrativas de setores responsáveis pela execução orçamentária, especialmente em ambientes militares. Seu foco principal é organizar, registrar e acompanhar as **notas de empenho** emitidas ao longo do exercício financeiro.

## 🧾 O que são Notas de Empenho?

A **nota de empenho** é um documento utilizado pela administração pública para reservar parte do orçamento com a finalidade de realizar determinada despesa. Trata-se de um compromisso formal da entidade pública com um fornecedor ou prestador de serviço, garantindo que existe dotação orçamentária suficiente para cobrir o valor empenhado.

Existem três tipos principais de empenho:
- **Empenho Ordinário:** para despesas que possam ser liquidadas de uma só vez.
- **Empenho Global:** utilizado para despesas com execução contínua (ex: contratos).
- **Empenho por Estimativa:** para despesas cujo valor exato não se conhece previamente.

## ⚙️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)**
- **[Django](https://www.djangoproject.com/)** – Framework web backend
- **[Tailwind CSS](https://tailwindcss.com/)** – Framework CSS utilitário

## 🚀 Funcionalidades

- Cadastro e consulta de notas de empenho
- Filtros por data, fornecedor, tipo de empenho, entre outros
- Histórico e status das notas
- Interface responsiva com Tailwind
- Sistema adaptado à rotina de organizações militares

## 🛠️ Instalação e Uso

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-projeto.git

2. Crie um ambiente virtual::
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Aplique as migrações:
    ```bash
    python manage.py migrate

5. Rode o servidor de desenvolvimento:
    ```bash
    python manage.py runserver

## 📄 Licença
Este projeto está sob a licença CC-BY-NC-SA-4.0 – veja o arquivo [CC-BY-NC-SA-4.0](CC-BY-NC-SA-4.0) para mais detalhes.

## 💻 Desenvolvedores
- **[Astraeus](https://github.com/astraeus917)** – Backend
- **[jhonathandelgado16](https://github.com/jhonathandelgado16)** – Frontend

## ⚠️ Atenção
O sistema já está em uso dentro da Organização Militar para a qual foi planejado. Estamos aguardando feedback dos usuários para futuras melhorias e ajustes. O projeto ainda não está em sua versão final e possui alguns bugs que serão corrigidos em breve. Agradecemos a atenção!

## Login
![Tela de login](./imgs/login.png)

## Register
![Tela de registro](./imgs/register.png)

## Action Taken
![Tela de ação tomada](./imgs/action-taken.png)

## Action Taken 1
![Tela de ação tomada 1](./imgs/action-taken-1.png)

## Admin NE Control
![Tela de controle de NEs (admin)](./imgs/admin-ne-control.png)

## Admin NE Control 1
![Tela de controle de NEs (admin) - variação 1](./imgs/admin-ne-control-1.png)

## Admin NE List
![Tela de lista de NEs (admin)](./imgs/admin-ne-list.png)

## Admin NE Manage
![Tela de gestão de NEs (admin)](./imgs/admin-ne-manage.png)

## Admin NE Manage 1
![Tela de gestão de NEs (admin) - variação 1](./imgs/admin-ne-manage-1.png)

## Admin NE Manage 2
![Tela de gestão de NEs (admin) - variação 2](./imgs/admin-ne-manage-2.png)

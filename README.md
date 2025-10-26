# To Do List - DataCake

Criei este projeto como uma proposta ao desafio lançado pela empresa DataCake, onde consegui estudar ao mesmo tempo que me desafiava. Obtive conhecimentos de: **Django + DRF** no backend e **React Native / Expo** no frontend. A proposta é simples, mas completa: autenticação segura baseada em cookies HTTPOnly e uma lista de tarefas com UI mobile pronta para rodar tanto em dispositivo físico quanto no emulador.

## O que vem no pacote

- **Autenticação** com cadastro, verificação por código, login persistente (cookies + refresh), recuperação de senha e logout seguro.
- **Gestão de tarefas** com CRUD, filtros por status/importância/data, alternância rápida de pendente/concluída e checklist.
- **Frontend** Expo pronto para Android/iOS/Web, incluindo centro de notificações in-app e tema claro/escuro.
- **Observabilidade** básica: logs estruturados no backend e tratamento padronizado de erros no app.

## Pré-requisitos do meu setup

Para reproduzir exatamente como executo aqui em casa, sigo estes requisitos mínimos:

| Ferramenta                           | Versão/Obs                                                        |
| ------------------------------------ | ----------------------------------------------------------------- |
| Python 3.12+                         | Instalo via `pyenv` (Linux/macOS) ou winget/ms-store (Windows)    |
| Pip + venv                           | Uso `python -m venv .venv` e mantenho `pip` atualizado            |
| Node.js 18+                          | Recomendo nvm ou volta; o projeto usa npm (incluído)              |
| npm 9+                               | Já vem com o Node 18                                              |
| Expo CLI / Expo Go                   | CLI vem via `npm install`, o app Expo Go precisa estar no celular |
| Android Studio + emulador (opcional) | Útil se não quiser usar um dispositivo físico                     |
| Docker 24+ (opcional)                | Só preciso quando quero rodar tudo containerizado                 |

> Dica: em dispositivos físicos eu sempre conecto PC e celular na mesma rede Wi-Fi. Quando isso não é possível, uso `npx expo start --tunnel` e exponho o backend com ngrok ou outro túnel.

## Passo a passo: backend do zero

1. **Clonar e configurar `.env`**

   ```bash
   cd backend
   cp .env.example .env
   ```

   Ajusto `SECRET_KEY`, `ALLOWED_HOSTS` (incluo o IP da minha máquina e `localhost`) e, se for expor para o celular, também adiciono o host em `CORS_ALLOWED_ORIGINS`.

2. **Criar e ativar o ambiente virtual**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # Linux/macOS
   pip install --upgrade pip
   pip install -r ../requirements.txt
   ```

3. **Rodar migrações**

   ```bash
   python manage.py migrate
   ```

4. **Popular dados de exemplo (opcional, mas eu gosto)**

   ```bash
   python manage.py seed
   ```

   Isso cria o usuário `demo` com senha `Demo@123!` e duas tarefas básicas.

5. **Subir o servidor**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   A API fica em `http://SEU_IP:8000/api/`. Se estiver rodando só no PC, `http://127.0.0.1:8000/api/` continua valendo.

## Passo a passo: frontend do zero

1. **Instalar dependências**

   ```bash
   cd frontend
   npm install
   ```

   Se o npm reclamar do Node, atualizo com `nvm use 18` (ou equivalente).

2. **Configurar a URL da API**

   - Em desenvolvimento costumo deixar o app descobrir automaticamente (ele usa o IP do Metro), **mas** quando uso túnel ou um backend remoto defino manualmente:

     ```bash
     # Windows PowerShell
     $env:EXPO_PUBLIC_API_URL="http://192.168.1.129:8000/api"

     # Linux/macOS
     export EXPO_PUBLIC_API_URL=http://192.168.1.129:8000/api
     ```
   - Se houver problemas ao tentar autenticar ou criar conta, possívelmente é a conexão com API. Verificar se API_URL está correta.
   - Para builds de produção/web sempre defino a variável antes de rodar `npm run build` (ou `npx expo export`).


3. **Start do Metro/Expo**

   ```bash
   npm run start
   ```

   Dentro do terminal uso as teclas:

   - `w` para abrir no navegador;
   - `a` para enviar para um emulador Android aberto;
   - `r` para dar reload;
   - `shift + r` para limpar cache.

4. **Rodar no dispositivo**
   - Instalo o app **Expo Go** (Google Play / App Store).
   - Escaneio o QR Code que aparece no terminal ou na interface web do Metro.
   - Se o celular não estiver na mesma rede, inicio o bundler com `npx expo start --tunnel` e exponho o backend com ngrok (`ngrok http 8000`). Basta apontar `EXPO_PUBLIC_API_URL` para a URL pública do ngrok.

## Migrações, dados e testes (resumo rápido)

| Ação                 | Comando                                  |
| -------------------- | ---------------------------------------- |
| Migrar banco         | `cd backend && python manage.py migrate` |
| Popular dados demo   | `python manage.py seed`                  |
| Criar superusuário   | `python manage.py createsuperuser`       |
| Rodar testes backend | `python manage.py test`                  |
| Lint frontend        | `cd frontend && npm run lint`            |

> Sempre que troco de branch ou atualizo dependências, repito `python manage.py migrate` e `npm install` para garantir que está tudo sincronizado.

## Fluxo completo que sigo em uma máquina nova

1. Instalo Python/Node (via gerenciador preferido) e o Expo Go no celular.
2. Clono o repositório, configuro `.env` do backend e rodo migrações + seeds.
3. Levanto o backend em `0.0.0.0:8000` para permitir acesso da rede.
4. Abro outra janela, instalo dependências do frontend e inicio `npm run start`.
5. Defino `EXPO_PUBLIC_API_URL` se necessário, escaneio o QR Code e valido login/cadastro/CRUD das tarefas.
6. Antes de commitar, executo `python manage.py test` e `npm run lint`.

## Usuários administrativos e contas de teste

- **Superusuário Django**: depois de ativar a venv e instalar as dependências (`pip install -r requirements.txt`), executo `python manage.py migrate` e em seguida `python manage.py createsuperuser`. Com o usuário criado, subo o backend ouvindo toda a rede local:
  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```
  Agora basta acessar `http://SEU_IP:8000/admin/` (ou `http://127.0.0.1:8000/admin/` na própria máquina) e logar com o superusuário recém-criado.
- **Conta demo via seed**: o comando `python manage.py seed` cria o usuário `demo` com senha `Demo@123!` e email `demo@datacake.local` e duas tarefas iniciais (uma pendente e outra concluída). Uso esse login tanto no backend (via API) quanto no app para validar rapidamente se tudo está funcionando.

## Execução com Docker (quando quero evitar instalar tudo)

1. Crio `backend/.env` (mesmo passo do ambiente local).
2. Exporto `EXPO_PUBLIC_API_URL=http://localhost:8000/api` para o processo que chamará o Compose.
3. Rodo:
   ```bash
   docker compose up --build
   ```
4. Endpoints expostos:
   - Backend: `http://localhost:8000/api/`
   - Expo Web: `http://localhost:19006/`

Hot reload funciona graças aos volumes montados, então dá para editar código localmente e ver o resultado dentro do container.

## Fluxos suportados (o que vale testar sempre)

- **Cadastro completo** → código enviado no console → verificação → login automático.
- **Login com cookies** → mantém sessão e renova access token sozinho.
- **Recuperar senha** → envio de código → valida policy forte → troca de senha.
- **CRUD de tarefas** → criação, filtros, alternar status, checklist e exclusão.

## Uso de IA

Durante este ciclo usei o Codex (GPT-5) para acelerar ajustes e documentação, mas reviso tudo manualmente antes de fechar qualquer tarefa.

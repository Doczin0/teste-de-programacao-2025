# Registro de Desenvolvimento
Será um relato em ordem cronológica, tentando detalhar e explicar e relembrar como foi realizada cada parte de modo mais direto e com menções pontuais a como o Codex me ajudou a acelerar algumas etapas.

1. **Planejamento e bootstrap**
   - Defini a arquitetura: Django + DRF para a API (com autenticação baseada em cookies HTTPOnly) e Expo/React Native para o app.  
   - Criei o repositório organizado em `backend/` e `frontend/`, configurei `.gitignore`, `.env.example` e as dependências básicas (venv, requirements, eslint, etc.).  
   - Subi os projetos iniciais (`django-admin startproject server`, `expo init todo-mobile`) e certifiquei-me de que ambos compilavam.

2. **Backend completo**
   - Modelei o app `todos`, criei migrations, serializers e viewsets para o CRUD, além de filtros e checklists.  
   - Implementei toda a jornada de autenticação: registro com verificação por código, login, refresh automático, logout e recuperação de senha.  
   - Escrevi o middleware `CookieToAuthorizationMiddleware`, os endpoints `/api/auth/*`, e um comando `python manage.py seed` para gerar usuário/tarefas demo.  
   - Configurei CORS/CSRF, logging estruturado e o uso de cookies HTTPOnly. O Codex me ajudou especialmente ao revisar as regras de validação e sugerir mensagens de erro mais claras.

3. **Frontend estruturado**
   - Montei a árvore de contextos (Auth, Theme, Notifications), criei componentes reutilizáveis e desenhei as telas de entrada (login, cadastro, verificação, recuperação) e a dashboard de tarefas.  
   - Configurei o React Navigation, o React Query, o centro de notificações e o tema com suporte a dark/light.  
   - Integrei o cliente Axios com interceptores e feedback visual consistente. O Codex serviu como “pair programmer” para prototipar rapidamente alguns layouts e ajustar microinterações.

4. **Integração e DX**
   - Escrevi o `src/api/client.js` com autodetecção de base URL (apoiada em `expo-constants`/`SourceCode.scriptURL`) e refresh automático de tokens.  
   - Fiz toda a cola entre o app e o backend, garantindo que os cookies fossem enviados corretamente (via `withCredentials`).  
   - Adicionei logs e notificações amigáveis para cada fluxo (cadastro, reset, falha de login, etc.).

5. **Polimento mobile**
   - Ao testar no Expo Go, surgiu o erro `crypto.getRandomValues() not supported`. Criei um polyfill em `src/polyfills/crypto.js` usando `expo-random` e passei a carregá-lo antes de qualquer outro import no `index.js`.  
   - Ajustei o resolver de host do Axios para evitar URLs do tipo `exp://…` — agora ele normaliza `debuggerHost`, `hostUri` e `scriptURL`, usando `globalThis.URL` quando houver suporte.  
   - Rodei `npm run lint` sempre que mexia no bundle. O Codex foi útil para validar os edge cases do polyfill e sugerir o fallback regex.

6. **Ambiente compartilhado**
   - Configurei o backend para aceitar dispositivos da rede local adicionando o IP da máquina em `ALLOWED_HOSTS` e `CORS_ALLOWED_ORIGINS`.  
   - Padronizei o `.env`, documentei como expor o backend com `runserver 0.0.0.0:8000` e dei dicas para quando for necessário usar túnel/ngrok.  
   - Validei com `python manage.py check` antes de seguir.

7. **Documentação final**
   - Reescrevi o `README.md` com um passo a passo completo: requisitos, setup, migrações, seeds, testes, iniciação do Expo e execução via Docker.  
   - Mantive este registro para contar a história do projeto e evidenciar onde o Codex entrou (diagnósticos rápidos, sugestões de validação e ajuda no wording).  
   - Finalizei fazendo uma última revisão geral para garantir que qualquer pessoa consiga seguir o mesmo caminho do zero.

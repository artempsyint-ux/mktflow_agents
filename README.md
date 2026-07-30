# Claude Code Skills — набор для студентов курса

27 готовых скиллов для Claude Code плюс подборка дизайн-документов по мульти-агентным паттернам (`concepts/`). Каждый скилл — папка с инструкцией `SKILL.md` и, где нужно, скриптами в `scripts/`.

## Как подключить

Скопируйте нужные папки в `.claude/skills/` внутри вашего проекта:

```bash
mkdir -p .claude/skills
cp -r <папка-скилла> .claude/skills/
```

Claude Code обнаружит скиллы автоматически и будет вызывать их по смыслу запроса.

API-ключи в скиллы не вшиты — каждый скилл читает их из `.env` вашего проекта (Apify, Instantly, OpenAI и т.д.). Заполняйте только те, которые нужны конкретному скиллу — список переменных указан в его `SKILL.md`.

## Состав

### Лидогенерация и обогащение
- `scrape-leads` — скрейпинг и верификация B2B-лидов через Apify, выгрузка в Google Sheets
- `gmaps-leads` — лиды из Google Maps с обогащением контактов с сайтов
- `classify-leads` — классификация лидов через LLM (например, продуктовый SaaS vs агентство)
- `casualize-names` — приведение формальных имён/названий к разговорным для персонализации

### Email и кампании
- `instantly-campaigns` — холодные email-кампании в Instantly с A/B-тестами
- `instantly-autoreply` — автоответы на входящие в Instantly по базе знаний
- `welcome-email` — welcome-цепочка для новых клиентов
- `gmail-inbox` — работа с несколькими Gmail-аккаунтами
- `gmail-label` — авторазметка входящих: Action Required / Waiting On / Reference

### Продажи и предложения
- `create-proposal` — коммерческие предложения в PandaDoc из брифа или транскрипта звонка
- `upwork-apply` — скрейпинг вакансий Upwork и персонализированные отклики
- `onboarding-kickoff` — автоматизация онбординга клиента после kickoff-звонка

### Контент и видео
- `video-edit` — удаление пауз в talking-head видео + 3D-переходы
- `pan-3d-transition` — 3D-эффекты панорамирования через Remotion
- `recreate-thumbnails` — генерация YouTube-обложек с заменой лица
- `youtube-outliers` — поиск «выстреливших» видео в своей нише
- `cross-niche-outliers` — виральные видео из смежных ниш для заимствования паттернов
- `title-variants` — варианты заголовков на основе анализа аутлаеров
- `reference-image-scraper-main` — сбор визуальных референсов с Pinterest/Behance

### Исследования
- `literature-research` — поиск по академическим базам (PubMed и др.)

### Инфраструктура
- `add-webhook` — добавление вебхуков Modal для событийного запуска
- `modal-deploy` — деплой скриптов в облако Modal
- `local-server` — локальный оркестратор с туннелем Cloudflare
- `generate-report` — пример скилла: PDF-отчёт о погоде через бесплатный API Open-Meteo

### Мульти-агентные скиллы (продвинутый уровень)
- `mcp-orchestrator` — Claude как менеджер: декомпозиция задачи и раздача подзадач воркерам, зарегистрированным как MCP-серверы (Codex, другие Claude, Gemini)
- `model-chat-skill` — мульти-агентные дебаты: N экземпляров Claude с разными ролями спорят в общей комнате и сходятся к решению
- `multi-agent-chrome-skill` — параллельная браузерная автоматизация: 1–5 агентов, у каждого свой Chrome через DevTools MCP

### `concepts/` — паттерны мульти-агентных систем (документы)
Не скиллы, а дизайн-документы: как проектировать мульти-агентные системы на Claude Code.
- `Agent Chatrooms.md` — общая комната для дебатов агентов
- `Multi-Agent MCP Orchestration.md` — оркестрация воркеров через MCP
- `Prompt Contracts.md` — контракты входа/выхода между агентами
- `Reverse Prompting.md` — агент сам формулирует уточняющие вопросы
- `Stochastic Multi-Agent Consensus.md` — консенсус N независимых прогонов
- `Subagent Verification Loops.md` — циклы проверки через субагентов
- `Video-to-Action via Gemini Passthrough.md` — извлечение действий из видео

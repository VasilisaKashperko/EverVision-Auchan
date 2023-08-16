<div align="center">
  <img src="https://github.com/VasilisaKashperko/EverVision-Auchan/assets/90206134/992efd5e-1b2b-4e94-bafc-11256fe98bcb" alt="EverVision">
</div>

# Инструкция по запуску

Данный репозиторий представляет собой проект чат-бота АШАН. Ниже приведены шаги, которые необходимо выполнить, чтобы запустить бота на вашей локальной машине.

## Шаг 1: Клонирование репозитория

Сначала склонируйте репозиторий на свою локальную машину, выполнив следующую команду в вашем терминале:

```zsh
git clone https://github.com/VasilisaKashperko/EverVision-Auchan.git
```

## Шаг 2: Переход в репозиторий

Перейдите в директорию склонированного репозитория:

```zsh
cd EverVision-Auchan
```

## Шаг 3: Создание виртуального окружения

Убедитесь, что на вашей машине установлены Python, pip и python-venv. Создайте виртуальное окружение с именем venv:

```zsh
python -m venv venv
```

## Шаг 4: Активация виртуального окружения

Активируйте виртуальное окружение venv:

```zsh
source venv/bin/activate
```

## Шаг 5: Установка зависимостей

Установите все необходимые зависимости из файла requirements.txt:

```zsh
pip install -r requirements.txt
```

Убедитесь, что данные зависимости установлены:

```zsh
pip install openai
pip install streamlit
pip install langchain
pip install tiktoken
pip install faiss-cpu
```

## Шаг 6: Создание файла с секретами

Создайте файл secrets.toml в директории .streamlit:

```zsh
touch .streamlit/secrets.toml
```

## Шаг 7: Добавление ключа OPENAI API

Откройте файл secrets.toml и добавьте ваш ключ OPENAI API в следующем формате:

```zsh
OPENAI_API_KEY="ваш_ключ"
```

## Шаг 8: Запуск бота

Теперь можно запустить бота одним из двух предложенных способов. Выберите одну из следующих команд:

Через Streamlit:

```zsh
streamlit run chatbot.py
```

Или через скрипт:

```zsh
sh run.sh
```

После выполнения указанных шагов, бот будет успешно запущен на вашей локальной машине. Наслаждайтесь общением!

На данном этапе к просмотру и тестированию рекомендуется ветка main. Разработка на текущий момент ведется в ветке vector_search (тоже рекомендуется к просмотру :)).

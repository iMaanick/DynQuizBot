# **DynBOT**

### **Описание проекта**

Этот проект разработан в рамках **Education Hour** для демонстрации возможностей `aiogram-dialog`.  
Он включает:

- **Бэкенд** на **FastAPI** с использованием **FastStream**
- **Телеграм-бот** на **aiogram-dialog** с использованием **FastStream** и **Dishka**
- **Фронтенд** на **React** для визуализации диалогов

### **Функциональность**

✅ Визуализация сообщений, кнопок и инпутов  
✅ Разные цвета стрелок для связи кнопок с сообщениями  
✅ Перетаскивание узлов для удобства просмотра  
✅ Редактирование JSON в текстовом поле  
✅ Отправка JSON на сервер

---

## **Запуск проекта**

```bash
pip install poetry
poetry install
poetry shell
````

### **1. Бэкенд (FastAPI с FastStream)**

```bash
docker-compose up
uvicorn --factory app.main:create_app --host localhost --port 8000
```

### **2. Телеграм-бот (aiogram-dialog с FastStream)**

```bash
python -m app.presentation.telegram.main
```

### **3. Фронтенд (React)**

```bash
npm install
npm run dev
```

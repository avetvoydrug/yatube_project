# Добавить папку в игнор-лист гита 
# командой из корневой директории проекта (а можно дописать gitignore руками)
```
echo 'name' >> .gitignore
``` 
### Удалить папку из списка отслеживаемых файлов (staging area)
```
git rm -r --cached name
``` 
### Добавить файл в гит
```
git add .gitignore
``` 
### Зафиксировать изменения в новом коммите
```
git commit -m 'Директория name добавлена в gitignore'
``` 
### Запушить 
```
git push 
```
# Запускаем!
- Откройте терминал и прейдите в корневую директорию проекта yatube_poject
- Активируйте виртуальное окружение
- Перейдите в папку с manage.py — yatube_poject/yatube
- Выполните команду, запускающую сервер в режиме разработки: python3 manage.py runserver (если что-то       пойдёт не так — попробуйте вызвать не python3, а python: python manage.py runserver).

# Venv activ
```
py -m venv venv

Set-ExecutionPolicy Unrestricted -Scope Process

.\venv\Scripts\activate
```

# links:

- http://127.0.0.1:8000,
- http://127.0.0.1:8000/group/suck_my_balls/ (на месте any_slug может быль любая slug-строка).
# Добавить папку в игнор-лист гита 
# командой из корневой директории проекта (а можно дописать gitignore руками)
echo '.vscode' >> .gitignore
 
# Удалить папку из списка отслеживаемых файлов (staging area)
git rm -r --cached .vscode
 
# Добавить файл в гит
git add .gitignore
 
# Зафиксировать изменения в новом коммите
git commit -m 'Директория .vscode добавлена в gitignore'
 
# Запушить 
git push 

# Запускаем!
- Откройте терминал и прейдите в корневую директорию проекта yatube_poject
- Активируйте виртуальное окружение
- Перейдите в папку с manage.py — yatube_poject/yatube
- Выполните команду, запускающую сервер в режиме разработки: python3 manage.py runserver (если что-то       пойдёт не так — попробуйте вызвать не python3, а python: python manage.py runserver).
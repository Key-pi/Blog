Функционал проекта.

- Я менял локальный путь и он у меня такой (http://mysite.ua:8000/boards/) Home страница. Это я к тому что возможно вам нужно будет убрать из настроек ALLOWED_HOSTS = [
    'mysite.ua',
]


- Так же , если хотите включить DDT нужно расскоментировать в настройках # INTERNAL_IPS = [
    '127.0.0.1',
 ]



- Регистрация
    - Читатель(Профайл)
    - Блоггер(Профайл)
    - Так же при регистрации приходит поздравительное письмо на почту(не в консоль)
 
    
- Сброс пароля / Восстановление пароля    
- Логин/Логаут


- Возможность создавать
    - Доску (ajax)
    - Тему
    - Пост (при созданни поста к теме, автору темы приходит письмо на почту с нотификацией о том что под его темой оставили пост)(так же не в консоль)
 
 
- Возможность удалять
    - Доску (Только блоггер) (ajax)     
 
    
- Возможность редактировать
    - Доску(Только Блоггер) (ajax)
    - Пост(Только автор поста)
    - Аккаунт(не совсем граммотно сделано)

- reCaptcha(на регистрации и логине)
- 2 flatpages 
- Infinity scroll (На домашней странице)
- Пагинатор (Topic page, Posts page)
- При CRUD Доски показывается  месседж(has been updated, has been created, has been deleted
- Профайлы Чиателя и Блоггера доступны в админке
- Экспорт Тем(Topic) в pdf и csv
- в Админке добавлен action который делает выбранные Доски не активными для отображения
- Social_auth(Git, Google) только для Читателя
- Последние изменения (так же только для блоггера)
- Тема имеет галерею картинок
- Возможность загружать картинку и кропать
- Менеджмент комманда на создание досок add_board 1-1000

    
    
from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

# для проставления лайков/дислайков. НЕ ОБЯЗАТЕЛЬНО
import random 

def todo():    
    # полезно для отладки удалять объекты
    User.objects.all().delete()
    Category.objects.all().delete()
    
    # создание пользователей
    johny_user = User.objects.create_user(username = 'johny', email = 'johny@mail.ru', password = 'johny_password')
    tommy_user = User.objects.create_user(username = 'tommy', email = 'tommy@mail.ru', password = 'tommy_password')
    
    # создание объектов авторов
    johny = Author.objects.create(user = johny_user)
    tommy = Author.objects.create(user = tommy_user)
    
    # создание категорий
    cat_sport = Category.objects.create(name = "Спорт")
    cat_music = Category.objects.create(name = "Музыка")
    cat_cinema = Category.objects.create(name = "Кино")
    cat_IT = Category.objects.create(name = "IT")
    
    # создание текстов статей/новостей
    text_article_sport_cinema = """статья_спорт_кино_Джонни__статья_спорт_кино_Джонни__статья_спорт_кино_Джонни_
                                   _статья_спорт_кино_Джонни__статья_спорт_кино_Джонни__"""
    
    text_article_music = """статья_музыка_Томми__статья_музыка_Томми__статья_музыка_Томми_
                            _статья_музыка_Томми__статья_музыка_Томми__"""
    
    text_news_IT = """новость_IT_Томми__новость_IT_Томми__новость_IT_Томми__новость_IT_Томми__
                    новость_IT_Томми__новость_IT_Томми__новость_IT_Томми__новость_IT_Томми__"""
    
    # создание двух статей и новости
    article_johny = Post.objects.create(author = johny, post_type = Post.article, title = "статья_спорт_кино_Джонни", text = text_article_sport_cinema)
    article_tommy = Post.objects.create(author = tommy, post_type = Post.article, title = "статья_музыка_Томми", text = text_article_music)
    news_tommy = Post.objects.create(author = tommy, post_type = Post.news, title = "новость_IT_Томми", text = text_news_IT)
    
    # присваивание категорий этим объектам
    PostCategory.objects.create(post = article_johny, category = cat_sport)
    PostCategory.objects.create(post = article_johny, category = cat_cinema)
    PostCategory.objects.create(post = article_tommy, category = cat_music)
    PostCategory.objects.create(post = news_tommy, category = cat_IT)
    
    # создание комментариев
    comment1 = Comment.objects.create(post = article_johny, user = tommy.user, text = "коммент Томми №1 к статье Джонни")
    comment2 = Comment.objects.create(post = article_tommy, user = johny.user, text = "коммент Джонни №2 к статье Томми")
    comment3 = Comment.objects.create(post = news_tommy, user = tommy.user, text = "коммент Томми №3 к новости Томми")
    comment4 = Comment.objects.create(post = news_tommy, user = johny.user, text = "коммент Джонни №4 к новости Томми")
    
    
    # МОЖЕТ БЫТЬ РЕАЛИЗОВАНО ИНАЧЕ У СТУДЕНТА
    # список всех объектов, которые можно лайкать
    list_for_like = [article_johny,
                    article_tommy,
                    news_tommy,
                    comment1,
                    comment2,
                    comment3,
                    comment4]
    
    # 100 рандомных лайков/дислайков (по четности счетчика)
    for i in range(100):
        random_obj = random.choice(list_for_like)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()
            
    # подсчет рейтинга Джонни
    rating_johny = (sum([post.rating*3 for post in Post.objects.filter(author=johny)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=johny.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=johny)]))
    johny.update_rating(rating_johny) # и обновление
    
    # подсчет рейтинга Томми
    rating_tommy = (sum([post.rating*3 for post in Post.objects.filter(author=tommy)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(user=tommy.user)]) 
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=tommy)]))
    tommy.update_rating(rating_tommy) # и обновление
    
    # лучший автор
    best_author = Author.objects.all().order_by('-rating')[0]
    
    print("Лучший автор")
    print("username:", best_author.user.username)
    print("Рейтинг:", best_author.rating)
    print("")
    
    # лучшая статья(!) - именно статья (ВАЖНО)
    best_article = Post.objects.filter(post_type = Post.article).order_by('-rating')[0]
    print("Лучшая статья")
    print("Дата:", best_article.created)
    print("Автор:", best_article.author.user.username)
    print("Рейтинг:", best_article.rating)
    print("Заголовок:", best_article.title)
    print("Превью:", best_article.preview())
    print("")
    
    # печать комментариев к ней. Обязательно цикл, потому что комментарий может быть не один и нужен универсальный код
    print("Комментарии к ней")
    for comment in Comment.objects.filter(post = best_article):
        print("Дата:", comment.created)
        print("Автор:", comment.user.username)
        print("Рейтинг:", comment.rating)
        print("Комментарий:", comment.text)
        print("")
        
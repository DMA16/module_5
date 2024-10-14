from threading import current_thread
from time import sleep

class UrTube:
    users = []
    videos = []
    current_user = None

    def __contains__(self, item):
        for video in self.videos:
            if video == item:
                return True

        return False


    def is_user_exist(self, nickname, password = None, return_object = False):
        user_found = False
        for user in self.users:
            if user.nickname == nickname:
                user_found = True

            if password and user.password != hash(password):
                user_found = False

            if user_found:
                if return_object:
                    return user
                return True

        return False


    def log_in(self, nickname, password):
        if not self.current_user:
            user = self.is_user_exist(nickname, password=password, return_object=True)

            if user:
                self.current_user = user
            else:
                print("Неверный логин или пароль!")


    def register(self, nickname, password, age):
        if self.is_user_exist(nickname):
            print(f"Пользователь {nickname} уже существует")
        else:
            self.log_out()
            self.users.append(User(nickname, password, age))
            self.log_in(nickname, password)


    def log_out(self):
        self.current_user = None


    def add(self, *args):
        for arg in args:
            if arg not in self.videos:
                self.videos.append(arg)


    def get_videos(self, search_text):
        videos = []
        for video in self.videos:
            if search_text in video:
                videos.append(video.title)

        return videos


    def watch_video(self, movie_title):
        if not self.current_user:
            return print("Войдите в аккаунт, чтобы смотреть видео")

        found_video = None

        for video in self.videos:
            if video == movie_title:
                found_video = video
                break

        if found_video:
            if self.current_user < 18 and found_video.adult_mode:
                return print("Вам нет 18 лет, пожалуйста покиньте страницу")

            for sec in range(found_video.duration):
                sleep(0.1)
                found_video.time_now += 1
                print(found_video.time_now)

            found_video.time_now = 0
            print("Конец видео")





class Video:
    def __init__(self, title, duration, time_now = 0, adult_mode = False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode

    def __contains__(self, item):
        return item.lower() in self.title.lower()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.title.lower() == other.lower()

        if isinstance(other, Video):
            return self.title.lower() == other.title.lower()

    def __ne__(self, other):
        return self.title.lower() != other.lower()




class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hash(password)
        self.age = age

    def __str__(self):
        return self.nickname

    def __lt__(self, other):
        return self.age < other



ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

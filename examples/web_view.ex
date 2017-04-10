class View:
    def dispatch(self, request, *args, **kwargs):
        method = request.method
        if method in self.http_method_names:
            if method == 'GET':
                return self.get(request, *args, **kwargs)
            elif method == 'POST':
                return self.post(request, *args, **kwargs)
        return {'405': 'Not allowed'}

class LoginView(View):
    http_method_names = ['post']

    class User:
        def __init__(self, email, password):
            self.email = email
            self.password = password
            self.is_active = True

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User(email=email, password=password)

        if user:
            if user.is_active:
                request.user = user
                return {'status': 'OK'}

            error = 'Пользователь не активен'
        else:
            error = 'Введены неверные логин / пароль'
        return {'status': 'ERROR', 'error': error}

def handle():
    class HttpRequest:
        method = 'post'
        POST = {'email': 'max@mail.ru', 'password': '11'}

    request = HttpRequest()
    response = LoginView().dispatch(request)
    print(response)
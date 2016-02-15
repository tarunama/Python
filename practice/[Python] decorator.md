
# decoratorとは？

別の関数を返す関数で、通常、 @wrapper 構文で関数変換として適用されます。

デコレータの一般的な利用例は、 classmethod() と staticmethod() です。

http://docs.python.jp/2/glossary.html#term-decorator

## とりあえず書いてみる


```python
def set_place(func):
    place = func()
    return u"私は{0}にいます".format(place)

@set_place
def hapon():
    return "hapon"

@set_place
def my_home():
    return u"家"

print hapon
print my_home
```

    私はhaponにいます
    私は家にいます


## 関数を返すようにする


```python
def set_place(func):
    def wrapper(*args, **kwargs):
        place = func(*args, **kwargs)
        return u"私は{0}にいます".format(place)
    return wrapper

@set_place
def get_your_place(place):
    return place

print get_your_place("hapon")
print get_your_place(u"家")

```

    私はhaponにいます
    私は家にいます


## 使用例
### Djangoの@login_required
https://github.com/django/django/blob/master/django/contrib/auth/decorators.py


```python
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    # 結局こいつを返している
    actual_decorator = user_passes_test(
        # 関数を引数にしている？
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
```

#### user_passes_test


```python
def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # test_func = lambda u:u.is_authenticated()
            if test_func(request.user):
                # ログインしていたらここで終わり
                return view_func(request, *args, **kwargs)
            # あとは遷移先を返すのを頑張っている
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        # 結局これを返している
        return _wrapped_view
    # 結局これを返している
    return decorator
```


## @wraps?

これはラッパ関数を定義するときに partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated) を関数デコレータとして呼び出す便宜関数です。

http://docs.python.jp/2/library/functools.html#functools.wraps

### 何が便利？


```python
def set_place(func):
    def wrapper(*args, **kwargs):
        place = func(*args, **kwargs)
        return u"私は{0}にいます".format(place)
    return wrapper

@set_place
def get_your_place(place):
    """これは場所を返す関数"""
    return place

print get_your_place.__name__
print get_your_place.__doc__
```

    wrapper
    None


*Lose decorated function name and docs!!*
### とりあえず被せてみる


```python
from functools import wraps

def set_place(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        place = func(*args, **kwargs)
        return u"私は{0}にいます".format(place)
    return wrapper

@set_place
def get_your_place(place):
    """これは場所を返す関数"""
    return place

print get_your_place.__name__
print get_your_place.__doc__
```

    get_your_place
    これは場所を返す関数


## @property?
http://docs.python.jp/2/library/functions.html#property

new-style class (新しい形式のクラス) (object から派生したクラス) における property 属性を返します。

### propertyがないと？


```python
class Prop(object):
    
    def __init__(self, x):
        self.x = x
        
    def get_x(self):
        return self.x

_property = Prop(1)
print _property.get_x()
```

    1


### propertyがあると


```python
class Prop(object):
    
    def __init__(self):
        self._x = None
        
    def get_x(self):
        return self._x
    
    def set_x(self, x):
        self._x = x
        
    def del_x(self):
        del self.x
    
    x = property(get_x, set_x, del_x)

_property = Prop()
# invoked set_x
_property.x = 1
# invoked get_x
print _property.x
```

    1


## @propertyは何が便利か


```python
class Prop2(object):
    
    def __init__(self):
        self.work_days = 0
        
    @property
    def add_work_day(self, day=1):
        self.work_days += day
        return self.work_days
    

my_work = Prop2()
print my_work.add_work_day
```

    1


### @propertyは何が便利なの？？
* クラスメソッドを属性のように使える？


```python

```

import pytest
from data.login import *


# Ввод валидных данных
#@pytest.mark.parametrize("testdata1", valid_data, ids=[repr(valid_data)])
#def test_valid_data(app, testdata1):
#    app.login(testdata1)
#    assert app.find_exit_button() == "Выйти"


# Пустой логин - ошибка валидации
@pytest.mark.parametrize("testdata2", empty_login, ids=[repr(empty_login)])
def test_empty_login(app, testdata2):
    app.login(testdata2)
    assert app.check_url().endswith("/login")
    assert app.empty_login() == "Введите логин!"


# Пустой пароль - ошибка валидации
@pytest.mark.parametrize("testdata3", empty_password, ids=[repr(empty_password)])
def test_empty_password(app, testdata3):
    app.login(testdata3)
    assert app.check_url().endswith("/login")
    assert app.empty_password() == "Введите пароль!"


# Пустой логин и пароль - ошибка валидации
@pytest.mark.parametrize("testdata4", empty_login_password, ids=[repr(empty_login_password)])
def test_empty_data(app, testdata4):
    app.login(testdata4)
    assert app.check_url().endswith("/login")
    assert app.empty_login() == "Введите логин!"
    assert app.empty_password() == "Введите пароль!"


# Ввод невалидных данных - всплывающая ошибка
@pytest.mark.parametrize("testdata5", unvalid_data, ids=[repr(unvalid_data)])
def test_unvalid_data(app, testdata5):
    app.login(testdata5)
    assert app.check_url().endswith("/login")
    assert app.error_for_data() == "Неверный пароль или имя пользователя"
    assert app.error_for_data() == app.authentication_error(testdata5)


# Ввод данных невалидного пользователя - заглушка-ошибка
@pytest.mark.parametrize("testdata6", unvalid_userdata, ids=[repr(x) for x in unvalid_userdata])
def test_unvalid_userdata(app, testdata6):
    app.login(testdata6)
    assert app.check_url().endswith("/error")
    assert app.refresh_button() == "Обновить"
from selenium import webdriver
import time
import requests


class Application:

    def __init__(self, base_url):
        self.wd = webdriver.Chrome()
        self.base_url = base_url

    def fixture_is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_login_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def change_fill_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_id(field_name).click()
            wd.find_element_by_id(field_name).clear()
            wd.find_element_by_id(field_name).send_keys(text)

    def fill_login_form(self, testdata):
        wd = self.wd
        self.change_fill_value("login_username", testdata.username)
        self.change_fill_value("login_password", testdata.password)
        wd.find_element_by_css_selector('[data-e2e="login-button"]').click()
        time.sleep(1)

    def login(self, testdata):
        self.open_login_page()
        self.fill_login_form(testdata)

    def find_exit_button(self):
        wd = self.wd
        exit_button = wd.find_element_by_xpath('//*[@id="root"]/section/aside/div/div/ul[3]/li[2]/span[2]').text
        return exit_button

    def check_url(self):
        url_page = self.wd.current_url
        return url_page

    def empty_login(self):
        wd = self.wd
        error_for_empty_login = wd.find_element_by_xpath('//*[@id="login"]/div[1]/div/div[2]/div').text
        return error_for_empty_login

    def empty_password(self):
        wd = self.wd
        error_for_empty_password = wd.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[2]/div').text
        return error_for_empty_password

    def error_for_data(self):
        wd = self.wd
        time.sleep(1
                   )
        error_message = wd.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div[1]").text
        return error_message

    def refresh_button(self):
        wd = self.wd
        refresh_button_text = wd.find_element_by_xpath('//*[@id="root"]/div/div/button/span').text
        return refresh_button_text

    def find_name(self):
        wd = self.wd
        name = wd.find_element_by_css_selector('div.userInfoName > b').text
        return name

    def find_module(self):
        wd = self.wd
        name = wd.find_element_by_xpath('//*[@id="root"]/section/aside/div/div/div[1]/div/div[2]').text
        return name

    def logout(self):
        wd = self.wd
        wd.find_element_by_xpath('//*[@id="root"]/section/aside/div/div/ul[3]/li[2]/span[2]').click()
        wd.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div[3]/button[2]/span').click()
        wd.find_element_by_id("login_username")

    def destroy(self):
        self.wd.quit()


    def api(self, testdata):
        mutation = {
            "query": '''
                mutation ($username:String!, $password:String!){
                    user {
                        login(payload: {username: $username, password: $password}) {
                          status
                          error {
                            __typename
                            ... on  AccessDeniedError {
                              message
                            }
                            ... on  AuthenticationError {
                              message
                            }
                          }
                          result {
                            id
                            isAdmin
                            fullName
                            module
                            point {
                                id
                                name
                            }
                            city {
                                id
                                name
                            }
                          }
                        }
                    }
                 }
            ''',
            "variables": {
                "username": testdata.username,
                "password": testdata.password
            }
        }
        response = requests.post('https://api.fc.frfrstaging.pw/graphql', json=mutation)
        return response

    def authentication_error(self, testdata):
        resp = self.api(testdata).json()
        ErrorText = resp['data']['user']['login']['error']['message']
        return ErrorText

    def get_full_name(self, testdata):
        resp = self.api(testdata).json()
        full_name = (resp['data']['user']['login']['result']['fullName'])
        return full_name

    def get_module(self, testdata):
        resp = self.api(testdata).json()
        module = (resp['data']['user']['login']['result']['module'])
        meta = self.api_meta(testdata)
        moduleMeta = meta['data']['meta']['result']['staffMeta']['moduleMeta']
        mod = [moduleMeta[i] for i in range(len(moduleMeta)) if(moduleMeta[i]["value"]==module)][0]
        findmodule = mod['text']
        return findmodule

    #def get_city_name(self):
        #resp = self.api().json()
        #city_name = (resp['data']['user']['login']['result']['city']['name'])
        #return city_name

    def api_meta(self, testdata):
        cookies = self.api(testdata).cookies
        query = """
            query Meta {
                  meta {
                    status
                    error {
                      __typename
                    }
                    result {
                        staffMeta {
                            moduleMeta {
                              value
                              text
                            }
                        }
                    }
                  }
            }     
            """
        response_meta = requests.get('https://api.fc.frfrstaging.pw/graphql', json={'query': query}, cookies=cookies).json()
        return response_meta


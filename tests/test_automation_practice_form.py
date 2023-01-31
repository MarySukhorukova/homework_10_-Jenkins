from allure_commons.types import Severity
from selene import be, have
from selene.support.shared import browser
from selene.support.shared.jquery_style import s
import os
from selene import command
import tests
import allure
from utils import attach


@allure.tag('web')
@allure.label('owner', 'marysukhorukova')
@allure.severity(Severity.CRITICAL)
@allure.feature('Регистрация нового пользователя со всеми заполненными полями')
@allure.story('Регистрация')
@allure.link('https://demoqa.com', name='Testing')
def test_filling_and_submitting_form():
    with allure.step("Открываем страницу с формой"):
        browser.open('/automation-practice-form')

    # WHEN
    with allure.step("Заполняем обязательные поля"):
        s('#firstName').type('Harry')
        s('#lastName').type('Potter')
        s('#userEmail').type('hp@test.com')
        browser.all('[name=gender]').element_by(have.value('Male')).element('./following-sibling::*').click()
        s('#userNumber').type('0123456789')

    with allure.step("Заполняем не обязательные поля"):
        s('#dateOfBirthInput').click()
        s('.react-datepicker__month-select').send_keys('July')
        s('.react-datepicker__year-select').send_keys('1980')
        s(f'.react-datepicker__day--0{31}').click()

        s('#subjectsInput').type('Arts').press_enter()
        s('[for="hobbies-checkbox-1"]').click()

        s('#uploadPicture').set_value(
            os.path.abspath(os.path.join(os.path.dirname(tests.__file__), 'files/Pytest_logo.svg.png')))

        s('#currentAddress').type('Hogwarts').perform(command.js.scroll_into_view)

        s('#state').click()
        browser.all('[id^=react-select][id*=option]').element_by(have.exact_text('Haryana')).click()
        s('#city').click()
        browser.all('[id^=react-select][id*=option]').element_by(have.exact_text('Karnal')).click()

    with allure.step("Сабмитим форму"):
        s('#submit').press_enter()

    # THEN
    with allure.step("Проверяем, что заполненные поля имеют нужные данные"):
        s('#example-modal-sizes-title-lg').should(have.text('Thanks for submitting the form'))
        s('.table').should(have.text('Harry Potter'))
        s('.table').should(have.text('hp@test.com'))
        s('.table').should(have.text('Male'))
        s('.table').should(have.text('0123456789'))
        s('.table').should(have.text('31 July,1980'))
        s('.table').should(have.text('Arts'))
        s('.table').should(have.text('Sports'))
        s('.table').should(have.text('Pytest_logo.svg.png'))
        s('.table').should(have.text('Hogwarts'))
        s('.table').should(have.text('Haryana Karnal'))

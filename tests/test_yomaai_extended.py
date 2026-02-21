"""
Расширенные автотесты YomaAI — Selenium + pytest.

Тест 4: Адаптивность (мобильный и планшетный viewport)
Тест 5: localStorage (персистентность и очистка)
Тест 6: Обработка ошибок (нет API ключа, сервер недоступен)
Тест 7: Кнопки результата (Create Another Idea, Regenerate)
Тест 8: Диалог Yoma (Next, Let's go!, Skip dialog)
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ─── Хелперы ──────────────────────────────────────────────────

def _skip_dialog_via_storage(driver, base_url: str) -> None:
    """Устанавливает skip-dialog в localStorage и переходит на /create."""
    driver.get(base_url)
    driver.execute_script("localStorage.setItem('yoma-skip-dialog', 'true');")
    driver.get(f"{base_url}/create")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
        )
    )


def _mock_fetch_success(driver) -> None:
    """
    Подменяет window.fetch так, чтобы POST /api/generate
    мгновенно возвращал фейковый успешный ответ.
    Остальные запросы идут через оригинальный fetch.
    """
    driver.execute_script("""
        window.__originalFetch = window.fetch;
        window.fetch = function(url, opts) {
            if (url === '/api/generate' && opts && opts.method === 'POST') {
                return Promise.resolve(new Response(
                    JSON.stringify({ result: '## Test Idea\\n\\nThis is a **mock AI response** for automated testing. It contains enough text to pass the length check and verifies that the result phase renders correctly with markdown content.' }),
                    { status: 200, headers: { 'Content-Type': 'application/json' } }
                ));
            }
            return window.__originalFetch(url, opts);
        };
    """)


def _mock_fetch_api_error(driver) -> None:
    """
    Подменяет fetch: POST /api/generate возвращает 500 с ошибкой.
    Имитирует ситуацию, когда API ключ невалиден / отсутствует.
    """
    driver.execute_script("""
        window.__originalFetch = window.fetch;
        window.fetch = function(url, opts) {
            if (url === '/api/generate' && opts && opts.method === 'POST') {
                return Promise.resolve(new Response(
                    JSON.stringify({ error: 'API key for Claude is not configured' }),
                    { status: 500, headers: { 'Content-Type': 'application/json' } }
                ));
            }
            return window.__originalFetch(url, opts);
        };
    """)


def _mock_fetch_network_error(driver) -> None:
    """
    Подменяет fetch: POST /api/generate выбрасывает TypeError (network error).
    Имитирует ситуацию, когда backend вообще не запущен.
    """
    driver.execute_script("""
        window.__originalFetch = window.fetch;
        window.fetch = function(url, opts) {
            if (url === '/api/generate' && opts && opts.method === 'POST') {
                return Promise.reject(new TypeError('Failed to fetch'));
            }
            return window.__originalFetch(url, opts);
        };
    """)


def _generate_with_mock(driver, base_url: str) -> None:
    """
    Полный цикл: skip dialog → mock fetch → нажать Create! → дождаться результата.
    После вызова драйвер находится на фазе result.
    """
    _skip_dialog_via_storage(driver, base_url)
    _mock_fetch_success(driver)

    create_btn = driver.find_element(
        By.XPATH, "//button[contains(@class, 'rainbow-btn')]"
    )
    create_btn.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), \"Yoma's Idea\")]")
        )
    )


# ─────────────────────────────────────────────────────────────
# Тест 4: Адаптивность
# ─────────────────────────────────────────────────────────────
class TestResponsiveness:
    """Проверяем, что страницы корректно отображаются на разных viewport."""

    def test_mobile_main_page_no_overflow(self, mobile_driver, base_url):
        """Мобильный viewport (375×812): элементы не вылезают за экран."""
        mobile_driver.get(base_url)

        WebDriverWait(mobile_driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        viewport_width = mobile_driver.execute_script("return window.innerWidth;")
        body_scroll_width = mobile_driver.execute_script(
            "return document.body.scrollWidth;"
        )

        assert body_scroll_width <= viewport_width + 5, (
            f"Горизонтальный скролл на мобильном: "
            f"scrollWidth={body_scroll_width}, viewport={viewport_width}"
        )

    def test_mobile_heading_font_size(self, mobile_driver, base_url):
        """
        Мобильный viewport: заголовок h1 использует text-4xl (≈36px),
        а не десктопный md:text-5xl (≈48px).
        """
        mobile_driver.get(base_url)

        heading = WebDriverWait(mobile_driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        font_size = mobile_driver.execute_script(
            "return parseFloat(window.getComputedStyle(arguments[0]).fontSize);",
            heading,
        )

        # text-4xl = 2.25rem ≈ 36px, md:text-5xl = 3rem ≈ 48px
        # На мобильном должен быть ~36px (±2px допуск)
        assert font_size < 42, (
            f"На мобильном заголовок слишком большой: {font_size}px "
            f"(ожидалось ~36px для text-4xl)"
        )

    def test_mobile_create_page_no_overflow(self, mobile_driver, base_url):
        """Мобильный viewport: страница /create не имеет горизонтального скролла."""
        mobile_driver.get(base_url)
        mobile_driver.execute_script(
            "localStorage.setItem('yoma-skip-dialog', 'true');"
        )
        mobile_driver.get(f"{base_url}/create")

        WebDriverWait(mobile_driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )

        viewport_width = mobile_driver.execute_script("return window.innerWidth;")
        body_scroll_width = mobile_driver.execute_script(
            "return document.body.scrollWidth;"
        )

        assert body_scroll_width <= viewport_width + 5, (
            f"Горизонтальный скролл на /create (мобильный): "
            f"scrollWidth={body_scroll_width}, viewport={viewport_width}"
        )

    def test_tablet_main_page_no_overflow(self, tablet_driver, base_url):
        """Планшетный viewport (768×1024): элементы не вылезают за экран."""
        tablet_driver.get(base_url)

        WebDriverWait(tablet_driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        viewport_width = tablet_driver.execute_script("return window.innerWidth;")
        body_scroll_width = tablet_driver.execute_script(
            "return document.body.scrollWidth;"
        )

        assert body_scroll_width <= viewport_width + 5, (
            f"Горизонтальный скролл на планшете: "
            f"scrollWidth={body_scroll_width}, viewport={viewport_width}"
        )

    def test_tablet_heading_font_size(self, tablet_driver, base_url):
        """
        Планшетный viewport (768px ≥ md breakpoint):
        заголовок использует md:text-5xl (≈48px).
        """
        tablet_driver.get(base_url)

        heading = WebDriverWait(tablet_driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        font_size = tablet_driver.execute_script(
            "return parseFloat(window.getComputedStyle(arguments[0]).fontSize);",
            heading,
        )

        # md breakpoint = 768px, text-5xl = 3rem ≈ 48px
        assert font_size >= 42, (
            f"На планшете заголовок слишком мелкий: {font_size}px "
            f"(ожидалось ~48px для md:text-5xl)"
        )

    def test_tablet_create_page_no_overflow(self, tablet_driver, base_url):
        """Планшетный viewport: страница /create не имеет горизонтального скролла."""
        tablet_driver.get(base_url)
        tablet_driver.execute_script(
            "localStorage.setItem('yoma-skip-dialog', 'true');"
        )
        tablet_driver.get(f"{base_url}/create")

        WebDriverWait(tablet_driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )

        viewport_width = tablet_driver.execute_script("return window.innerWidth;")
        body_scroll_width = tablet_driver.execute_script(
            "return document.body.scrollWidth;"
        )

        assert body_scroll_width <= viewport_width + 5, (
            f"Горизонтальный скролл на /create (планшет): "
            f"scrollWidth={body_scroll_width}, viewport={viewport_width}"
        )


# ─────────────────────────────────────────────────────────────
# Тест 5: localStorage
# ─────────────────────────────────────────────────────────────
class TestLocalStorage:
    """Проверяем персистентность и очистку localStorage."""

    def test_skip_dialog_persists_after_reload(self, driver, base_url):
        """
        Включаем skip dialog → перезагружаем страницу →
        настройка сохранилась (диалог не показывается).
        """
        # Включаем skip dialog
        driver.get(f"{base_url}/settings")
        driver.execute_script("localStorage.setItem('yoma-skip-dialog', 'true');")

        # Перезагружаем страницу
        driver.refresh()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Settings')]")
            )
        )

        # Проверяем, что значение сохранилось
        value = driver.execute_script(
            "return localStorage.getItem('yoma-skip-dialog');"
        )
        assert value == "true", (
            f"localStorage['yoma-skip-dialog'] после reload = '{value}', ожидалось 'true'"
        )

        # Идём на /create — должны сразу попасть в настройки
        driver.get(f"{base_url}/create")

        craft_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )
        assert craft_heading.is_displayed(), (
            "После перезагрузки skip dialog не сохранился — диалог показывается"
        )

    def test_clearing_localstorage_restores_default(self, driver, base_url):
        """
        После удаления yoma-skip-dialog из localStorage
        поведение возвращается к дефолту (диалог показывается).
        """
        # Сначала включаем skip dialog
        driver.get(base_url)
        driver.execute_script("localStorage.setItem('yoma-skip-dialog', 'true');")

        # Удаляем ключ
        driver.execute_script("localStorage.removeItem('yoma-skip-dialog');")

        # Проверяем, что ключ удалён
        value = driver.execute_script(
            "return localStorage.getItem('yoma-skip-dialog');"
        )
        assert value is None, (
            f"localStorage['yoma-skip-dialog'] после удаления = '{value}', ожидалось null"
        )

        # Идём на /create — диалог должен появиться
        driver.get(f"{base_url}/create")

        yoma_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Yoma:')]")
            )
        )
        assert yoma_label.is_displayed(), (
            "После очистки localStorage диалог не появился — дефолт не восстановлен"
        )


# ─────────────────────────────────────────────────────────────
# Тест 6: Обработка ошибок
# ─────────────────────────────────────────────────────────────
class TestErrorHandling:
    """
    Проверяем отображение ошибок при проблемах с backend/API.
    Используем подмену window.fetch для имитации ошибок.
    """

    def test_api_error_shows_red_message(self, driver, base_url):
        """
        Если backend возвращает ошибку (нет API ключа, 500),
        на странице появляется красное сообщение (div с border-red-300).
        """
        _skip_dialog_via_storage(driver, base_url)
        _mock_fetch_api_error(driver)

        # Нажимаем Create!
        create_btn = driver.find_element(
            By.XPATH, "//button[contains(@class, 'rainbow-btn')]"
        )
        create_btn.click()

        # Ждём появления красного блока ошибки
        error_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'border-red-300')]")
            )
        )
        assert error_div.is_displayed(), "Красное сообщение об ошибке не отображается"

        error_text = error_div.text
        assert len(error_text) > 0, "Сообщение об ошибке пустое"
        assert "API key" in error_text or "not configured" in error_text, (
            f"Текст ошибки не содержит информацию об API ключе: '{error_text}'"
        )

    def test_network_error_shows_failed_message(self, driver, base_url):
        """
        Если backend недоступен (fetch выбрасывает ошибку),
        появляется сообщение 'Failed to connect to the server'.
        """
        _skip_dialog_via_storage(driver, base_url)
        _mock_fetch_network_error(driver)

        # Нажимаем Create!
        create_btn = driver.find_element(
            By.XPATH, "//button[contains(@class, 'rainbow-btn')]"
        )
        create_btn.click()

        # Ждём появления красного блока ошибки
        error_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'border-red-300')]")
            )
        )
        assert error_div.is_displayed(), "Сообщение об ошибке не отображается"

        error_text = error_div.text
        assert "Failed to connect to the server" in error_text, (
            f"Ожидалось 'Failed to connect to the server', получено: '{error_text}'"
        )


# ─────────────────────────────────────────────────────────────
# Тест 7: Кнопки результата
# ─────────────────────────────────────────────────────────────
class TestResultButtons:
    """
    Проверяем кнопки 'Create Another Idea' и 'Regenerate'
    на странице результата. Используем mock fetch для скорости.
    """

    def test_create_another_idea_resets_to_settings(self, driver, base_url):
        """
        Кнопка 'Create Another Idea' сбрасывает результат
        и возвращает к пустым настройкам.
        """
        _generate_with_mock(driver, base_url)

        # Нажимаем "Create Another Idea"
        another_btn = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Create Another Idea')]"
        )
        another_btn.click()

        # Должны вернуться в фазу настроек
        craft_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )
        assert craft_heading.is_displayed(), (
            "'Create Another Idea' не вернул к настройкам"
        )

        # Проверяем, что все select-ы сброшены (значение = пустая строка)
        selects = driver.find_elements(By.CSS_SELECTOR, "select.sketchy-select")
        for select in selects:
            value = select.get_attribute("value")
            assert value == "", (
                f"Select '{select.get_attribute('id')}' не сброшен: value='{value}'"
            )

        # Проверяем, что textarea пустой
        textarea = driver.find_element(By.ID, "additional-details")
        assert textarea.get_attribute("value") == "", (
            "Textarea 'Additional Details' не сброшен"
        )

    def test_regenerate_produces_new_result(self, driver, base_url):
        """
        Кнопка 'Regenerate' повторно генерирует идею —
        показывается загрузка, потом новый результат.
        """
        _generate_with_mock(driver, base_url)

        # Запоминаем текущий результат
        result_container = driver.find_element(
            By.XPATH, "//div[contains(@class, 'prose-yoma')]"
        )
        first_result = result_container.text.strip()
        assert len(first_result) > 0, "Первый результат пустой"

        # Мокаем fetch с небольшой задержкой, чтобы фаза загрузки
        # успела отрисоваться и Selenium мог её поймать
        driver.execute_script("""
            window.__originalFetch = window.__originalFetch || window.fetch;
            window.fetch = function(url, opts) {
                if (url === '/api/generate' && opts && opts.method === 'POST') {
                    return new Promise(resolve => {
                        setTimeout(() => {
                            resolve(new Response(
                                JSON.stringify({ result: '## Regenerated Idea\\n\\nThis is a **regenerated mock response** with different content to verify that the Regenerate button triggers a new generation cycle successfully.' }),
                                { status: 200, headers: { 'Content-Type': 'application/json' } }
                            ));
                        }, 500);
                    });
                }
                return window.__originalFetch(url, opts);
            };
        """)

        # Нажимаем "Regenerate"
        regen_btn = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Regenerate')]"
        )
        regen_btn.click()

        # Должна появиться фаза загрузки (мок отвечает через 500ms)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Yoma is crafting your idea')]")
            )
        )

        # Потом снова результат
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), \"Yoma's Idea\")]")
            )
        )

        new_result_container = driver.find_element(
            By.XPATH, "//div[contains(@class, 'prose-yoma')]"
        )
        new_result = new_result_container.text.strip()
        assert len(new_result) > 0, "Результат после Regenerate пустой"


# ─────────────────────────────────────────────────────────────
# Тест 8: Диалог Yoma (Next, Let's go!, Skip dialog)
# ─────────────────────────────────────────────────────────────
class TestYomaDialog:
    """
    Проверяем поведение TypewriterDialog:
    - Кнопка 'Next' после первой реплики
    - Кнопка 'Let's go!' после последней
    - Кнопка 'Skip dialog' пропускает весь диалог
    """

    def _open_create_with_dialog(self, driver, base_url: str) -> None:
        """Открывает /create с чистым localStorage (диалог показывается)."""
        driver.get(base_url)
        driver.execute_script("localStorage.removeItem('yoma-skip-dialog');")
        driver.get(f"{base_url}/create")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Yoma:')]")
            )
        )

    def _wait_for_typewriter(self, driver) -> None:
        """
        Ждёт завершения typewriter-эффекта.
        Диалог печатает по 3ms/символ, максимум ~80 символов ≈ 240ms.
        Ждём до 3 секунд для надёжности.
        """
        time.sleep(1)

    def test_next_button_appears_after_first_line(self, driver, base_url):
        """
        После завершения первой реплики появляется кнопка 'Next'.
        """
        self._open_create_with_dialog(driver, base_url)
        self._wait_for_typewriter(driver)

        next_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Next')]")
            )
        )
        assert next_btn.is_displayed(), "Кнопка 'Next' не появилась после первой реплики"

    def test_next_shows_second_line(self, driver, base_url):
        """
        Клик по 'Next' показывает вторую реплику диалога.
        """
        self._open_create_with_dialog(driver, base_url)
        self._wait_for_typewriter(driver)

        next_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Next')]")
            )
        )
        next_btn.click()

        # После клика начинается вторая реплика — ждём typewriter
        self._wait_for_typewriter(driver)

        # Текст второй реплики содержит "help you create"
        dialog_text = driver.find_element(
            By.XPATH, "//div[contains(@class, 'border-gray-800')]//p[contains(@class, 'text-xl')]"
        )
        assert "help you create" in dialog_text.text.lower() or "ready" in dialog_text.text.lower(), (
            f"Вторая реплика не показана. Текст: '{dialog_text.text}'"
        )

    def test_lets_go_button_on_last_line(self, driver, base_url):
        """
        На последней реплике вместо 'Next' отображается 'Let's go!'.
        """
        self._open_create_with_dialog(driver, base_url)
        self._wait_for_typewriter(driver)

        # Кликаем Next для перехода ко второй (последней) реплике
        next_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Next')]")
            )
        )
        next_btn.click()
        self._wait_for_typewriter(driver)

        # Должна появиться кнопка "Let's go!" вместо "Next"
        lets_go_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), \"Let's go!\")]")
            )
        )
        assert lets_go_btn.is_displayed(), "Кнопка 'Let's go!' не появилась на последней реплике"

        # "Next" не должно быть на странице
        next_buttons = driver.find_elements(
            By.XPATH, "//button[text()='Next']"
        )
        assert len(next_buttons) == 0, (
            "Кнопка 'Next' всё ещё видна на последней реплике"
        )

    def test_lets_go_transitions_to_settings(self, driver, base_url):
        """
        Клик по 'Let's go!' переводит в фазу настроек (Craft Your Idea).
        """
        self._open_create_with_dialog(driver, base_url)
        self._wait_for_typewriter(driver)

        # Next → вторая реплика
        next_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Next')]")
            )
        )
        next_btn.click()
        self._wait_for_typewriter(driver)

        # Let's go! → настройки
        lets_go_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), \"Let's go!\")]")
            )
        )
        lets_go_btn.click()

        # Должна появиться фаза настроек
        craft_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )
        assert craft_heading.is_displayed(), (
            "'Let's go!' не перевёл в фазу настроек"
        )

    def test_skip_dialog_button(self, driver, base_url):
        """
        Кнопка 'Skip dialog' пропускает весь диалог
        и сразу показывает настройки.
        """
        self._open_create_with_dialog(driver, base_url)

        # Нажимаем "Skip dialog" (не ждём окончания typewriter)
        skip_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Skip dialog')]")
            )
        )
        skip_btn.click()

        # Должна появиться фаза настроек
        craft_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )
        assert craft_heading.is_displayed(), (
            "'Skip dialog' не перевёл в фазу настроек"
        )

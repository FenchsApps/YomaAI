"""
Автотесты YomaAI — Selenium + pytest.

Тест 1: Загружается ли сайт?
Тест 2: Работают ли настройки (skip dialog)?
Тест 3: Генерируется ли история через ИИ?
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ─────────────────────────────────────────────────────────────
# Тест 1: Сайт загружается
# ─────────────────────────────────────────────────────────────
class TestSiteLoads:
    """Проверяем, что главная страница загружается корректно."""

    def test_main_page_opens(self, driver, base_url):
        """Главная страница открывается без ошибок."""
        driver.get(base_url)

        # Ждём появления заголовка
        heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert "idea" in heading.text.lower() or "work" in heading.text.lower(), (
            f"Заголовок главной страницы не содержит ожидаемый текст: {heading.text}"
        )

    def test_main_page_has_cta_button(self, driver, base_url):
        """На главной есть кнопка 'Create Idea with Yoma'."""
        driver.get(base_url)

        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Create Idea with Yoma')]")
            )
        )
        assert button.is_displayed(), "Кнопка 'Create Idea with Yoma' не видна"

    def test_navigation_links_exist(self, driver, base_url):
        """В хедере есть ссылки навигации: Main, Create new Idea, Settings."""
        driver.get(base_url)

        nav = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "nav"))
        )

        buttons = nav.find_elements(By.TAG_NAME, "button")
        button_texts = [b.text for b in buttons]

        assert "Main" in button_texts, f"Нет кнопки 'Main' в навигации: {button_texts}"
        assert "Create new Idea" in button_texts, (
            f"Нет кнопки 'Create new Idea' в навигации: {button_texts}"
        )
        assert "Settings" in button_texts, (
            f"Нет кнопки 'Settings' в навигации: {button_texts}"
        )


# ─────────────────────────────────────────────────────────────
# Тест 2: Настройки работают (skip dialog)
# ─────────────────────────────────────────────────────────────
class TestSettingsSkipDialog:
    """
    Проверяем, что настройка 'Skip Yoma's intro dialog' работает:
    1. Заходим на /create — там должен быть диалог (по умолчанию).
    2. Заходим в настройки, включаем skip dialog.
    3. Заходим на /create — диалога быть не должно, сразу настройки.
    """

    def test_dialog_shown_by_default(self, driver, base_url):
        """По умолчанию на /create показывается диалог Yoma."""
        # Очищаем localStorage, чтобы был дефолт
        driver.get(base_url)
        driver.execute_script("localStorage.removeItem('yoma-skip-dialog');")

        driver.get(f"{base_url}/create")

        # Диалог должен содержать текст "Yoma:"
        yoma_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Yoma:')]")
            )
        )
        assert yoma_label.is_displayed(), "Диалог Yoma не показан по умолчанию"

    def test_skip_dialog_setting_works(self, driver, base_url):
        """
        После включения настройки skip dialog,
        на /create диалога нет — сразу показываются настройки идеи.
        """
        # Шаг 1: Заходим на /settings
        driver.get(f"{base_url}/settings")

        # Находим toggle-кнопку (Skip Yoma's intro dialog)
        toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'rounded-full')]")
            )
        )

        # Проверяем начальное состояние — если уже включён, не кликаем повторно
        # bg-gray-800 = включён (skip), bg-white = выключен
        classes = toggle.get_attribute("class")
        if "bg-white" in classes and "bg-gray-800" not in classes.replace("bg-white", ""):
            # Toggle выключен — кликаем, чтобы включить
            toggle.click()
        elif "bg-gray-800" not in classes:
            # На всякий случай кликаем
            toggle.click()

        # Шаг 2: Переходим на /create
        driver.get(f"{base_url}/create")

        # Шаг 3: Диалога быть НЕ должно — должен быть заголовок "Craft Your Idea"
        craft_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )
        assert craft_heading.is_displayed(), (
            "После включения skip dialog, страница /create "
            "должна сразу показывать настройки, а не диалог"
        )

        # Убеждаемся, что диалога "Yoma:" на странице нет
        yoma_labels = driver.find_elements(
            By.XPATH, "//*[contains(text(), 'Yoma:')]"
        )
        assert len(yoma_labels) == 0, (
            "Диалог Yoma всё ещё показывается, хотя skip dialog включён"
        )

    def test_reset_skip_dialog(self, driver, base_url):
        """
        Отключаем skip dialog обратно — диалог снова появляется на /create.
        """
        # Устанавливаем skip dialog = true через localStorage
        driver.get(base_url)
        driver.execute_script("localStorage.setItem('yoma-skip-dialog', 'true');")

        # Заходим в настройки и отключаем toggle
        driver.get(f"{base_url}/settings")
        toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'rounded-full')]")
            )
        )

        # Сейчас toggle включён (bg-gray-800) — кликаем, чтобы выключить
        toggle.click()

        # Идём на /create — диалог должен снова появиться
        driver.get(f"{base_url}/create")

        yoma_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Yoma:')]")
            )
        )
        assert yoma_label.is_displayed(), (
            "После отключения skip dialog, диалог должен снова появляться"
        )


# ─────────────────────────────────────────────────────────────
# Тест 3: Генерация истории через ИИ
# ─────────────────────────────────────────────────────────────
class TestAIGeneration:
    """
    Проверяем, что ИИ генерирует историю:
    1. Скипаем диалог.
    2. Нажимаем кнопку 'Create!'.
    3. Ждём появления результата от ИИ.
    """

    def test_create_story(self, driver, base_url):
        """
        Бот нажимает на кнопку Create, ждёт пока ИИ выдаст текст.
        Таймаут увеличен до 120 секунд, т.к. ИИ может думать долго.
        """
        # Скипаем диалог через localStorage
        driver.get(base_url)
        driver.execute_script("localStorage.setItem('yoma-skip-dialog', 'true');")

        # Переходим на страницу создания
        driver.get(f"{base_url}/create")

        # Ждём появления заголовка настроек
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Craft Your Idea')]")
            )
        )

        # Находим и нажимаем кнопку "Create!" (rainbow-btn)
        create_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'rainbow-btn')]")
            )
        )
        create_btn.click()

        # Должна появиться фаза загрузки "Yoma is crafting your idea..."
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Yoma is crafting your idea')]")
            )
        )

        # Ждём результат — заголовок "Yoma's Idea" (таймаут 120 сек)
        result_heading = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), \"Yoma's Idea\")]")
            )
        )
        assert result_heading.is_displayed(), "Заголовок результата 'Yoma's Idea' не отображается"

        # Проверяем, что в блоке результата есть текст (ИИ что-то сгенерировал)
        result_container = driver.find_element(
            By.XPATH, "//div[contains(@class, 'prose-yoma')]"
        )
        result_text = result_container.text.strip()
        assert len(result_text) > 50, (
            f"ИИ вернул слишком короткий или пустой результат "
            f"({len(result_text)} символов): '{result_text[:100]}...'"
        )

        # Проверяем, что кнопки "Create Another Idea" и "Regenerate" появились
        another_btn = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Create Another Idea')]"
        )
        regen_btn = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Regenerate')]"
        )
        assert another_btn.is_displayed(), "Кнопка 'Create Another Idea' не видна"
        assert regen_btn.is_displayed(), "Кнопка 'Regenerate' не видна"

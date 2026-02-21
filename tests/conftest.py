"""
Фикстуры для автотестов YomaAI.

Перед запуском тестов необходимо:
  1. Запустить приложение: npm run dev:full
  2. Установить зависимости: pip install -r tests/requirements.txt
  3. Убедиться, что ChromeDriver установлен и доступен в PATH

Запуск тестов:
  uv run --with pytest --with selenium pytest tests/ -v
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BASE_URL = "http://localhost:5173"


def _make_driver(width: int, height: int) -> webdriver.Chrome:
    """Создаёт Chrome headless-драйвер с заданным размером окна."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--window-size={width},{height}")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(5)
    return browser


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL приложения."""
    return BASE_URL


@pytest.fixture(scope="function")
def driver():
    """Chrome WebDriver — десктоп (1920×1080). Закрывается после каждого теста."""
    browser = _make_driver(1920, 1080)
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def mobile_driver():
    """Chrome WebDriver — мобильный viewport (375×812, iPhone-like).
    Использует CDP DeviceMetricsOverride, т.к. headless Chrome
    имеет минимальную ширину окна ~500px."""
    browser = _make_driver(375, 812)
    # Принудительно задаём viewport через Chrome DevTools Protocol
    browser.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 375,
        "height": 812,
        "deviceScaleFactor": 1,
        "mobile": True,
    })
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def tablet_driver():
    """Chrome WebDriver — планшетный viewport (768×1024, iPad-like)."""
    browser = _make_driver(768, 1024)
    yield browser
    browser.quit()

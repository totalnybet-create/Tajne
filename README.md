# Bonus Radar

Mobilny panel HTML i skaner Python dla publicznych katalogów bonusów slotowych.

## Lokalnie

```sh
python monitor.py
python -m http.server 8000
```

Otwórz `http://localhost:8000`. Pliku HTML nie otwieraj przez `file://`, bo wtedy odczyt `data.json` bywa blokowany.

## GitHub

Umieść zawartość tego katalogu w osobnym repozytorium. Włącz GitHub Pages dla gałęzi `main` i katalogu `/ (root)` oraz GitHub Actions. Uruchom workflow ręcznie po pierwszym wdrożeniu; później skan działa co sześć godzin. Nadaj Actions uprawnienia do zapisu zawartości repozytorium, jeśli organizacja je ogranicza. Skrypt korzysta tylko z biblioteki standardowej Python.

Skan dotyczy tylko widocznego tekstu czterech stron. Nie weryfikuje aktywności oferty, uprawnień w Polsce ani regulaminu. Strony oparte o JavaScript lub blokujące automatyczne pobieranie mogą zwrócić błąd lub niepełną treść. Szanuj warunki korzystania z serwisów.

HTML można później opakować jako aplikację Android WebView/PWA; APK nie jest potrzebne do działania na telefonie.

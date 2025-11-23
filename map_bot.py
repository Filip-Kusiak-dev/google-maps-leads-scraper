from playwright.sync_api import sync_playwright
import pandas as pd
import time
import datetime

def run():
    print("🚀 Uruchamiam bota Google Maps (Wersja 4.0 - FEED SCROLL)...")
    
    fraza = input("👉 Podaj frazę (np. Fryzjer Wrocław): ")
    if not fraza: fraza = "Pizzeria Warszawa"
    
    TARGET_COUNT = 20  # Ile chcesz wyników
    print(f"🎯 Cel: Pobranie minimum {TARGET_COUNT} wyników.")

    with sync_playwright() as p:
        # Start przeglądarki
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale="pl-PL") 
        page = context.new_page()

        print("🌍 Wchodzę na Google Maps...")
        page.goto("https://www.google.com/maps", timeout=60000)

        # Cookies
        try:
            page.get_by_role("button", name="Zaakceptuj wszystko").click(timeout=3000)
        except:
            try: page.get_by_role("button", name="Akceptuję").click(timeout=2000)
            except: pass

        # Wyszukiwanie
        try:
            page.locator("input#searchboxinput").fill(fraza)
            page.keyboard.press("Enter")
            print(f"✅ Szukam: {fraza}")
        except Exception as e:
            print(f"❌ Błąd wyszukiwania: {e}")
            return

        print("⏳ Czekam na pierwsze wyniki...")
        time.sleep(4)

        # ---------------------------------------------------------
        # 4. SCROLLOWANIE (METODA NA KONTENER "FEED")
        # ---------------------------------------------------------
        print("🔄 Rozpoczynam przewijanie listy...")
        
        last_count = 0
        scroll_attempts = 0
        
        # Namierzamy kontener, który ma pasek przewijania (Google oznacza go jako role="feed")
        feed = page.locator('div[role="feed"]')
        
        while True:
            # Sprawdź ile mamy artykułów
            listings = page.locator('div[role="article"]').all()
            count = len(listings)
            
            print(f"   📊 Załadowano: {count} / {TARGET_COUNT}")
            
            if count >= TARGET_COUNT:
                print("✅ Osiągnięto cel liczbowy!")
                break
            
            if count == last_count:
                scroll_attempts += 1
                if scroll_attempts > 5:
                    print("🛑 Koniec listy. Więcej nie ma.")
                    break
            else:
                scroll_attempts = 0 # Reset licznika
            
            last_count = count

            # --- OSTATECZNY SPOSÓB NA SCROLL ---
            # 1. Najedź myszką na ten konkretny pasek boczny
            try:
                feed.hover()
                # 2. Zakręć kółkiem bardzo mocno
                page.mouse.wheel(0, 3000)
                # 3. Poczekaj chwilę, żeby Google zdążyło wczytać nowe
                time.sleep(2)
                
                # Opcja zapasowa: JavaScript Scroll (Gdyby myszka zawiodła)
                # To komenda JS, która mówi "Przesuń suwak tego elementu na sam dół"
                feed.evaluate("element => element.scrollTop = element.scrollHeight")
            except Exception as e:
                print(f"⚠️ Problem ze scrollem: {e}")
                # Próba ratunkowa: scroll na całej stronie
                page.mouse.wheel(0, 3000)
            
            time.sleep(1.5)
        
        # ---------------------------------------------------------
        # 5. Pobieranie Danych
        # ---------------------------------------------------------
        
        listings = page.locator('div[role="article"]').all()
        final_count = min(TARGET_COUNT, len(listings))
        
        print(f"\n🏁 Rozpoczynam pobieranie szczegółów dla {final_count} firm...")

        data = []

        for i in range(final_count):
            try:
                # Odśwież listę
                listings = page.locator('div[role="article"]').all()
                if i >= len(listings): break
                
                listing = listings[i]
                nazwa = listing.get_attribute("aria-label") or "Brak nazwy"
                
                # Przewiń do elementu
                listing.scroll_into_view_if_needed()
                
                print(f"\n➡️ [{i+1}/{final_count}] Pobieram: {nazwa}")
                
                listing.click()
                time.sleep(1.5)

                # Szczegóły
                panel = page.locator('div[role="main"]')

                # Adres
                adres = "Brak"
                if panel.locator('button[data-item-id="address"]').count() > 0:
                    raw_adres = panel.locator('button[data-item-id="address"]').get_attribute("aria-label")
                    adres = raw_adres.replace("Adres: ", "").strip()

                # Telefon
                telefon = "Brak"
                btns = panel.locator("button[data-item-id]").all()
                for btn in btns:
                    item_id = btn.get_attribute("data-item-id")
                    if item_id and "phone:" in item_id:
                        telefon = btn.get_attribute("aria-label").replace("Telefon: ", "").strip()
                        break
                
                # WWW
                www = "Brak"
                if panel.locator('a[data-item-id="authority"]').count() > 0:
                    www = panel.locator('a[data-item-id="authority"]').get_attribute("href")

                # Ocena
                ocena = "Brak"
                try:
                    stars = panel.locator('span[role="img"]').first
                    aria = stars.get_attribute("aria-label")
                    if aria and ("gwiazd" in aria or "stars" in aria):
                        ocena = aria
                except: pass

                print(f"   📞 {telefon} | 🌐 {www}")

                data.append({
                    "Nazwa": nazwa,
                    "Adres": adres,
                    "Telefon": telefon,
                    "WWW": www,
                    "Ocena": ocena
                })

            except Exception as e:
                print(f"⚠️ Błąd przy pozycji {i}: {e}")
                continue

        # Zapis
        if data:
            timestamp = datetime.datetime.now().strftime("%H-%M-%S")
            filename = f"google_leady_{timestamp}.xlsx"
            
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            print(f"\n💾 Zapisano plik: {filename}")
        
        browser.close()

if __name__ == "__main__":
    run()
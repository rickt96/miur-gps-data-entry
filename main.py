import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


SOURCE_TIPI_CONTRATTI = [
    #"ANNUALE",
    "FINO AL TERMINE DELLE ATTIVITA' DIDATTICHE",
    "SPEZZONE"
]

SOURCE_CLASSI_CONCORSO = [
    "A027",
    "A026",
    "A020",
    #"A028"
]

SOURCE_SCUOLE = [
    "CESENA-FOPS010006", # L.S. RIGHI (con sede a Bagno di R.)
    "CESENA-FOPM05000N", # L.LINGUISTICO ALPI
    "CESENA-FOPC030008", # L.C. MONTI
    "CESENATICO-FOIS00400D", # I.I.S. LEONARDO DA VINCI
    "CESENA-FOTA03000R", # I.T. GARIBALDI/DA VINCI
    "CESENA-FOIS01100L", # I.I.S. PASCAL-COMANDINI
    "CESENA-FOTD02000L", # I.T. SERRA
    "CESENA-FORF03000N", # I.P. VERSARI/MACRELLI
    "SAVIGNANO SUL RUBICONE-FOIS001002", # I.I.S. MARIE CURIE
    "FORLI'-FOPS040002", # L.S. FULCIERI 
    "FORLI'-FOPC04000V", # L.C. MORGAGNI
    "FORLI'-FOIS00900L", # I.I.S. BARACCA
    "FORLI'-FOTE020004", # I.T. SAFFI/ALBERTI
    "FORLI'-FOTD010002", # I.T. MATTEUCCI 
    "FORLI'-FOSD020007", # L.ARTISTICO E MUSICALE A. CANOVA
    "FORLI'-FORF040008", # I.P. RUFFILLI 
    "FORLIMPOPOLI-FOIS00200T" # I.I.S. ARTUSI
]



# Funzione per inserire i dati nella modale
def process_entry(classe_concorso, preferenza, comune, codice_scuola, tipo_contratto):
    try:
        # Clicca il bottone "Apri modale aggiungi preferenza"
        apri_modale_button = driver.find_element(By.CLASS_NAME, "apri-modale-aggiungi-preferenza")
        apri_modale_button.click()

        # Attendi l'apertura della modale con id "modalConfirmRegister" e classe "show"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modalConfirmRegister.show")))

        # Seleziona il valore dalla select "graduatorie"
        graduatorie_select = Select(driver.find_element(By.ID, 'graduatorie'))
        graduatorie_select.select_by_value(classe_concorso)

        # Seleziona il valore dalla select "tipoContestoPreferenza"
        tipo_contesto_select = Select(driver.find_element(By.ID, 'tipoContestoPreferenza'))
        tipo_contesto_select.select_by_value(preferenza)

        # Attendere che nel DOM compaia un div con classe "panSede"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "panSede")))

        # Imposta il valore dalla select con classe "docCom"
        doccom_select = Select(driver.find_element(By.NAME, "codCom"))
        doccom_select.select_by_visible_text(comune)

        # Imposta il valore nell'input text con id "codScuUte"
        cod_scu_ute_input = driver.find_element(By.ID, "codScuUte")
        cod_scu_ute_input.clear()
        cod_scu_ute_input.send_keys(codice_scuola)

        # Clicca il bottone "Cerca sede"
        cerca_sede_button = driver.find_element(By.CLASS_NAME, "btn-cerca-sede")
        cerca_sede_button.click()

        # Attendi che nel DOM compaia un div con classe "tabella-ricerca"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tabella-ricerca")))

        time.sleep(2)

        # Cerca il tr nella table "dt-elenco-ricerca" con il secondo td con il valore inserito in "codScuUte"
        dt_elenco_ricerca_table = driver.find_element(By.ID, "dt-elenco-ricerca")
        tr_elements = dt_elenco_ricerca_table.find_elements(By.TAG_NAME, "tr")
        for tr_element in tr_elements:
            td_elements = tr_element.find_elements(By.TAG_NAME, "td")
            if len(td_elements) >= 2 and td_elements[1].text == codice_scuola:
                tr_element.click()
                break
        else:
            # Se non viene trovato alcun tr con il valore cercato, esci dalla funzione
            print(processed, ". ERRORE per ", classe_concorso, " - ", "S", " - ", comune, " - ", codice_scuola, " - ", tipo_contratto)
            return

        # Clicca il bottone "Conferma" nella modale
        btn_conferma_button = driver.find_element(By.CLASS_NAME, "btnConferma")
        btn_conferma_button.click()

        # Attendere 1 secondo
        time.sleep(2)

        # Imposta la proprietà "checked" a "false" per tutte le checkbox con classe "sel-preferenza-prop" nella table "dt-tipo-contratto"
        driver.execute_script('$(".sel-preferenza-prop").prop("checked", false)')

        # Cerca il tr nella table "dt-tipo-contratto" con il quarto td con il valore inserito in "tipoContestoSelect"
        dt_tipo_contratto_table = driver.find_element(By.ID, "dt-tipo-contratto")
        tr_elements = dt_tipo_contratto_table.find_elements(By.TAG_NAME, "tr")
        for tr_element in tr_elements:
            td_elements = tr_element.find_elements(By.TAG_NAME, "td")
            if len(td_elements) >= 4 and td_elements[4].text == tipo_contratto:
                tr_element.click()
                break

        time.sleep(1)

        # Seleziona la checkbox con id "flgCoeEqu"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "flgCoeEqu")))
        driver.execute_script('$("#flgCoeEqu").prop("checked", true)')

        # Clicca il bottone "Conferma" nella modale
        btn_conferma_button = driver.find_element(By.CLASS_NAME, "btnConferma")
        btn_conferma_button.click()

        # Attendi che la modale con id "modalConfirmRegister" non contenga più la classe "show"
        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, "#modalConfirmRegister.show")))

        print(processed, ". OK - ", classe_concorso, " - ", "S", " - ", comune, " - ", codice_scuola, " - ", tipo_contratto)
        
        time.sleep(1)

    except:
        print(processed, ". EXCEPTION per ", classe_concorso, " - ", "S", " - ", comune, " - ", codice_scuola, " - ", tipo_contratto)


# Inizializza il webdriver (sostituisci "percorso/al/chromedriver" con il percorso al tuo driver di Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--remote-debugging-port=9222")
options.add_argument("disable-extensions")
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
#options.add_argument('--user-data-dir=C:\\Users\\Riccardo\\AppData\\Local\\Google\\Chrome\\User Data\\')
driver = webdriver.Chrome(options=options)

# Limite di inserimenti
insert_limit = 150 # int(driver.find_element_by_id("label_id").text)
processed = 0

try:
    # Apri la pagina web
    driver.get("https://graduatorie.pubblica.istruzione.it/snpd-ins-domanda-polis-web/private/index/confermaInfo")

    for tipo_contratto in SOURCE_TIPI_CONTRATTI:
        for classe_concorso in SOURCE_CLASSI_CONCORSO:
            for comune_scuola in SOURCE_SCUOLE:

                # Verifica threshold
                datatables_info_lbl = driver.find_element(By.ID, 'dt-elenco-preferenze_info')
                if datatables_info_lbl.text == "Totale preferenze: 150":
                    break

                # Inserimento entry
                comune = comune_scuola.split("-")[0]
                codice_scuola = comune_scuola.split("-")[1]
                process_entry(classe_concorso, "S", comune, codice_scuola, tipo_contratto)
                processed = processed + 1

finally:
    # Chiudi il webdriver alla fine dell'esecuzione
    driver.quit()

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

USER ='5249657'
PW =''
MAX_WAIT = 20
NOMBRE_COMERCIO = 'Diego larrea - freelancer'
URL = None


OPERACIONES = [
    {
        'listId': 3465,
        'tipo': 'ATLAS',
        'ci': '5249657',
        'cuenta': '1241292',
        'monto': '5000'
    },
    {
        'listId': 3465,
        'tipo': 'ATLAS',
        'ci': '5249657',
        'cuenta': '1241292',
        'monto': '6000'
    },
    {
        'listId': 3465,
        'tipo': 'ATLAS',
        'ci': '5249657',
        'cuenta': '1241292',
        'monto': '7000'
    },
    {
        'listId': 3465,
        'tipo': 'ATLAS',
        'ci': '5249657',
        'cuenta': '1241292',
        'monto': '10000'
    },
]

def login():
    username = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'input-0')))
    password = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'input-2')))

    username.send_keys(USER)  # Ingresa tu usuario
    password.send_keys(PW)  # Ingresa tu contraseña

    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ingresar')]"))).click()

def abrirSucursal():
    WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.v-list-item'))).click()

def pantallaInicio():
    # Click en otro momento overlay del inicio
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'En otro momento')]"))).click()

    # Click en servicios
    WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'services'))).click()

def buscadorDeServicios(servicio, id):
    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'inputRaw')))
    textInput.send_keys(Keys.CONTROL + "a")  # Selecciona todo el texto
    textInput.send_keys(Keys.BACKSPACE)  # Borra el texto seleccionado
    textInput.send_keys(servicio)

    WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, id))).click()

def opAtlas(ci, nroCuenta, monto):
    # Paso 1
    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'p_01_0')))
    textInput.send_keys(ci)
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Siguiente')]"))).click()
    
    # Paso 2
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, f"//h3[contains(., '{nroCuenta}')]"))).click()
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Siguiente')]"))).click()

    # Paso 3
    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'amount')))
    textInput.clear()
    textInput.send_keys(0)
    textInput.send_keys(Keys.CONTROL + "a")  # Selecciona todo el texto
    textInput.send_keys(Keys.BACKSPACE)  # Borra el texto seleccionado
    textInput.send_keys(monto)
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirmar y Pagar')]"))).click()

def opEko(ci, nroCuenta, monto, depositante):
    # Paso 1
    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'p_01_0')))
    textInput.send_keys(ci)
    
    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'p_02_0')))
    textInput.send_keys(nroCuenta)

    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'p_03_0')))
    textInput.send_keys(depositante)

    textInput = WebDriverWait(driver, MAX_WAIT).until(EC.presence_of_element_located((By.ID, 'p_04_0')))
    textInput.send_keys(monto)

    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Siguiente')]"))).click()
    
    # Paso 2
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//h5[contains(., 'DIEGO GABRIEL LARREA BARRIOS')]"))).click()
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Siguiente')]"))).click()

    # Paso 3
    WebDriverWait(driver, MAX_WAIT).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirmar y Pagar')]"))).click()

chrome_options = Options()
#chrome_options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser in action
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = Service('./chromedriver.exe')

driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

driver.get("https://app.acapuedo.com/")

login()

abrirSucursal()

pantallaInicio()

URL = driver.current_url
URL = URL.replace('/inicio', '/services')
print(URL)

for operacion in OPERACIONES:
    tipo = operacion['tipo']
    ci = operacion['ci']
    cuenta = operacion['cuenta']
    monto = operacion['monto']
    listId = operacion['listId']
    
    print(tipo)

    if tipo == 'ATLAS':
        buscadorDeServicios(tipo, listId)
        opAtlas(ci, cuenta, monto)
    elif tipo == 'EKO':
        depositante = operacion['depositante']
        buscadorDeServicios(tipo, listId)
        opEko(ci, cuenta, monto, depositante)

    time.sleep(5)
    driver.get(URL)
    time.sleep(5)
    driver.refresh()
    time.sleep(5)

time.sleep(10)

driver.close()
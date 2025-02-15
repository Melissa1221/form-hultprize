from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
import os
from datetime import datetime
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import logging
import traceback
import sys
from selenium.webdriver.common.action_chains import ActionChains

# Configurar logging
def setup_logging():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    # Configurar el logger principal
    logger = logging.getLogger('automation')
    logger.setLevel(logging.DEBUG)
    
    # Crear formateador detallado
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Handler para archivo
    file_handler = logging.FileHandler(f"{log_folder}/automation_{timestamp}.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Cargar variables de entorno
load_dotenv()

class FormAutomation:
    def __init__(self):
        self.logger = setup_logging()
        self.driver = None
        self.excel_path = os.getenv('EXCEL_PATH')
        self.screenshots_folder = os.getenv('SCREENSHOT_FOLDER', 'error_screenshots')
        self.form_url = os.getenv('FORM_URL', 'http://localhost:3000')
        self.wait_time = int(os.getenv('WAIT_TIME', 2))
        self.default_phone_code = '+51'  # Código por defecto para Perú
        
        # Mapeo de países a códigos ISO
        self.country_codes = {
            'Perú': 'PE',
            'Peru': 'PE',
            'México': 'MX',
            'Mexico': 'MX',
            'Estados Unidos': 'US',
            'United States': 'US',
            'España': 'ES',
            'Spain': 'ES',
            # Agregar más países según sea necesario
        }
        
        # Mapeo de universidades a sus IDs
        self.university_codes = {
            'Pontificia Universidad Católica Del Perú': '001Dn00000W4wwYIAR',
            'Universidad De Lima': '001Dn00000W4vw7IAB',
            'Universidad Del Pacífico': '001Dn00000W4vwfIAB',
            'Universidad Nacional Mayor De San Marcos': '001Dn00000W4vypIAB',
            'Universidad Nacional De Ingeniería': '001Dn00000W4vyEIAR',
            'UPC - Universidad Peruana De Ciencias Aplicadas': '001Dn00000W4vz9IAB',
            'UTEC - Universidad de Ingeniería y Tecnología': '001Dn00000W4vwWIAR',
            'Other': 'Other'
        }
        
        # Mapeo de fuentes de información a IDs
        self.lead_source_mapping = {
            'Country Coordinator': 'countryCoordinator',
            'Friend': 'friend',
            'Hult Prize Alumni': 'alumni',
            'Hult Prize Campus Director': 'campusDirector',
            'Hult Prize Team - Direct Communication': 'directCommunication',
            'Hult Prize Website': 'website',
            'Internet Search': 'internetSearch',
            'Social Media - Facebook': 'facebook',
            'Social Media - Instagram': 'instagram',
            'Social Media - LinkedIn': 'linkedin',
            'Social Media - Other': 'otherSocialMedia',
            'University Rep': 'universityRep',
            'Other': 'other'
        }
        
        # Definir columnas requeridas
        self.required_columns = [
            'startup_name',
            'country',
            'city',
            'university',
            'captain_first_name',
            'captain_last_name',
            'captain_email',
            'captain_phone',
            'member2_first_name',
            'member2_last_name',
            'member2_email',
            'member2_phone',
            'sdg',
            'is_competitor',
            'lead_source'
        ]
        
        # Mapeo de nombres de columnas
        self.column_mapping = {
            'captain_phone': 'captain_phone_code',
            'member2_phone': 'member2_phone_code',
            'member3_phone': 'member3_phone_code',
            'member4_phone': 'member4_phone_code'
        }
        
        self.logger.info(f"Inicializando automatización con:")
        self.logger.info(f"- Excel Path: {self.excel_path}")
        self.logger.info(f"- Form URL: {self.form_url}")
        self.logger.info(f"- Wait Time: {self.wait_time} segundos")
        
        # Crear carpeta de screenshots si no existe
        if not os.path.exists(self.screenshots_folder):
            os.makedirs(self.screenshots_folder)
            self.logger.info(f"Carpeta de screenshots creada: {self.screenshots_folder}")

    def setup_driver(self):
        """Inicializar el webdriver con configuraciones mejoradas"""
        try:
            self.logger.info("Configurando Chrome WebDriver...")
            
            # Configuraciones adicionales para Chrome
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            try:
                # Usar selenium-manager (método más nuevo y robusto)
                self.logger.info("Intentando inicializar Chrome con selenium-manager...")
                self.driver = webdriver.Chrome(options=options)
                self.driver.implicitly_wait(10)
                self.logger.info("WebDriver configurado exitosamente con selenium-manager")
                return True
                
            except Exception as e:
                self.logger.error(f"Error con selenium-manager: {str(e)}")
                
                try:
                    # Intentar con webdriver_manager
                    self.logger.info("Intentando con webdriver_manager...")
                    from webdriver_manager.chrome import ChromeDriverManager
                    from webdriver_manager.core.utils import ChromeType
                    from selenium.webdriver.chrome.service import Service
                    
                    # Forzar la descarga de la última versión
                    os.environ['WDM_LOCAL'] = '0'
                    os.environ['WDM_SSL_VERIFY'] = '0'
                    
                    service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                    self.driver.implicitly_wait(10)
                    self.logger.info("WebDriver configurado exitosamente con webdriver_manager")
                    return True
                    
                except Exception as wdm_error:
                    self.logger.error(f"Error con webdriver_manager: {str(wdm_error)}")
                    
                    try:
                        # Último intento: Descarga directa
                        self.logger.info("Intentando descarga directa del ChromeDriver...")
                        import requests
                        import zipfile
                        import io
                        import subprocess
                        
                        # Obtener versión de Chrome
                        chrome_version = subprocess.check_output(
                            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                            stderr=subprocess.DEVNULL
                        ).decode('utf-8').split()[-1]
                        
                        major_version = chrome_version.split('.')[0]
                        self.logger.info(f"Versión de Chrome detectada: {chrome_version}")
                        
                        # URL de descarga directa
                        download_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
                        latest_version = requests.get(download_url).text.strip()
                        
                        chromedriver_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip"
                        self.logger.info(f"Descargando ChromeDriver desde: {chromedriver_url}")
                        
                        # Descargar y extraer ChromeDriver
                        response = requests.get(chromedriver_url)
                        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
                        
                        # Crear directorio para ChromeDriver si no existe
                        driver_dir = os.path.join(os.path.dirname(__file__), "chromedriver")
                        if not os.path.exists(driver_dir):
                            os.makedirs(driver_dir)
                        
                        # Extraer ChromeDriver
                        zip_file.extractall(driver_dir)
                        chromedriver_path = os.path.join(driver_dir, "chromedriver.exe")
                        
                        self.logger.info(f"ChromeDriver extraído en: {chromedriver_path}")
                        
                        # Inicializar el driver con el ChromeDriver descargado
                        service = Service(executable_path=chromedriver_path)
                        self.driver = webdriver.Chrome(service=service, options=options)
                        self.driver.implicitly_wait(10)
                        self.logger.info("WebDriver configurado exitosamente con descarga directa")
                        return True
                        
                    except Exception as direct_error:
                        self.logger.error(f"Error en descarga directa: {str(direct_error)}")
                        raise
                
        except Exception as e:
            self.logger.error(f"Error al configurar el driver: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Información de diagnóstico
            self.logger.error("\nInformación de diagnóstico:")
            try:
                import platform
                self.logger.error(f"Sistema Operativo: {platform.platform()}")
                self.logger.error(f"Python Version: {platform.python_version()}")
                self.logger.error(f"Selenium Version: {webdriver.__version__}")
                
                # Verificar Chrome
                try:
                    chrome_version = subprocess.check_output(
                        ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                        stderr=subprocess.DEVNULL
                    ).decode('utf-8')
                    self.logger.error(f"Chrome Version: {chrome_version.split()[-1]}")
                except:
                    self.logger.error("No se pudo determinar la versión de Chrome")
                
            except Exception as diagnostic_error:
                self.logger.error(f"Error al recopilar información de diagnóstico: {str(diagnostic_error)}")
            
            return False

    def wait_for_element(self, by, value, timeout=10):
        """Esperar a que un elemento esté presente y visible"""
        try:
            self.logger.debug(f"Esperando elemento: {by}={value}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Timeout esperando elemento: {by}={value}")
            return None

    def take_error_screenshot(self, error_description):
        """Tomar screenshot cuando ocurre un error"""
        try:
            if not os.path.exists(self.screenshots_folder):
                os.makedirs(self.screenshots_folder)
                self.logger.info(f"Carpeta de screenshots creada: {self.screenshots_folder}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.screenshots_folder, f"error_{timestamp}.png")
            
            # Asegurarse de que el driver está inicializado
            if self.driver:
                self.driver.save_screenshot(filename)
                
                # Guardar también el error en un archivo de texto
                error_file = os.path.join(self.screenshots_folder, f"error_{timestamp}.txt")
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Error Description: {error_description}\n")
                    f.write(f"URL: {self.driver.current_url}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Page Source:\n{self.driver.page_source}\n")
                
                self.logger.info(f"Screenshot guardado: {filename}")
                self.logger.info(f"Detalles del error guardados: {error_file}")
                return filename
            else:
                self.logger.error("No se pudo tomar screenshot: WebDriver no inicializado")
                return None
                
        except Exception as e:
            self.logger.error(f"Error al tomar screenshot: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None

    def safe_send_keys(self, element_id, value):
        """Enviar texto de forma segura a un elemento"""
        try:
            self.logger.debug(f"Intentando enviar texto a {element_id}: {value}")
            element = self.wait_for_element(By.ID, element_id)
            if element:
                element.clear()
                element.send_keys(str(value))
                self.logger.debug(f"Texto enviado exitosamente a {element_id}")
                return True
            self.logger.warning(f"No se encontró el elemento {element_id}")
            return False
        except Exception as e:
            self.logger.error(f"Error al enviar texto a {element_id}: {str(e)}")
            return False

    def safe_select_option(self, element_id, value):
        """Seleccionar una opción de un select de forma segura"""
        try:
            self.logger.debug(f"Intentando seleccionar opción en {element_id}: {value}")
            element = self.wait_for_element(By.ID, element_id)
            if element:
                select = Select(element)
                
                # Imprimir todas las opciones disponibles
                if element_id == "university":
                    self.logger.info("Opciones disponibles en el select:")
                    for option in select.options:
                        self.logger.info(f"- value: '{option.get_attribute('value')}', text: '{option.text}'")
                    # Para universidades, seleccionar por texto visible
                    select.select_by_visible_text(str(value))
                else:
                    # Para otros campos, seleccionar por valor
                    select.select_by_value(str(value))
                    
                self.logger.debug(f"Opción seleccionada exitosamente en {element_id}")
                return True
            self.logger.warning(f"No se encontró el elemento select {element_id}")
            return False
        except Exception as e:
            self.logger.error(f"Error al seleccionar opción en {element_id}: {str(e)}")
            return False

    def select_university(self, element_id, university_name, other_input_id):
        """Helper function para seleccionar universidad"""
        try:
            if university_name is None or pd.isna(university_name):
                self.logger.error(f"No se encontró universidad para el elemento {element_id}")
                return False

            self.logger.info(f"Intentando seleccionar universidad '{university_name}' en {element_id}")
            university_select = Select(self.driver.find_element(By.ID, element_id))
            
            # Imprimir todas las opciones disponibles
            self.logger.info("Opciones disponibles en el select:")
            for option in university_select.options:
                self.logger.info(f"- value: '{option.get_attribute('value')}', text: '{option.text}'")
            
            # Primero intentamos seleccionar directamente
            try:
                university_select.select_by_visible_text(university_name)
                self.logger.info(f"Universidad seleccionada exitosamente: {university_name}")
                return True
            except:
                # Si falla, intentamos encontrar una coincidencia parcial
                options = [o.text for o in university_select.options]
                self.logger.info(f"Buscando coincidencia parcial para: {university_name}")
                
                matches = [o for o in options if university_name.lower() in o.lower()]
                
                if matches:
                    self.logger.info(f"Coincidencia encontrada: {matches[0]}")
                    university_select.select_by_visible_text(matches[0])
                    return True
                else:
                    # Si no hay coincidencias, usar "Other"
                    self.logger.info(f"No se encontraron coincidencias, usando 'Other'")
                    university_select.select_by_visible_text("Other")
                    other_input = self.driver.find_element(By.ID, other_input_id)
                    other_input.clear()
                    other_input.send_keys(university_name)
                    return True
                
        except Exception as e:
            self.logger.error(f"Error al seleccionar universidad: {str(e)}")
            return False

    def safe_click(self, element, element_name="elemento"):
        """Intenta hacer click en un elemento de manera segura usando diferentes métodos"""
        try:
            # Primer intento: click normal
            element.click()
            return True
        except Exception as e1:
            self.logger.debug(f"Click normal falló para {element_name}: {str(e1)}")
            try:
                # Segundo intento: scroll y click
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                element.click()
                return True
            except Exception as e2:
                self.logger.debug(f"Click con scroll falló para {element_name}: {str(e2)}")
                try:
                    # Tercer intento: click con JavaScript
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception as e3:
                    self.logger.error(f"Todos los intentos de click fallaron para {element_name}")
                    self.logger.error(f"Error final: {str(e3)}")
                    return False

    def wait_and_click(self, by, value, timeout=10, element_name="elemento"):
        """Espera por un elemento y hace click de manera segura"""
        try:
            element = self.wait_for_element(by, value, timeout)
            if element and self.safe_click(element, element_name):
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error al esperar y hacer click en {element_name}: {str(e)}")
            return False

    def fill_form(self, row_data):
        """Llenar el formulario con datos del Excel"""
        try:
            self.logger.info(f"Iniciando llenado de formulario para startup: {row_data['startup_name']}")
            
            # Información Básica
            if not self.safe_send_keys("startupName", row_data['startup_name']):
                raise Exception("Error al llenar el nombre del startup")
            
            # Selección de País (usando el código ISO)
            country_name = row_data['country']
            country_code = self.country_codes.get(country_name)
            if not country_code:
                raise Exception(f"País no encontrado en el mapeo: {country_name}")
            
            if not self.safe_select_option("country", country_code):
                raise Exception("Error al seleccionar el país")
            
            # Ciudad
            if not self.safe_select_option("city", row_data['city']):
                raise Exception("Error al seleccionar la ciudad")
            if row_data['city'] == "Other":
                if not self.safe_send_keys("otherCity", row_data['other_city']):
                    raise Exception("Error al llenar otra ciudad")

            # Universidad (usando el nombre directamente)
            university_name = row_data['university']
            if not self.safe_select_option("university", university_name):
                raise Exception("Error al seleccionar la universidad")
            if university_name == "Other":
                if not self.safe_send_keys("otherUniversity", row_data.get('other_university', '')):
                    raise Exception("Error al llenar otra universidad")

            # Información del Capitán
            self.logger.info("Llenando información del capitán")
            captain_fields = {
                "firstName": row_data['captain_first_name'],
                "lastName": row_data['captain_last_name'],
                "email": row_data['captain_email']
            }
            
            for field_id, value in captain_fields.items():
                if not self.safe_send_keys(field_id, value):
                    raise Exception(f"Error al llenar {field_id} del capitán")

            # Código de teléfono del capitán (siempre +51)
            if not self.safe_select_option("phoneCode", self.default_phone_code):
                raise Exception("Error al seleccionar el código de teléfono del capitán")
            if not self.safe_send_keys("phone", str(row_data['captain_phone'])):
                raise Exception("Error al llenar el teléfono del capitán")

            # Universidad diferente para el capitán
            if pd.notna(row_data.get('captain_different_university')) and row_data['captain_different_university']:
                self.logger.info("Capitán tiene universidad diferente")
                self.driver.find_element(By.ID, "differentUniversity1").click()
                time.sleep(1)
                
                # Obtener el código del país
                country_name = row_data['country']
                country_code = self.country_codes.get(country_name)
                if not country_code:
                    raise Exception(f"País no encontrado en el mapeo: {country_name}")
                
                self.logger.info(f"Seleccionando país: {country_name} (código: {country_code})")
                
                # Seleccionar país y ciudad
                if not self.safe_select_option("memberCountry1", country_code):
                    raise Exception(f"Error al seleccionar el país {country_name}")

                time.sleep(1)  # Esperar a que carguen las ciudades
                
                if not self.safe_select_option("memberCity1", row_data['city']):
                    raise Exception(f"Error al seleccionar la ciudad {row_data['city']}")

                # Usar la universidad del Excel
                if not self.select_university("memberUniversity1", "Universidad Antonio Ruiz de Montoya", "otherUniversity1"):
                    raise Exception("Error al seleccionar universidad del capitán")

            # Universidad diferente para el miembro 2
            if pd.notna(row_data.get('member2_different_university')) and row_data['member2_different_university']:
                self.logger.info("Miembro 2 tiene universidad diferente")
                self.driver.find_element(By.ID, "differentUniversity2").click()
                time.sleep(1)
                
                # Seleccionar país y ciudad
                if not self.safe_select_option("memberCountry2", country_code):
                    raise Exception(f"Error al seleccionar el país {country_name}")

                time.sleep(1)
                
                if not self.safe_select_option("memberCity2", row_data['city']):
                    raise Exception(f"Error al seleccionar la ciudad {row_data['city']}")

                # Usar la universidad del Excel
                if not self.select_university("memberUniversity2", "Universidad Nacional Del Callao", "otherUniversity2"):
                    raise Exception("Error al seleccionar universidad del miembro 2")

            # Miembros del equipo (2-4)
            for member_num in range(2, 5):
                if pd.notna(row_data.get(f'member{member_num}_first_name')):
                    self.logger.info(f"Llenando información del miembro {member_num}")
                    self.fill_team_member(member_num, row_data)

            # Selección de SDG
            if not self.safe_select_option("sdg", row_data['sdg']):
                raise Exception("Error al seleccionar SDG")

            # Experiencia previa
            if pd.notna(row_data.get('is_competitor')) and row_data.get('is_competitor'):
                self.logger.info("Marcando experiencia previa como competidor")
                if not self.wait_and_click(By.ID, "competitor", element_name="checkbox de competidor"):
                    raise Exception("No se pudo marcar el checkbox de competidor")

            # Cómo se enteró
            lead_source = row_data['lead_source']
            self.logger.info(f"Seleccionando fuente de información: {lead_source}")
            
            # Usar XPath para encontrar el radio button por su valor
            radio_xpath = f"//input[@type='radio'][@value='{lead_source}']"
            try:
                radio_button = self.driver.find_element(By.XPATH, radio_xpath)
                radio_button.click()
            except Exception as e:
                self.logger.error(f"No se pudo encontrar el radio button para: {lead_source}")
                self.logger.error("Radio buttons disponibles:")
                radio_buttons = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
                for rb in radio_buttons:
                    self.logger.error(f"- value: {rb.get_attribute('value')}")
                raise Exception(f"Error al seleccionar fuente de información: {lead_source}")

            # Confirmaciones
            self.logger.info("Marcando confirmaciones")
            if not self.wait_and_click(By.ID, "teamConfirmation", element_name="confirmación de equipo"):
                raise Exception("No se pudo marcar la confirmación de equipo")
            
            if not self.wait_and_click(By.ID, "termsConditions", element_name="términos y condiciones"):
                raise Exception("No se pudo marcar los términos y condiciones")

            # Enviar formulario
            self.logger.info("Enviando formulario")
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()

            # Esperar a que se procese el envío
            self.logger.info(f"Esperando {self.wait_time} segundos para procesamiento")
            time.sleep(self.wait_time)

            self.logger.info("Formulario enviado exitosamente")
            return True, None

        except Exception as e:
            self.logger.error(f"Error al llenar formulario: {str(e)}")
            self.logger.error(traceback.format_exc())
            screenshot_path = self.take_error_screenshot(str(e))
            return False, f"Error: {str(e)}\nScreenshot saved at: {screenshot_path}"

    def fill_team_member(self, member_num, row_data):
        try:
            self.logger.info(f"\n=== Iniciando llenado de miembro {member_num} ===")
            
            if member_num == 1:
                self.logger.info("DEBUG - Llenando campos del capitán")
                
                # Campos básicos del capitán
                self.driver.find_element(By.ID, "firstName1").send_keys(row_data['captain_first_name'])
                self.driver.find_element(By.ID, "lastName1").send_keys(row_data['captain_last_name'])
                self.driver.find_element(By.ID, "email1").send_keys(row_data['captain_email'])
                
                # Teléfono
                phone_select = Select(self.driver.find_element(By.ID, "phoneCode1"))
                phone_select.select_by_visible_text("(+51) Peru")
                self.driver.find_element(By.ID, "phone1").send_keys(row_data['captain_phone'])
                
                # Verificar universidad del capitán
                captain_university = row_data.get('captain_university')
                main_university = row_data.get('university')
                
                self.logger.info("=== DEBUG CAPTAIN UNIVERSITY INFO ===")
                self.logger.info(f"Universidad principal: {main_university}")
                self.logger.info(f"Universidad del capitán: {captain_university}")
                
                # Si el capitán tiene una universidad diferente
                if pd.notna(captain_university) and captain_university.strip():
                    self.logger.info(f"Capitán tiene universidad diferente: {captain_university}")
                    
                    try:
                        # Marcar checkbox
                        checkbox = self.driver.find_element(By.ID, "differentUniversity1")
                        time.sleep(1)
                        
                        # Scroll y click
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", checkbox)
                        time.sleep(1)
                        
                        # Verificar si se marcó
                        if checkbox.is_selected():
                            self.logger.info("Checkbox marcado exitosamente")
                            
                            # Seleccionar país
                            country_code = self.country_codes.get(row_data['country'])
                            self.safe_select_option("memberCountry1", country_code)
                            time.sleep(1)
                            
                            # Seleccionar ciudad
                            self.safe_select_option("memberCity1", row_data['city'])
                            time.sleep(1)
                            
                            # Seleccionar universidad
                            self.select_university("memberUniversity1", captain_university, "otherUniversity1")
                        else:
                            self.logger.error("No se pudo marcar el checkbox del capitán")
                    
                    except Exception as e:
                        self.logger.error(f"Error procesando universidad del capitán: {str(e)}")
                        raise
                else:
                    self.logger.info("Capitán usa la universidad principal")
                
                self.logger.info("=== Fin procesamiento universidad capitán ===")
                
            else:
                # ... resto del código para otros miembros ...
                pass

            self.logger.info(f"=== Finalizado llenado de miembro {member_num} ===\n")

        except Exception as e:
            self.logger.error(f"Error al llenar información del miembro {member_num}: {str(e)}")
            self.logger.error(f"DEBUG - Valores disponibles en Excel: {row_data}")
            raise

    def validate_excel_columns(self, df):
        """Validar que el Excel tenga todas las columnas necesarias"""
        required_columns = [
            'startup_name',
            'country',
            'city',
            'university',
            'captain_first_name',
            'captain_last_name',
            'captain_email',
            'captain_phone',
            'captain_university',
            'member2_first_name',
            'member2_last_name',
            'member2_email',
            'member2_phone',
            'member2_university',
            'member3_first_name',
            'member3_last_name',
            'member3_email',
            'member3_phone',
            'member3_university',
            'member4_first_name',
            'member4_last_name',
            'member4_email',
            'member4_phone',
            'member4_university'
        ]

        # Columnas opcionales que no son requeridas
        optional_columns = [
            'captain_different_university',
            'member2_different_university',
            'member3_different_university',
            'member4_different_university'
        ]

        missing_required = [col for col in required_columns if col not in df.columns]
        missing_optional = [col for col in optional_columns if col not in df.columns]

        if missing_required:
            self.logger.error("Columnas requeridas faltantes:")
            for col in missing_required:
                self.logger.error(f"- {col}")
            raise Exception("Faltan columnas requeridas en el Excel")

        if missing_optional:
            self.logger.warning("Columnas opcionales faltantes (no crítico):")
            for col in missing_optional:
                self.logger.warning(f"- {col}")

        self.logger.info("Validación de columnas completada")

    def process_excel(self):
        """Procesar el archivo Excel y llenar formularios"""
        try:
            self.logger.info(f"Leyendo archivo Excel: {self.excel_path}")
            
            if not os.path.exists(self.excel_path):
                self.logger.error(f"El archivo Excel no existe en la ruta: {self.excel_path}")
                raise FileNotFoundError(f"No se encontró el archivo: {self.excel_path}")
                
            try:
                df = pd.read_excel(self.excel_path)
            except Exception as e:
                self.logger.error(f"Error al leer el archivo Excel: {str(e)}")
                self.logger.error("Verifica que el archivo no esté corrupto o en uso")
                raise

            self.logger.info(f"Excel leído exitosamente. Columnas encontradas: {df.columns.tolist()}")
            
            # Validar columnas del Excel
            self.validate_excel_columns(df)
            
            # Verificar si hay datos
            if len(df) == 0:
                self.logger.error("El archivo Excel no contiene datos")
                raise Exception("El archivo Excel está vacío")

            results = []
            
            if not self.setup_driver():
                raise Exception("No se pudo inicializar el driver")
            
            total_rows = len(df)
            self.logger.info(f"Total de registros a procesar: {total_rows}")
            
            for index, row in df.iterrows():
                # Verificar valores nulos en campos requeridos
                null_fields = [col for col in self.required_columns if col in row.index and pd.isna(row[col])]
                if null_fields:
                    self.logger.warning(f"Fila {index + 2} tiene campos requeridos vacíos: {null_fields}")
                    continue

                self.logger.info(f"\nProcesando registro {index + 1} de {total_rows}")
                self.logger.info(f"Startup: {row['startup_name']}")
                
                try:
                    self.driver.get(self.form_url)
                    self.logger.info(f"Navegando a: {self.form_url}")
                    time.sleep(self.wait_time)
                    
                    success, error = self.fill_form(row)
                    
                    result = {
                        'row_number': index + 2,
                        'startup_name': row['startup_name'],
                        'status': 'Success' if success else 'Failed',
                        'error': error if not success else None,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    results.append(result)
                    
                    self.logger.info(f"Estado: {'Éxito' if success else 'Error'}")
                    if error:
                        self.logger.error(f"Error: {error}")
                    
                    time.sleep(self.wait_time)
                    
                except Exception as e:
                    self.logger.error(f"Error procesando registro {index + 1}: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    screenshot_path = self.take_error_screenshot(str(e))
                    error_msg = f"Error: {str(e)}\nScreenshot saved at: {screenshot_path}"
                    self.logger.error(error_msg)
                    results.append({
                        'row_number': index + 2,
                        'startup_name': row['startup_name'] if 'startup_name' in row else f"Fila {index + 2}",
                        'status': 'Failed',
                        'error': error_msg,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error crítico en process_excel: {str(e)}")
            self.logger.error(traceback.format_exc())
            return []
            
        finally:
            if self.driver:
                self.logger.info("Cerrando WebDriver")
                self.driver.quit()

    def save_results(self, results):
        """Guardar resultados en Excel"""
        try:
            self.logger.info("Guardando resultados en Excel")
            results_df = pd.DataFrame(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"automation_results_{timestamp}.xlsx"
            results_df.to_excel(output_file, index=False)
            self.logger.info(f"Resultados guardados en: {output_file}")
            return output_file
        except Exception as e:
            self.logger.error(f"Error al guardar resultados: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None

def main():
    logger = logging.getLogger('automation')
    try:
        logger.info("=== Iniciando proceso de automatización ===")
        automation = FormAutomation()
        results = automation.process_excel()
        
        if results:
            output_file = automation.save_results(results)
            
            # Imprimir resumen
            total = len(results)
            successful = sum(1 for r in results if r['status'] == 'Success')
            failed = total - successful
            
            logger.info("\n=== Resumen de Automatización ===")
            logger.info(f"Total de registros procesados: {total}")
            logger.info(f"Envíos exitosos: {successful}")
            logger.info(f"Envíos fallidos: {failed}")
            logger.info(f"Tasa de éxito: {(successful/total)*100:.2f}%")
            
            if output_file:
                logger.info(f"\nReporte detallado guardado en: {output_file}")
        else:
            logger.error("\nNo se procesaron registros debido a errores")
            
    except Exception as e:
        logger.error(f"\nError crítico en la automatización: {str(e)}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

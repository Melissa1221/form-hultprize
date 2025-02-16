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
        # Forzar la URL de Hult Prize independientemente del .env
        self.form_url = 'https://www.hultprize.org/startup-pre-registration-is-now-open/'
        self.logger.info(f"URL del formulario configurada a: {self.form_url}")
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
                
                # Imprimir todas las opciones disponibles para diagnóstico
                self.logger.info(f"Opciones disponibles en {element_id}:")
                for option in select.options:
                    self.logger.info(f"- value: '{option.get_attribute('value')}', text: '{option.text}'")
                
                try:
                    # Intentar primero por valor
                    self.logger.info(f"Intentando seleccionar por valor: {value}")
                    select.select_by_value(str(value))
                except:
                    try:
                        # Si falla, intentar por texto visible
                        self.logger.info(f"Intentando seleccionar por texto visible: {value}")
                        select.select_by_visible_text(str(value))
                    except:
                        # Si ambos fallan, buscar coincidencia parcial
                        self.logger.info("Buscando coincidencia parcial...")
                        found = False
                        for option in select.options:
                            if str(value).lower() in option.text.lower() or str(value).lower() in option.get_attribute('value').lower():
                                self.logger.info(f"Coincidencia encontrada: {option.text}")
                                select.select_by_value(option.get_attribute('value'))
                                found = True
                                break
                        if not found:
                            raise Exception(f"No se encontró opción que coincida con: {value}")
                
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

    def fill_form(self, row_data):
        """Llenar el formulario con datos del Excel"""
        try:
            self.logger.info(f"Iniciando llenado de formulario para startup: {row_data['startup_name']}")
            
            # Esperar a que la página se cargue completamente
            self.logger.info("Esperando a que la página se cargue completamente...")
            time.sleep(10)  # Dar más tiempo para la carga inicial
            
            # Función helper para marcar checkbox
            def mark_checkbox(checkbox_id, should_check=True):
                try:
                    # Esperar a que el checkbox sea clickeable
                    checkbox = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, checkbox_id))
                    )
                    
                    # Scroll al checkbox con offset para evitar problemas de navegación
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", 
                        checkbox
                    )
                    time.sleep(2)  # Esperar a que el scroll termine
                    
                    if should_check and not checkbox.is_selected():
                        # Intentar múltiples métodos para marcar el checkbox
                        try:
                            # Método 1: JavaScript directo
                            self.driver.execute_script(
                                """
                                arguments[0].click();
                                arguments[0].checked = true;
                                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                                """, 
                                checkbox
                            )
                        except:
                            try:
                                # Método 2: ActionChains
                                actions = ActionChains(self.driver)
                                actions.move_to_element(checkbox).click().perform()
                            except:
                                # Método 3: Click normal
                                checkbox.click()
                        
                        # Verificar que se marcó
                        time.sleep(1)
                        if not checkbox.is_selected():
                            # Último intento con JavaScript
                            self.driver.execute_script(
                                "arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                                checkbox
                            )
                        
                        self.logger.info(f"Checkbox {checkbox_id} marcado: {checkbox.is_selected()}")
                        return checkbox.is_selected()
                    
                    return True
                    
                except Exception as e:
                    self.logger.error(f"Error al marcar checkbox {checkbox_id}: {str(e)}")
                    return False

            # Información Básica
            if not self.safe_send_keys("23e058fb-9c48-4fbe-9d62-87a8b366ad55", row_data['startup_name']):
                raise Exception("Error al llenar el nombre del startup")
            
            # Para Perú/Lima, simplificamos la selección
            if not self.safe_select_option("country_code", "PE"):  # Código ISO para Perú
                raise Exception("Error al seleccionar el país")
            
            # Ciudad (Lima por defecto)
            if not self.safe_select_option("city", "Lima"):
                raise Exception("Error al seleccionar la ciudad")

            # Universidad (usando el ID del mapeo)
            university_name = row_data['university']
            university_id = self.university_codes.get(university_name)
            if not university_id:
                self.logger.error(f"Universidad no encontrada en el mapeo: {university_name}")
                raise Exception(f"Universidad no encontrada en el mapeo: {university_name}")
            
            self.logger.info(f"Seleccionando universidad: {university_name} (ID: {university_id})")
            if not self.safe_select_option("UniversityId__c", university_id):
                raise Exception("Error al seleccionar la universidad")

            # Información del Capitán
            self.logger.info("Llenando información del capitán")
            captain_fields = {
                "7c6f527f-90e5-4481-9d2f-b9686e9e1bfd": row_data['captain_first_name'],  # FirstName
                "642a9c53-4ea8-482d-bef4-29f7a5444d58": row_data['captain_last_name'],   # LastName
                "4a97fb6f-789e-48f3-847e-6872727e0c1c": row_data['captain_email']        # Email
            }
            
            for field_id, value in captain_fields.items():
                if not self.safe_send_keys(field_id, value):
                    raise Exception(f"Error al llenar campo del capitán: {field_id}")

            # Teléfono del capitán
            try:
                self.logger.info("Intentando llenar el teléfono del capitán...")
                
                # Seleccionar el código de país para Perú (+51)
                phone_code_select = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "StyledDropdown-sc-186t4dl-0"))
                )
                Select(phone_code_select).select_by_value("+51")
                self.logger.info("Código de país seleccionado: +51")
                
                # Encontrar y llenar el campo de teléfono
                phone_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ee4156f9-e9df-4505-81b6-6d018ace7a32"))
                )
                
                # Scroll y espera
                self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_element)
                time.sleep(2)
                
                # Formatear el número (remover +51 o 51 si existe)
                phone_number = str(row_data['captain_phone'])
                phone_number = phone_number.replace('+51', '').replace('51', '', 1) if phone_number.startswith(('51', '+51')) else phone_number
                
                # Usar JavaScript para establecer el valor
                self.driver.execute_script("arguments[0].value = arguments[1];", phone_element, phone_number)
                self.logger.info(f"Teléfono del capitán llenado: {phone_number}")
                
            except Exception as e:
                self.logger.error(f"Error al llenar el teléfono del capitán: {str(e)}")
                self.logger.error(f"Traceback completo: {traceback.format_exc()}")
                raise Exception("Error al llenar el teléfono del capitán")

            # Miembros del equipo (2-4)
            member_fields = {
                2: {
                    'first_name': "26a9c204-1741-47c5-baef-3f24c04d49a6",
                    'last_name': "754e8291-28ff-432e-8cf1-349ff69446fd",
                    'email': "3d6579f4-bbb7-4bf8-ac8e-068b55b8c945",
                    'phone': "f1f3081b-5c7c-46c3-8c1c-651b5ffb0ba3",
                    'university_checkbox': "member2_different_university"
                },
                3: {
                    'first_name': "9038fb4c-77e7-428e-9699-8d4ee32a2b77",
                    'last_name': "3c5bd2bb-e7bc-432d-8fb3-44e612d799bb",
                    'email': "9842094a-ffb5-4457-8d69-4e64bc10708a",
                    'phone': "d4226650-e612-4a34-9e74-a333e83b10e5",
                    'university_checkbox': "member3_different_university"
                },
                4: {
                    'first_name': "877e1bbd-2f94-4618-8b50-929f16a8b5b8",
                    'last_name': "6216c72c-2382-42a8-b833-b7acebc17f26",
                    'email': "39c4458a-4887-407b-8c57-cb9ad5183665",
                    'phone': "0a415619-b619-4f9c-99de-109fa1b32985",
                    'university_checkbox': "member4_different_university"
                }
            }

            for member_num in range(2, 5):
                if pd.notna(row_data.get(f'member{member_num}_first_name')):
                    self.logger.info(f"Llenando información del miembro {member_num}")
                    fields = member_fields[member_num]
                    
                    # Llenar campos básicos
                    self.safe_send_keys(fields['first_name'], row_data[f'member{member_num}_first_name'])
                    self.safe_send_keys(fields['last_name'], row_data[f'member{member_num}_last_name'])
                    self.safe_send_keys(fields['email'], row_data[f'member{member_num}_email'])
                    
                    # Manejar teléfono
                    try:
                        self.logger.info(f"Intentando llenar el teléfono del miembro {member_num}...")
                        
                        # Encontrar todos los selectores de código de país
                        phone_code_selects = self.driver.find_elements(By.CLASS_NAME, "StyledDropdown-sc-186t4dl-0")
                        self.logger.info(f"Total de selectores de código de país encontrados: {len(phone_code_selects)}")
                        
                        # Calcular el índice correcto (0 para capitán, 1 para miembro 2, 2 para miembro 3, 3 para miembro 4)
                        selector_index = member_num - 1
                        
                        if selector_index >= len(phone_code_selects):
                            self.logger.error(f"No se encontró el selector de código de país para el miembro {member_num}")
                            raise Exception(f"Selector de código de país no encontrado para miembro {member_num}")
                        
                        phone_code_select = phone_code_selects[selector_index]
                        Select(phone_code_select).select_by_value("+51")
                        self.logger.info(f"Código de país seleccionado para miembro {member_num}: +51")
                        
                        # Encontrar y llenar el campo de teléfono
                        phone_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.ID, fields['phone']))
                        )
                        
                        # Scroll y espera
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_element)
                        time.sleep(2)
                        
                        # Formatear el número (remover +51 o 51 si existe)
                        phone_number = str(row_data[f'member{member_num}_phone'])
                        phone_number = phone_number.replace('+51', '').replace('51', '', 1) if phone_number.startswith(('51', '+51')) else phone_number
                        
                        # Intentar múltiples métodos para establecer el valor
                        try:
                            # Método 1: JavaScript
                            self.driver.execute_script("arguments[0].value = arguments[1];", phone_element, phone_number)
                            
                            # Verificar si se estableció el valor
                            actual_value = phone_element.get_attribute('value')
                            if not actual_value:
                                # Método 2: Clear y Send Keys
                                phone_element.clear()
                                phone_element.send_keys(phone_number)
                                
                                # Verificar nuevamente
                                actual_value = phone_element.get_attribute('value')
                                if not actual_value:
                                    # Método 3: ActionChains
                                    actions = ActionChains(self.driver)
                                    actions.move_to_element(phone_element).click().send_keys(phone_number).perform()
                            
                            self.logger.info(f"Teléfono del miembro {member_num} llenado: {phone_number}")
                            self.logger.info(f"Valor actual del campo: {phone_element.get_attribute('value')}")
                            
                        except Exception as e:
                            self.logger.error(f"Error al establecer el valor del teléfono: {str(e)}")
                            raise
                        
                    except Exception as e:
                        self.logger.error(f"Error al llenar teléfono del miembro {member_num}: {str(e)}")
                        self.logger.error(traceback.format_exc())
                        raise Exception(f"Error al llenar el teléfono del miembro {member_num}")

            # Manejar checkboxes de universidad diferente
            for member_num in range(1, 5):
                member_university = row_data.get(f'member{member_num}_university')
                if pd.notna(member_university) and member_university.strip():
                    self.logger.info(f"Verificando universidad diferente para miembro {member_num}")
                    checkbox_id = f"differentUniversity{member_num}"
                    
                    if mark_checkbox(checkbox_id):
                        self.logger.info(f"Checkbox de universidad diferente marcado para miembro {member_num}")
                        
                        # Seleccionar país y ciudad
                        country_code = self.country_codes.get(row_data['country'])
                        self.safe_select_option(f"memberCountry{member_num}", country_code)
                        time.sleep(1)
                        
                        self.safe_select_option(f"memberCity{member_num}", row_data['city'])
                        time.sleep(1)
                        
                        # Seleccionar universidad
                        self.select_university(
                            f"memberUniversity{member_num}", 
                            member_university, 
                            f"otherUniversity{member_num}"
                        )
                    else:
                        self.logger.warning(f"No se pudo marcar checkbox para miembro {member_num}")

            # Selección de SDG
            if not self.safe_select_option("Sustainable_Development_Goals__c", row_data['sdg']):
                raise Exception("Error al seleccionar SDG")

            # Experiencia previa y checkboxes
            self.logger.info("Marcando checkboxes y confirmaciones")
            
            # Scroll al final del formulario primero
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Esperar a que el scroll termine
            
            # Manejar radio button de "How did you find out"
            lead_source = row_data['lead_source']
            self.logger.info(f"Seleccionando fuente de información: {lead_source}")
            
            try:
                # Buscar todos los radio buttons de LeadSource
                radio_buttons = self.driver.find_elements(By.NAME, "LeadSource")
                self.logger.info(f"Radio buttons encontrados: {len(radio_buttons)}")
                
                # Encontrar el radio button correcto por su valor
                found = False
                for radio in radio_buttons:
                    if radio.get_attribute('value') == lead_source:
                        # Scroll al elemento
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
                        time.sleep(1)
                        
                        # Intentar múltiples métodos para seleccionar
                        try:
                            # Método 1: JavaScript directo
                            self.driver.execute_script("arguments[0].click(); arguments[0].checked = true;", radio)
                        except:
                            try:
                                # Método 2: ActionChains
                                actions = ActionChains(self.driver)
                                actions.move_to_element(radio).click().perform()
                            except:
                                # Método 3: Click normal
                                radio.click()
                        
                        # Verificar selección
                        if radio.is_selected():
                            self.logger.info(f"Radio button '{lead_source}' seleccionado exitosamente")
                            found = True
                            break
                        else:
                            self.logger.warning(f"Radio button no quedó seleccionado, intentando JavaScript directo")
                            self.driver.execute_script(
                                "arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                                radio
                            )
                
                if not found:
                    raise Exception(f"No se encontró el radio button para: {lead_source}")
                
            except Exception as e:
                self.logger.error(f"Error al seleccionar fuente de información: {str(e)}")
                self.logger.error("Radio buttons disponibles:")
                for rb in radio_buttons:
                    self.logger.error(f"- value: {rb.get_attribute('value')}")
                raise
            
            # Manejar checkboxes requeridos
            checkboxes = {
                "b2dbe7ba-266d-48f3-bbd3-1035700ded97": "Eligible",  # Checkbox de elegibilidad
                "ca6efbd7-f16a-4b7a-8a70-213de5920544": "Terms",     # Términos y condiciones
                "f0f70521-3e33-4805-b696-6b5c6e55a6fc": "Competitor" # Checkbox de competidor
            }
            
            # Scroll al final del formulario primero
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            for checkbox_id, checkbox_name in checkboxes.items():
                # Solo marcar el checkbox de competidor si es requerido
                if checkbox_name == "Competitor" and not row_data.get('is_competitor'):
                    continue
                    
                if not mark_checkbox(checkbox_id):
                    raise Exception(f"No se pudo marcar el checkbox {checkbox_name}")
                
                time.sleep(1)  # Esperar entre checkboxes

            # Esperar para revisión final
            self.logger.info("Esperando 10 segundos para revisión final")
            time.sleep(10)

            self.logger.info("Formulario llenado exitosamente")
            return True, None

        except Exception as e:
            self.logger.error(f"Error al llenar formulario: {str(e)}")
            self.logger.error(traceback.format_exc())
            screenshot_path = self.take_error_screenshot(str(e))
            return False, f"Error: {str(e)}\nScreenshot saved at: {screenshot_path}"

    def fill_team_member(self, member_num, row_data):
        """Llenar información de un miembro del equipo"""
        try:
            self.logger.info(f"\n=== Iniciando llenado de miembro {member_num} ===")
            
            # Prefijos para los campos según el número de miembro
            prefix = f"member{member_num}_"
            id_suffix = str(member_num)
            
            # Verificar si hay datos para este miembro
            if not pd.notna(row_data.get(f'{prefix}first_name')):
                self.logger.info(f"No hay datos para el miembro {member_num}")
                return
            
            # Campos básicos
            fields = {
                f"firstName{id_suffix}": row_data[f'{prefix}first_name'],
                f"lastName{id_suffix}": row_data[f'{prefix}last_name'],
                f"email{id_suffix}": row_data[f'{prefix}email'],
                f"phone{id_suffix}": row_data[f'{prefix}phone']
            }
            
            # Llenar campos básicos
            for field_id, value in fields.items():
                if pd.notna(value):
                    if not self.safe_send_keys(field_id, value):
                        raise Exception(f"Error al llenar {field_id}")
            
            # Seleccionar código de teléfono (siempre +51 para Perú)
            if not self.safe_select_option(f"phoneCode{id_suffix}", "+51"):
                raise Exception(f"Error al seleccionar código de teléfono para miembro {member_num}")
            
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
                    self.logger.info(f"Intentando navegar a URL: {self.form_url}")
                    self.driver.get(self.form_url)
                    current_url = self.driver.current_url
                    self.logger.info(f"URL actual: {current_url}")
                    
                    # Aumentar tiempo de espera para sitio externo
                    self.logger.info("Esperando 5 segundos para carga completa...")
                    time.sleep(5)  # Esperar 5 segundos para que la página se cargue completamente
                    
                    # Verificación más estricta de la URL
                    if "hultprize.org" not in current_url:
                        error_msg = f"Error: URL incorrecta. Esperada: hultprize.org, Actual: {current_url}"
                        self.logger.error(error_msg)
                        screenshot_path = self.take_error_screenshot(error_msg)
                        raise Exception(f"No se pudo acceder al formulario de Hult Prize. URL actual: {current_url}")
                    
                    self.logger.info("URL verificada correctamente, procediendo con el llenado del formulario")
                    
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

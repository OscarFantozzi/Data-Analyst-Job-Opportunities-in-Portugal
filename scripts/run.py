import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Configuração do SQLAlchemy Engine
db_host = 'o host do banco de dados'
db_name = 'nome do banco de dados'
table_name = 'nome da tabela'
connection_string = f'mssql+pyodbc://{db_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server'

# Criar engine
engine = create_engine(connection_string)

# Configuração do proxy (opcional)
PROXY = None  # Remover proxy para evitar problemas de conexão

options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)

# Configuração opcional do proxy
if PROXY:
    options.add_argument(f'--proxy-server={PROXY}')

# Caminho do ChromeDriver
driver_path = r"caminho local onde está instalado o webdriver"
service = Service(driver_path)

# Inicializando o WebDriver
try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    logging.error(f"Erro ao inicializar o WebDriver: {e}")
    exit()

# Configuração de tempo limite
driver.set_page_load_timeout(60)

# Configurações de login do LinkedIn
email_usuario = "inserir email"
senha_usuario = "senha"

# URL do LinkedIn
url_login = "https://www.linkedin.com/login/"
# Página da lista de vagas
url_vagas = "https://www.linkedin.com/jobs/search/?currentJobId=3763296160&keywords=analista%20de%20dados&origin=SWITCH_SEARCH_VERTICAL"

# Simular comportamento humano
def simular_comportamento_humano(min_tempo=1, max_tempo=3):
    time.sleep(random.uniform(min_tempo, max_tempo))

# Função para realizar login no LinkedIn
def realizar_login(email, senha):
    try:
        driver.get(url_login)
        simular_comportamento_humano()
        
        # Aguarda o elemento do e-mail estar visível
        campo_email = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        campo_email.send_keys(email)
        simular_comportamento_humano()
        
        campo_senha = driver.find_element(By.ID, "password")
        campo_senha.send_keys(senha)
        simular_comportamento_humano()
        
        campo_senha.send_keys(Keys.RETURN)
        simular_comportamento_humano(5, 7)
        logging.info("Login realizado com sucesso!")
        
        # Espera adicional para evitar bloqueios
        logging.info("Esperando 10 segundos para evitar bloqueios...")
        time.sleep(30)

    except TimeoutException:
        logging.error("Timeout ao localizar elementos de login. Verifique a conexão.")
        driver.quit()
        exit()
    except Exception as e:
        logging.error(f"Erro ao realizar login: {e}")
        driver.quit()
        exit()

# Função para navegar até a página de vagas
def acessar_vagas():
    try:
        driver.get(url_vagas)
        simular_comportamento_humano(5, 10)
        logging.info("Página de vagas acessada com sucesso!")
    except TimeoutException:
        logging.error("Timeout ao tentar acessar a página de vagas. Verifique a conexão.")
        driver.quit()
        exit()
    except Exception as e:
        logging.error(f"Erro ao acessar a página de vagas: {e}")
        driver.quit()
        exit()

# Função para verificar se a vaga já existe no banco de dados
def vaga_existe(url):
    query = text(f"SELECT COUNT(1) FROM {table_name} WHERE url = :url")
    with engine.connect() as connection:
        result = connection.execute(query, {'url': url}).scalar()
    return result > 0

# Função para extrair informações de vagas
def extrair_informacoes():
    driver.get(url_vagas)
    time.sleep(10)

    start_index = 1
    pagina_atual = 0


    while True:
        try:
            # Recarrega a lista de vagas a cada iteração
            vagas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ember-view.jobs-search-results__list-item")))
            logging.info(f'Encontradas {len(vagas)} vagas na página {pagina_atual}')
    
            for i, vaga in enumerate(vagas, start=1):
                try:
                    # Aguarda o elemento ser clicável
                    driver.execute_script("arguments[0].scrollIntoView();", vaga)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ember-view.jobs-search-results__list-item")))
                    vaga.click()  # Clica na vaga atual
                    simular_comportamento_humano(10, 15)
                    logging.info(f"Cliquei no elemento {i}")
                    
                    # Extrair informações
                    titulo = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.t-24.t-bold.inline"))).text
                    logging.info(f'Título da vaga: {titulo}')
                    
                    empresa = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__company-name a"))).text.strip()
                    logging.info(f'Empresa: {empresa}')
                    
                    local = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.t-black--light.mt2 span.tvm__text.tvm__text--low-emphasis:nth-child(1)")
                        )
                    ).text.strip()
                    logging.info(f'Local: {local}')
                    
                    regime = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.ui-label.ui-label--accent-3.text-body-small"))).text.strip()
                    logging.info(f'Regime: {regime}')
                    
                    try:
                        elemento_senioridade = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@dir='ltr' and contains(@class, 'job-insight-view-model-secondary')]"))
                        )
                        senioridade = elemento_senioridade.text
                        logging.info(f"Senioridade: {senioridade}")
                    except (NoSuchElementException, TimeoutException):
                        senioridade = "Não disponível"
                        logging.warning(f"Erro ao capturar a senioridade: Não disponível")

                    # Esperando a página carregar e encontrando o elemento desejado
                    try:
                        elemento_cliques = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__primary-description-container strong"))
                        )
                        numero_cliques = elemento_cliques.text
                        logging.info(f"Número de cliques: {numero_cliques}")
                    except (NoSuchElementException, TimeoutException):
                        numero_cliques = "Não disponível"
                        logging.warning(f"Erro ao capturar o número de cliques: Não disponível")
                    
                    url = driver.current_url
                    logging.info(f'URL: {url}')
                    
                    data_extracao = datetime.now().date()
                    logging.info(f'Data de extração: {data_extracao}')
            
                    # Verificar se a vaga já existe no banco de dados
                    if vaga_existe(url):
                        logging.info(f"Vaga já existe no banco de dados: {titulo} - {empresa}")
                        continue
            
                    # Adicionando os dados ao banco de dados
                    vaga_info = {
                        "titulo": titulo,
                        "empresa": empresa,
                        "local": local,
                        "regime": regime,
                        "senioridade": senioridade,
                        "numero_cliques": numero_cliques,
                        "url": url,
                        "data_extracao": data_extracao
                    }
                    df_vagas = pd.DataFrame([vaga_info])
                    df_vagas.to_sql(name=table_name, con=engine, if_exists="append", index=False)
                    logging.info(f"Vaga extraída e salva: {titulo}")
            
                except StaleElementReferenceException:
                    logging.warning("Erro de elemento stale. Ignorando vaga.")
                except NoSuchElementException as e:
                    logging.warning(f"Erro ao encontrar um elemento: {e}")
                except SQLAlchemyError as e:
                    logging.error(f"Erro ao inserir no banco de dados: {e}")
        

            time.sleep(2)
            if i % 25 == 0:
                proximo_start = i + 1
                pagina_atual = pagina_atual + 1 
                print(f"Indo para próxima página: {pagina_atual}" )
                novo_url = f"{url_vagas}&start={pagina_atual * 25}"
                print(novo_url)
                driver.get(novo_url)
                driver.implicitly_wait(5)
                start_index = proximo_start
    
            time.sleep(5)
    
        except Exception as e:
            logging.warning(f"Erro ao processar a página: {e}, tentando novamente...")
            simular_comportamento_humano(5, 10)
            continue

# Fluxo principal
try:
    realizar_login(email_usuario, senha_usuario)
    acessar_vagas()
    extrair_informacoes()
except Exception as e:
    logging.error(f"Erro na execução principal: {e}")
finally:
    logging.info("Finalizando WebDriver...")
    driver.quit()

import time
from warnings import warn
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
from requests import get
from requests_xml import XMLSession

class ImdbSpider(object):

    def scraping(self):
        municipios = []
        codigo_iteraveis = []
        session = XMLSession()
        r = session.get('http://www.der.sp.gov.br/Upload/XML/codigo_rodoviario_cadastro_rodoviario.xml')
        headers = {"Accept-Language": "en-US,en;q=0.8", "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3"}

        print(r.text)

        requests = 0

        cod_id_value = []


        for item in r:
            cod_id = r.xml.find('cod_id')
            cod_id[requests].text
            cod_tipo = r.xml.find('cod_tipo')
            cod_tipo[requests].text
            cod_codigo = r.xml.find('cod_codigo')
            cod_codigo[requests].text
            municipios.append([cod_id, cod_tipo, cod_codigo])
            codigo_iteraveis.append(cod_id[requests].text)
            print('Qtd iteracoes: %s' % (requests))
            requests += 1
            if requests == 10:
                break

        requests = 0

        for item in municipios:
            print(item)

        for codigo in codigo_iteraveis:
            print('Codigo sendo utilizado: %s'%(codigo))
            response = get('http://www.der.sp.gov.br/WebSite/Acessos/MalhaRodoviaria/Services/rodovia_pesquisa.aspx??'
                           'pg=4500'
                           '&codigo=' + codigo +
                           '&superfice='
                           '&jurisdicao='
                           '&municipio='
                           '&kminicial='
                           '&kmfinal='
                           '&administracao='
                           '&operadora=', headers)
            time.sleep(10)
            if response.status_code != 200:
                warn('Request: {}; Status code: {}'.format(requests, response.status_code))
            page_html = BeautifulSoup(response.text, 'html.parser')

            tag = page_html.findAll('td')
            km_inicial =  tag[0]
            km_final = tag[1]
            extensao = tag[2]
            tag_municipio = tag[3]
            tag_regional = tag[4]
            tag_jurisdicao = tag[6]
            tag_superficie = tag[9]


            requests += 1
            if requests == 3:
                break
            print('=======================================================================================================')
            print(km_inicial.text)
            print(km_final.text)
            print(extensao.text)
            print(tag_municipio.text)
            print(tag_regional.text)
            print(tag_jurisdicao.text)
            print(tag_superficie.text)
           # print(page_html)



    def separa_genero(self):
        filmes_por_genero = {}
        format=[]
        for filme in self:
            generos = filme[2]
            for genero in generos:
                if genero in filmes_por_genero:
                    format = format_to_use_json(filme)
                    filmes_por_genero[genero].append(format)
                else:
                    format = format_to_use_json(filme)
                    filmes_por_genero[genero] = [format]
        return filmes_por_genero


    def salva_json(filmes_por_genero):
        dict_key = filmes_por_genero.keys()
        for filmes in filmes_por_genero:
            if dict_key.__contains__(filmes):
                with open('JSONs/%s.json'% (filmes), 'w') as fp:
                    json.dump(filmes_por_genero[filmes], fp)

        print('Arquivos JSONs gerados')






import scrapy
import re

from PROPIEDADES_Final.items import PropiedadesFinalItem



class Part1Spider(scrapy.Spider):
    name = 'part1mai'
    allowed_domains = ['propiedades.com']
    start_urls = ["https://propiedades.com/sitemaps/sitemap_results_1a.xml",
                  "https://propiedades.com/sitemaps/sitemap_results_2b.xml",
                  "https://propiedades.com/sitemaps/sitemap_results_3c.xml",
                  "https://propiedades.com/sitemaps/sitemap_results_4d.xml",
                  "https://propiedades.com/sitemaps/sitemap_results_5e.xml",]

    def parse(self, response):
        print (" (______^__^______)")

        liens = re.findall(r"<loc>(.+)</loc>", response.text)
        for lien in liens:
            yield scrapy.Request(url=lien, callback=self.parse_list)

    def parse_list(self, response):
        print("(---^-*---)")
        liste = response.xpath('//div[@class="address"]/p[@class="title-property"]/a/@href').extract()

        for href in liste:

            if "html" not in href:
                yield scrapy.Request(url=href, callback=self.parse_details)
            next_page = response.xpath('//a[@class="page siguiente"]/@href').extract_first()
            if next_page is not None:
                print ('------------------------->', next_page)
                yield scrapy.Request(next_page, callback=self.parse_list)
    def correct(self,champ):

        return str(champ).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace(';', ' ').replace('\"', ' ')


    def parse_details(self, response):
        print("details")
        item = PropiedadesFinalItem()

       # surfaceTerrain = response.xpath(
       #         "//div/ul/li/p[contains(., 'Mediana de m2 de terreno:')]/parent::li/following-sibling::li/span/text()").extract_first()
       # if surfaceTerrain == None:
       # surfaceTerrain = "0"
#en cas de surface terrain ne se trouve pas en Características típicas  en voir en Características principales
        surfaceTerrain=response.xpath("//section/div/ul/li/span[contains('Tamaño del terreno ',.)]/following-sibling::span/text()").extract_first()
        
        if surfaceTerrain in [None,"N/D"]:
            surfaceTerrain=""
        else:
            surface_symbole=surfaceTerrain.split(" ")
            if surface_symbole[1]=="ha":
            	surfaceTerrain=float(surface_symbole[0].replace(",",""))*10000
            elif surface_symbole[1]=="m":
            	surfaceTerrain=float(surface_symbole[0].replace(",",""))


            len_surfaceTerrain=len(str(surfaceTerrain))
            if len_surfaceTerrain >11:
                cc=float(surfaceTerrain)
                cc1=int(cc)
                cc2=float(cc1)+1
                surfaceTerrain=cc2

            if surfaceTerrain>99999999.9:
                  
                surfaceTerrain=99999999
                                  #surfaceTotal = response.xpath(
         #       "//div/ul/li/p[contains(., 'Mediana de m2 de construcción:')]/parent::li/following-sibling::li/span/text()").extract_first()
        #if surfaceTotal == None:
        #surfaceTotal = "0"
#en cas de surface ne se trouve pas en Características típicas  en voir en Características principales
        surfaceTotal=response.xpath("//section/div/ul/li/span[contains('Tamaño de construcción',.)]/following-sibling::span/text()").extract_first()
        if surfaceTotal in [None,"N/D"]:
            surfaceTotal=""
        else:
            surface_symbole=surfaceTotal.split(" ")
            if surface_symbole[1]=="ha":
                surfaceTotal=float(surface_symbole[0].replace(",",""))*10000
            elif surface_symbole[1]=="m":
                surfaceTotal=float(surface_symbole[0].replace(",",""))
 
            len_surfaceTotal=len(str(surfaceTotal))
            if len_surfaceTotal >11:
                cc=float(surfaceTotal)
                cc1=int(cc)
                cc2=float(cc1)+1
                surfaceTotal=cc2
         
            if surfaceTotal>99999999.9:
                surfaceTotal=99999999


        #chambre = response.xpath("//div/ul/li/p[contains(., 'Recámaras')]/parent::li/following-sibling::li/span/text()").extract_first()
        chambre=response.xpath("//section/div/ul/li/span[contains('Recámaras',.)]/following-sibling::span/text()").extract_first()

        if chambre in [None,"N/D"] :
            chambre = ""
        #sdbain = response.xpath("//div/ul/li/p[contains(., 'Baños')]/parent::li/following-sibling::li/span/text()").extract()
        #if sdbain == None:
         #   sdbain = "0"

       # prix = response.xpath("//div/ul/li/p[contains(., 'Precio medio')]/parent::li/following-sibling::li/span/text()").extract_first()
       # if prix in[None,"N/D"]:
        prix = "0"
#en cas de prix ne se trouve pas en Características típicas  en voir en C$
        prix_2methode=response.xpath("//div/div/span[@class='price-gallery text-green']/text()").extract_first()
        if prix_2methode[0]=="$" and prix_2methode[1]==" ":
            prix=prix_2methode[2:]
        else:
            prix=prix_2methode

        #if prix=="0":
        #    prix_chifre=prix_2methode.split(" ")
        #    prix_symbole=re.findall("([a-z,A-Z].+)",prix_2methode)
        #    if prix_symbole[0] =="MN" :
        #        res=float(prix_chifre[1])/19
        #    elif prix_symbole[0]=="mil MN":
        #        res=float(prix_chifre[1])*1000/19
        #    elif prix_symbole[0]=="MDP" :
        #        res=float(prix_chifre[1])*1000000/19
        #    elif prix_symbole[0]=="MDD" :
        #        res=float(prix_chifre[1])*1000000
        #    elif prix_symbole[0] =="mil USD" :
        #        res=float(prix_chifre[1])*1000
        #    elif prix_symbole[0]=="USD" :
        #        res=float(prix_chifre[1])
        #    else:
        #        res=prix_2methode

 
       #     prix=res



        #prixM2 = response.xpath("//div/ul/li/p[contains(., 'Mediana del precio/m2 de construcción:')]/parent::li/following-sibling::li/span/text()").extract_first()
       # if prixM2 in[None,"N/D"]:
       #     prixM2 = "0"
       # garage = response.xpath("//div/ul/li/p[contains(., 'Estacionamiento')]/parent::li/following-sibling::li/span/text()").extract_first()
        garage=response.xpath("//section/div/ul/li/span[contains('Estacionamiento',.)]/following-sibling::span/text()").extract_first() 
        if garage in [None,"N/D"] :
            garage = ""

        #
        # item['surface'] = surface

        # item['sdbain'] = sdbain
        dsc = response.xpath('//article[@class="content-left"]/section/div[2]/p/text()').extract_first()
        if dsc==None:
            dsc=" "


        province = str(response.xpath(
            './/div/div/h1[@class="title-gallery"]/span[@itemprop="addressRegion"]/text()').extract_first()).replace("\n","").replace('\t','')
        if province==None:
            province=" "

        quartier = str(response.xpath('.//div/div/h1[@class="title-gallery"]/span/text()').extract_first()).replace("\n","").replace(',','')
        if quartier==None:
            quartier=" "
        ville= str(response.xpath(
            './/div/div/h1[@class="title-gallery"]/span[@itemprop="addressLocality"]/text()').extract_first()).replace("\n","").replace(',','')
        if ville==None:
            ville=" "
        codeP = str(response.xpath(
            '//div/div/h1[@class="title-gallery"]/span[@itemprop="postalCode"]/text()').extract_first()).replace("\n","").replace(',','')
        if codeP == None:
            codeP = "0"

        nom = str(response.xpath('.//div/div/h1[@class="title-gallery"]/em/text()').extract_first()).replace("\n"," ").replace('\t','').replace(",","")


        if nom==None:
            nom="n'existe pas"


        maison_apt=response.xpath('//div[1]/div[3]/div/div/ol[1]/li/a/span[@itemprop="name"]/text()').extract()
        categorie=maison_apt[len(maison_apt)-1]

        if categorie=="Departamentos":
            maison_apt=2
        elif categorie=="Casas" :
            maison_apt=1
        elif "Cuartos" in categorie:
            maison_apt=6

        else:
            maison_apt=8



       # id_client=str(response.url)
       # res = re.findall("([0-9]+)",id_client)
       # res = [int(x) for x in res]
       # max = 0
       # for x in res:
       #     if x > max:
       #         max = x
        id_client=response.xpath("//input[@id='property_id']/@value").extract_first()
        typee = response.xpath('//div[1]/div[4]/div[3]/div[1]/div/div[1]/p').extract_first()

        if "Venta" in typee:
            achat_loc = "1"
        elif maison_apt==6:
            achat_loc="6"
        else:
            achat_loc= "2"

        annonce_part1=response.xpath("//div[1]/div[5]/div/p[@class='info-update']/text()").extract()
       
        if annonce_part1==None:
            annonce_date=" "
        else:
            annonce_part1=str(annonce_part1).split(":")
            annonce_part2=annonce_part1[1].split("n")
            annonce_part3=annonce_part2[1].split("\\")
            annonce_date=annonce_part3[0]
            if "']" in annonce_date:
                annonce_date=annonce_date.replace("']","")

        nb_etage=response.xpath("//section/div/ul/li/span[contains('No. de pisos',.)]/following-sibling::span/text()").extract_first()
        if nb_etage in [None,"N/D"]:
            nb_etage=""    




#        item['SITE']=self.correct("propiedades.com")
        item['ANNONCE_LINK']=self.correct(response.url)
        item['FROM_SITE']=self.correct("propiedades")
        item['ID_CLIENT']=self.correct(id_client)
        item['ACHAT_LOC']=self.correct(achat_loc)
#        item['MAISON_APT']=self.correct(maison_apt)
        item['NOM']=self.correct(nom)
       # item['ADRESSE']=quartier+" "+ville+" "+codeP+" "+province
        item['CP']=self.correct(codeP)
        item['VILLE']=self.correct(ville)
        item['QUARTIER']=self.correct(quartier)
        item['PROVINCE']=self.correct(province)
        item['ANNONCE_TEXT']=self.correct(dsc)
        item['SURFACE_TERRAIN']=self.correct(surfaceTerrain)
        item['M2_TOTALE']=self.correct(surfaceTotal)
        item['PIECE']=self.correct(chambre)
        item['PRIX']=self.correct(prix)
       # item['PRIX_M2']=self.correct(prixM2)
        item['NB_GARAGE']=self.correct(garage)

        item['ANNONCE_DATE']=self.correct(annonce_date)
        item['CATEGORIE']=self.correct(categorie)
        item['NB_ETAGE']=self.correct(nb_etage)

        yield item














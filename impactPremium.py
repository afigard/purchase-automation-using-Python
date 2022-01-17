#_________________ AUTOMATION OF A PRODUCT PURCHASE ON THE WEBSITE : https://www.impact-premium.com/ _________________

import threading
import requests
import re
import os
import random
from threading import Thread
import csv
from termcolor import colored
import time
from discord_webhook import DiscordWebhook






# Proxies
proxy_file = os.listdir('proxies')
print("Choissiez votre liste de proxies")
for i in range(len(proxy_file)):
    print(str(i) +". " + proxy_file[i].replace(".txt",""))
choix_proxies = int(input())
Proxys_file = open("proxies/"+proxy_file[choix_proxies], 'r')
proxy = Proxys_file.readlines()

def Get_new_proxy():
    proxy_used = proxy[random.randint(0, len(proxy) - 1)]
    contenu = re.findall(r'(.*?):(.*?):(.*?):(.*?)\n', proxy_used)
    proxies = {
        'https': 'http://' + contenu[0][2] + ":" + contenu[0][3] + "@" + contenu[0][0] + ":" + contenu[0][1]
    }
    return proxies



# Open csv and slicing
with open('impactPremium/impactPremium.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)[1:]
    
    

# Main function
def Checkout(i):
    s = requests.session()
    s.proxies.update(Get_new_proxy())
    
    # --------------- 1 : PRODUCT PAGE ---------------
    
    url_produit = rows[i][0]
    
    headers = {
        "authority" : "www.impact-premium.com",
        "method" : "GET",
        "path" : "/nike/13057-80505-nike-air-huarache-toadstool.html",
        "scheme" : "https",
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "fr-FR,fr;q=0.9",
        "sec-ch-ua" : '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile" : "?0",
        "sec-ch-ua-platform" : '"Windows"',
        "sec-fetch-dest" : "document",
        "sec-fetch-mode" : "navigate",
        "sec-fetch-site" : "none",
        "sec-fetch-user" : "?1",
        "upgrade-insecure-requests" : "1",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }    
    s.headers.update(headers)
    
    while True:
        try:
            get_url_req = s.get(url=url_produit)
            if "Ajouter au panier" in get_url_req.text:
                print(colored("Successfully got product page " + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to get product Page") 
        except:
            print("Error")
    
    id_product_attribute = re.findall(r'data-id_product_attribute="(.*?)"',get_url_req.text)[0]
    id_product = re.findall(r'data-id_product="(.*?)"',get_url_req.text)[0] 
    token_1 = re.findall(r'name="token" value="(.*?)"',get_url_req.text)[0]
    
    # --------------- 2 : PANIER  --------------
    
    url_panier1 = "https://www.impact-premium.com/panier"
     
    s.headers["authority"] = "www.impact-premium.com"
    s.headers["method"] = "POST"
    s.headers["path"] = "/panier"
    s.headers["accept"] = "application/json, text/javascript, */*; q=0.01"
    s.headers["origin"] = "https://www.impact-premium.com"
    s.headers["referer"] = "https://www.impact-premium.com/nike/13057-80505-nike-air-huarache-toadstool.html"
    s.headers["sec-fetch-dest"] = "empty"
    s.headers["sec-fetch-mode"] = "cors"
    s.headers["sec-fetch-site"] = "same-origin"
    
    data2_panier1 = {
        "token" : token_1,
        "id_product" : id_product,
        "id_customization" : "0",
        "ma-sendgroup" : "0",
        "ma-tooltip" : "0",
        "group[2]" : "75",
        "group[5]" : "317",
        "add" : "1",
        "action" : "update"
        }
    
    s.post(url=url_panier1,data=data2_panier1)
    
    
    
            
    atc_url = "https://www.impact-premium.com/module/ps_shoppingcart/ajax"
    
    #update headers
    s.headers["method"] = "POST"
    s.headers["path"] = "/module/ps_shoppingcart/ajax"
    s.headers["accept"] = "*/*"
    s.headers["sec-fetch-dest"] = "empty"
    s.headers["sec-fetch-mode"] = "cors"
    s.headers["sec-fetch-site"] = "same-origin"
    #delete headers
    s.headers.pop("upgrade-insecure-requests")
    #new headers
    s.headers["content-length"] = "62"
    s.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    s.headers["origin"] = "https://www.impact-premium.com"
    s.headers["referer"] = "https://www.impact-premium.com/nike/13057-80505-nike-air-huarache-toadstool.html"
    s.headers["x-requested-with"] = "XMLHttpRequest"
    
    data_atc = {
        "id_product_attribute" : id_product_attribute,
        "id_product" : id_product,
        "action" : "add-to-cart"
    }
    
    while True:
        try:
            atc_req = s.post(url=atc_url,data=data_atc)
            if "Commander" in atc_req.text:
                print(colored("Successfully added to cart " + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to ATC")
        except:
            print("Error")




    url_panier = "https://www.impact-premium.com/panier?action=show"
    
    #update headers
    s.headers["method"] = "GET"
    s.headers["path"] = "/panier?action=show"
    s.headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    s.headers["sec-ch-ua"] = '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"'
    s.headers["sec-fetch-dest"] = "document"
    s.headers["sec-fetch-mode"] = "navigate"
    #delete headers
    s.headers.pop("content-length")
    s.headers.pop("content-type")
    s.headers.pop("origin")
    s.headers.pop("x-requested-with")
    #new headers
    s.headers["upgrade-insecure-requests"] = "1"     
    
    while True:
        try:
            get_panier_req = s.get(url=url_panier, headers=headers)
            if "Poursuivre" in get_panier_req.text:
                print(colored("Successfully ordered " + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to order")
        except:
            print("Error")
 

    

    url_checkout = "https://www.impact-premium.com/commande"
    
    #update headers
    s.headers["path"] = "/commande"
    s.headers["referer"] = "https://www.impact-premium.com/panier?action=show"
    
    while True:
        try:
            get_checkout_req = s.get(url=url_checkout, headers=headers)
            if "Prénom" in get_checkout_req.text:
                print(colored("Successfully got checkout " + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to checkout")
        except:
            print("Error")
            
            
            
        
    
    # --------------- 3 : CREATION DE COMPTE ---------------
    
    # --- sous-partie a ---
    #post
    #update headers
    s.headers["method"] = "POST"
    s.headers["referer"] = "https://www.impact-premium.com/commande"
    #new headers
    s.headers["cache-control"] = "max-age=0"
    s.headers["content-length"] = "128"
    s.headers["content-type"] = "application/x-www-form-urlencoded"
    s.headers["origin"] = "https://www.impact-premium.com" 
    
    data_infop_1 = {
        "id_gender" : "3",
        "firstname" : rows[i][1],
        "lastname" : rows[i][2],
        "email" : rows[i][3],
        "password" : rows[i][4],
        "psgdpr" : "1",
        "submitCreate" : "1",
        "continue" : "1"
    }
    
    sendinfop1_req = s.post(url=url_checkout,data=data_infop_1, headers=headers)
    
    
    #get
    #update headers
    s.headers["method"] = "GET"
    #delete headers
    s.headers.pop("content-length")
    s.headers.pop("content-type")
    s.headers.pop("origin")
    
    while True:
        try:
            s.get(url=url_checkout, headers=headers)
            if "Société" in sendinfop1_req.text:
                print(colored("Successfully passed step a " + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to get through step a")
        except:
            print("Error")
            
    
    
    # --- sous-partie b ---
    #post
    url_post2 = "https://www.impact-premium.com/commande?id_address=0"
    #update headers
    s.headers["method"] = "POST"
    s.headers["path"] = "/commande?id_address=0"
    s.headers["referer"] = "https://www.impact-premium.com/commande"
    #new headers
    s.headers["cache-control"] = "max-age=0"
    s.headers["content-length"] = "261"
    s.headers["content-type"] = "application/x-www-form-urlencoded"
    s.headers["origin"] = "https://www.impact-premium.com"
    
    data_infop_2 = {
        "back" : "",
        "token" : token_1,
        "firstname" : rows[i][1],
        "lastname" : rows[i][2],
        "company" : "",
        "vat_number" : "",
        "address1" : rows[i][5],
        "address2" : "",
        "postcode" : rows[i][6],
        "city" : rows[i][7],
        "id_country" : "8",
        "phone" : rows[i][8],
        "saveAddress" : "delivery",
        "use_same_address" : "1",
        "submitAddress" : "1",
        "confirm-addresses" : "1"
    }
    
    sendinfop2_req = s.post(url=url_post2,data=data_infop_2, headers=headers)
    
    #get
    #update headers
    s.headers["method"] = "GET"
    #delete headers
    s.headers.pop("content-length")
    s.headers.pop("content-type")
    s.headers.pop("origin")
    
    while True:
        try:
            s.get(url=url_post2, headers=headers)
            #if "Choisissez vos options UPS" in sendinfop2_req.text:
            if "a" in sendinfop2_req.text:
                print(colored("Successfully passed step b " + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to get through step b")
        except:
            print("Error")
    
    
    
    # --- sous-partie c ---
    #post
    #update headers
    s.headers["method"] = "POST"
    s.headers["path"] = "/commande"
    s.headers["accept"] = "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
    s.headers["referer"] = "https://www.impact-premium.com/commande"
    #new headers
    s.headers["cache-control"] = "max-age=0"
    s.headers["content-length"] = "75"
    s.headers["content-type"] = "application/x-www-form-urlencoded"
    s.headers["origin"] = "https://www.impact-premium.com"
    
    data_infop_3 = {
        "delivery_option[20381]" : "496,",
        "delivery_message" : "",
        "confirmDeliveryOption" : "1"
    }
    
    sendinfop3_req = s.post(url=url_checkout,data=data_infop_3, headers=headers)
    
    #get
    #update headers
    s.headers["method"] = "GET"
    #delete headers
    s.headers.pop("content-length")
    s.headers.pop("content-type")
    s.headers.pop("origin")
    
    while True:
        try:
            s.get(url=url_checkout, headers=headers)
            if "Payer avec un compte PayPal" in sendinfop3_req.text:
                print(colored("Successfully passed step c" + threading.current_thread().getName(), 'green', attrs=['bold']))
                break
            else:
                print("Error trying to get through step c ")
        except:
            print("Error")
            
            
    
    # --- sous-partie d ---
    #update headers
    s.headers["authority"] = "www.facebook.com"
    s.headers["method"] = "GET"
    s.headers["path"] = "/tr/?id=783554445526554&ev=AddPaymentInfo&dl=https%3A%2F%2Fwww.impact-premium.com%2Fcommande&rl=https%3A%2F%2Fwww.impact-premium.com%2Fcommande&if=false&ts=1635250498368&sw=1536&sh=864&v=2.9.47&r=stable&ec=2&o=30&fbp=fb.1.1635243898743.1106523548&it=1635250446164&coo=false&rqm=GET"
    s.headers["referer"] = "https://www.impact-premium.com/"
    #delete headers
    s.headers.pop("cache-control")
    s.headers.pop("upgrade-insecure-requests")
    s.headers.pop("sec-fetch-user")
    #new headers
    s.headers["sec-fetch-dest"] = "image"
    s.headers["sec-fetch-mode"] = "no-cors"
    s.headers["sec-fetch-site"] = "cross-site"
    
    s.get(url="https://www.facebook.com/tr/?id=783554445526554&ev=AddPaymentInfo&dl=https%3A%2F%2Fwww.impact-premium.com%2Fcommande&rl=https%3A%2F%2Fwww.impact-premium.com%2Fcommande&if=false&ts=1635250498368&sw=1536&sh=864&v=2.9.47&r=stable&ec=2&o=30&fbp=fb.1.1635243898743.1106523548&it=1635250446164&coo=false&rqm=GET", headers=headers)
    print(colored("Successfully got PayPal link available " + threading.current_thread().getName(), 'green', attrs=['bold']))
    
    
    
    # --- sous-partie e ---
    fcheckout_url = "https://www.impact-premium.com/module/ps_checkout/create"
    #update headers
    s.headers["authority"] = "www.impact-premium.com"
    s.headers["method"] = "POST"
    s.headers["path"] = "/module/ps_checkout/check"
    s.headers["accept"] = "*/*"
    s.headers["content-length"] = "26"
    s.headers["content-type"] = "application/json"
    s.headers["origin"] = "https://www.impact-premium.com"
    s.headers["referer"] = "https://www.impact-premium.com/commande"
    s.headers["sec-fetch-dest"] = "empty"
    s.headers["sec-fetch-mode"] = "cors"
    s.headers["sec-fetch-site"] = "same-origin"
    
    data_req_payload = {"fundingSource":"paypal"} 
    post_reqpayload_req = s.post(url=fcheckout_url, data=data_req_payload, headers=headers)
    
    
    
    
    
    # --------------- 4 : LIEN PAYPAL + WEBHOOK ---------------
    
    #find paypal token
    token_PayPal = re.findall(r'"orderID":"(.*?)"',post_reqpayload_req.text)[0]
    
    #construct paypal link
    paypal_checkout_link = 'https://www.paypal.com/checkoutnow?token=EC-' + token_PayPal
    
    #webhook
    webhook = DiscordWebhook(url=rows[i][9], 
                             content = paypal_checkout_link)
    webhook.execute()






threads= []
class impactPremium(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
    def run(self):
        Checkout(i)

for i in range(len(rows)):
    t = impactPremium()
    threads.append(t)
    t.daemon = True
    t.start()
    time.sleep(0.5)

for x in threads:
    x.join()
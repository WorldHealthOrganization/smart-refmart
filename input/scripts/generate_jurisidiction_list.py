#!/usr/bin/env python3

import glob as glob
import re
# import pandas lib as pd
import pandas as pd
#import string
import sys
import getopt
import urllib3 as urllib
import json

# the WHO RefMart Country List
refmart_country_list_url = "https://xmart-api-public.who.int/REFMART/REF_COUNTRY"


iso3_vs_filename = "input/fsh/valuesets/COUNTRYISO3.fsh"
iso2_vs_filename = "input/fsh/valuesets/COUNTRYISO2.fsh"
m49_vs_filename = "input/fsh/valuesets/COUNTRYM49.fsh"
iso3_cs_filename = "input/fsh/codesystems/COUNTRYISO3.fsh"
iso2_cs_filename = "input/fsh/codesystems/COUNTRYISO2.fsh"
m49_cs_filename = "input/fsh/codesystems/COUNTRYM49.fsh"
m49_conceptmap_filename = "input/fsh/conceptmaps/M49toISO3.fsh"
iso2_conceptmap_filename = "input/fsh/conceptmaps/ISO3toISO2.fsh"



def usage():
    print("OPTIONS:")
    print(" none")
    print("--help|h : print this information")
    sys.exit(2)


def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError:
        usage()

    extract_countries(load_remote_json(refmart_country_list_url))

def printout(content,filename):
    file = open(filename,"w")
    print(content, file=file)
    file.close


def load_remote_json(url):
    response = urllib.request("GET",url)
    return json.loads(response.data)


# the WHO refmart Country List
#{
# "@odata.context": "https://xmart-api-public.who.int/REFMART/$metadata#REF-COUNTRY",
# "value": [
# {
# "GEO-M49-CODE": "004",
# "CODE-ISO-2": "AF",
# "CODE-ISO-3": "AFG",
# "CODE-WHO": "AFG",
# "CODE-ISO-NUMERIC": 4,
# "NAME-SHORT-EN": "Afghanistan",
# "NAME-FORMAL-EN": "the Islamic Republic of  Afghanistan",
# "CAPITAL-CITY": "Kabul",
# "ADJECTIVE-PEOPLE": "Afghan",
# "GEO-SMALL-POP-FLAG": false,
# "GEO-SOVEREIGN": null,
# "SOVEREIGN-ISO-3": null,
# "GRP-WB-INCOME": "LIC",
# "GRP-WHO-REGION": "EMR",
# "WHO-LEGAL-STATUS": "M",
# "WHO-LEGAL-STATUS-TITLE": "Member State",
# "DATE-START": null,
# "NAME-CHANGE": null,
# "ISO-CHANGE": null,
# "CAPITAL-CHANGE": null,
# "STATISTICAL-CHANGE": null,
# "GEO-PRECEDED-BY": null,
# "GEO-SUCCEEDED-BY": null,
# "NAME-SHORT-AR": "أفغانستان",
# "NAME-FORMAL-AR": "جمهورية أفغانستان الإسلامية",
# "NAME-SHORT-ES": "Afganistán",
# "NAME-FORMAL-ES": "República Islámica del Afganistán",
# "NAME-SHORT-FR": "Afghanistan",
# "NAME-FORMAL-FR": "République islamique d'Afghanistan",
# "NAME-SHORT-RU": "Афганистан",
# "NAME-FORMAL-RU": "Исламская Республика Афганистан",
# "NAME-SHORT-ZH": "阿富汗",
# "NAME-FORMAL-ZH": "阿富汗伊斯兰共和国"
# },

def pp(json_content):
    return json.dumps(json_content, indent=2)

def escape(s):
    if (isinstance(s,str)):
        return s.replace('"', r'\"')
    else:
        print("Warning bad string: " , s)
        return "";


def extract_countries(data):

    
    iso3codes = "CodeSystem: COUNTRYISO3\n"
    iso3codes += 'Title: "WHO RefMart Country List ISO 3 Codes"\n'
    iso3codes += 'Description: "CodeSystem for ISO 3 code from  WHO RefMart Country and Jurisidiction List available at ' + refmart_country_list_url + '"\n'
    iso3codes += '* ^status = #active\n'
    iso3codes += '* ^experimental = true\n'

    iso2codes = "CodeSystem: COUNTRYISO2\n"
    iso2codes += 'Title: "WHO RefMart Country List ISO 2 Codes"\n'
    iso2codes += 'Description: "CodeSystem for ISO 2 code from from WHO RefMart Country and Jurisidiction List available at ' + refmart_country_list_url + '"\n'
    iso2codes += '* ^status = #active\n'
    iso2codes += '* ^experimental = true\n'

    m49codes = "CodeSystem: COUNTRYM49\n"
    m49codes += 'Title: "WHO RefMart Country List M49 Codes"\n'
    m49codes += 'Description: "CodeSystem for M49 code from WHO RefMart Country and Jurisidiction List available at ' + refmart_country_list_url + '"\n'
    m49codes += '* ^status = #active\n'
    m49codes += '* ^experimental = true\n'

    
    m49maps = 'Instance: M49toISO3\n'
    m49maps += 'InstanceOf: ConceptMap\n'
    m49maps += 'Title: "Concept Map from M49 to ISO3 country codes"\n'
    m49maps += 'Description: "WHO Concept Map for RefMart countries from M49 to ISO3 codes"\n'
    m49maps += 'Usage:        #definition\n'
    m49maps += '* status = #active\n'
    m49maps += '* meta.profile[+] = "http://hl7.org/fhir/uv/crmi/StructureDefinition/crmi-shareableconceptmap"\n' 
    m49maps += '* meta.profile[+] = "http://hl7.org/fhir/uv/crmi/StructureDefinition/crmi-publishableconceptmap"\n'
    m49maps += '* group[+]\n'
    m49maps += '  * source = $m49codes\n'
    m49maps += '  * target = $iso3codes\n'

    iso2maps = 'Instance: ISO3toISO2\n'
    iso2maps += 'InstanceOf: ConceptMap\n'
    iso2maps += 'Title: "Concept Map from ISO3 to ISO2 country codes"\n'
    iso2maps += 'Description: "WHO Concept Map for RefMart countries from ISO3 to ISO2 codes"\n'
    iso2maps += 'Usage:        #definition\n'
    iso2maps += '* status = #active\n'
    iso2maps += '* meta.profile[+] = "http://hl7.org/fhir/uv/crmi/StructureDefinition/crmi-shareableconceptmap"\n' 
    iso2maps += '* meta.profile[+] = "http://hl7.org/fhir/uv/crmi/StructureDefinition/crmi-publishableconceptmap"\n'
    iso2maps += '* group[+]\n'
    iso2maps += '  * source = $iso3codes\n'
    iso2maps += '  * target = $iso2codes\n'
    
    for country in data['value']:
        #print(pp(country))
        if ((not 'NAME_SHORT_EN' in country) or (not 'CODE_ISO_3' in country)):
            print("Could not get ISO code or name for record", data)
            continue
        print("Processing " + country['CODE_ISO_3'] + ' / ' + country['NAME_SHORT_EN'])
        if ('NAME_FORMAL_EN' in country and isinstance(country['NAME_FORMAL_EN'],str)):
            iso3codes += "* #" + country['CODE_ISO_3'] + ' "' + escape(country['NAME_SHORT_EN']) + '" "' + escape(country['NAME_FORMAL_EN']) + '"\n'
        else:
            iso3codes += "* #" + country['CODE_ISO_3'] + ' "' + escape(country['NAME_SHORT_EN']) +  '"\n'

        if ('GEO_M49_CODE' in country and isinstance(country['GEO_M49_CODE'],str)):
            if ('NAME_FORMAL_EN' in country and isinstance(country['NAME_FORMAL_EN'],str)):
                m49codes += "* #" + country['GEO_M49_CODE'] + ' "' + escape(country['NAME_SHORT_EN']) + '" "' + escape(country['NAME_FORMAL_EN']) + '"\n'
            else:
                m49codes += "* #" + country['GEO_M49_CODE'] + ' "' + escape(country['NAME_SHORT_EN']) +  '"\n'

            m49maps += "  * insert ElementMap(" + country['GEO_M49_CODE'] + "," + country['CODE_ISO_3']  +", equivalent)\n"
        if ('CODE_ISO_2' in country and isinstance(country['CODE_ISO_2'],str)):
            if ('NAME_FORMAL_EN' in country and isinstance(country['NAME_FORMAL_EN'],str)):
                iso2codes += "* #" + country['CODE_ISO_2'] + ' "' + escape(country['NAME_SHORT_EN']) + '" "' + escape(country['NAME_FORMAL_EN']) + '"\n'
            else:
                iso2codes += "* #" + country['CODE_ISO_2'] + ' "' + escape(country['NAME_SHORT_EN']) +  '"\n'
            iso2maps += "  * insert ElementMap(" + country['CODE_ISO_3'] + "," + country['CODE_ISO_2']  +", equivalent)\n"
    
            


    iso3valueset = "ValueSet: COUNTRYISO3\n"
    iso3valueset += 'Title: "WHO RefMart ISO3 Country List"\n'
    iso3valueset += 'Description: "ValueSet of ISO 3 codes for WHO RefMart Country and Jurisidiction List available at ' + refmart_country_list_url + '"\n'
    iso3valueset += '* ^status = #active\n'
    iso3valueset += '* ^experimental = true\n'
    iso3valueset += '* include codes from system COUNTRYISO3\n'

    iso2valueset = "ValueSet: COUNTRYISO2\n"
    iso2valueset += 'Title: "WHO RefMart ISO2 Country List"\n'
    iso2valueset += 'Description: "ValueSet of ISO 2 codes for WHO RefMart Country and Jurisidiction List available at ' + refmart_country_list_url + '"\n'
    iso2valueset += '* ^status = #active\n'
    iso2valueset += '* ^experimental = true\n'
    iso2valueset += '* include codes from system COUNTRYISO2\n'

    m49valueset = "ValueSet: COUNTRYM49\n"
    m49valueset += 'Title: "WHO RefMart M49 Country List"\n'
    m49valueset += 'Description: "ValueSet of M49 codes for WHO RefMart Country and Jurisidiction List available at ' + refmart_country_list_url + '"\n'
    m49valueset += '* ^status = #active\n'
    m49valueset += '* ^experimental = true\n'
    m49valueset += '* include codes from system COUNTRYM49\n'
    
    printout(iso3valueset,iso3_vs_filename)
    printout(iso3codes,iso3_cs_filename)
    printout(iso2valueset,iso2_vs_filename)
    printout(iso2codes,iso2_cs_filename)
    printout(m49valueset,m49_vs_filename)
    printout(m49codes,m49_cs_filename)
    printout(m49maps, m49_conceptmap_filename)
    printout(iso2maps,iso2_conceptmap_filename)

main()

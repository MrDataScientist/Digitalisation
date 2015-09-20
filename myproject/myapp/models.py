# -*- coding: utf-8 -*-
from __future__ import unicode_literals


########################################################################################################################
# Crossbar
########################################################################################################################
from django.db.models.expressions import F
from django.shortcuts import render
import crochet
crochet.setup()
from autobahn.twisted.wamp import Application
import logging

logging.basicConfig()
wapp = Application()

@crochet.wait_for(timeout=50)
def publish(topic, *args, **kwargs):
    return wapp.session.publish(topic, *args, **kwargs)

@crochet.wait_for(timeout=50)
def call(name, *args, **kwargs):
    return wapp.session.call(name, *args, **kwargs)

def register(name, *args, **kwargs):
    @crochet.run_in_reactor
    def decorator(func):
        wapp.register(name, *args, **kwargs)(func)

    return decorator

def subscribe(name, *args, **kwargs):
    @crochet.run_in_reactor
    def decorator(func):
        wapp.subscribe(name, *args, **kwargs)(func)

    return decorator

########################################################################################################################
# Customed
########################################################################################################################
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.forms.widgets import HiddenInput
from django.core.files.storage import FileSystemStorage
from django.contrib import admin
from django.db import models
from django.conf import settings

from lxml import etree
import arrow
from django import forms
import xml.etree.ElementTree as ET
import random
import datetime
import base64
import os
import tempfile
import sys


CONFIG = ET.parse("/home/hduser/Bureau/BeamLabs/Scripts/Python/config.xml")
root = CONFIG.getroot()
NUMBER_SERVER = int(root.find("CROSSBAR").find("number_server").text)

QUALITY_CHOICE = (
    ('A', 'Free'),
    ('B', 'Member'),
    ('C', 'Gold'),
    ('D', 'Premium'),
)

COUNTRIES = (
    ('France', 'France'),
)

COLOR = (
    ('r', 'Rouge'),
    ('b', 'Bleu'),
    ('v', 'Vert'),
)


PROVINCE = (
    ('Ain', 'Ain (01)'),
    ('Aisne', 'Aisne (02)'),
    ('Allier', 'Allier (03)'),
    ('Alpes-de-Haute-Provence', 'Alpes-de-Haute-Provence (04)'),
    ('Hautes-Alpes', 'Hautes-Alpes (05)'),
    ('Alpes-Maritimes', 'Alpes-Maritimes (06)'),
    ('Ardèche', 'Ardèche (07)'),
    ('Ardennes', 'Ardennes (08)'),
    ('Ariège', 'Ariège (09)'),
    ('Aube', 'Aube (10)'),
    ('Aude', 'Aude (11)'),
    ('Aveyron', 'Aveyron (12)'),
    ('Bouches-du-Rhône', 'Bouches-du-Rhône (13)'),
    ('Calvados', 'Calvados (14)'),
    ('Cantal', 'Cantal (15)'),
    ('Charente', 'Charente (16)'),
    ('Charente-Maritime', 'Charente-Maritime (17)'),
    ('Cher', 'Cher (18)'),
    ('Corrèze', 'Corrèze (19)'),
    ('Corse-du-Sud', 'Corse-du-Sud (2A)'),
    ('Haute-Corse', 'Haute-Corse (2B)'),
    ("Côte-d'Or", "Côte-d'Or (21)"),
    ("Côtes-d'Armor", "Côtes-d'Armor (22)"),
    ('Creuse', 'Creuse (23)'),
    ('Dordogne', 'Dordogne (24)'),
    ('Doubs', 'Doubs (25)'),
    ('Drôme', 'Drôme (26)'),
    ('Eure', 'Eure (27)'),
    ('Eure-et-Loir', 'Eure-et-Loir (28)'),
    ('Finistère', 'Finistère (29)'),
    ('Gard', 'Gard (30)'),
    ('Haute-Garonne', 'Haute-Garonne (31)'),
    ('Gers', 'Gers (32)'),
    ('Gironde', 'Gironde (33)'),
    ('Hérault', 'Hérault (34)'),
    ('Ille-et-Vilaine', 'Ille-et-Vilaine (35)'),
    ('Indre', 'Indre (36)'),
    ('Indre-et-Loire', 'Indre-et-Loire (37)'),
    ('Isère', 'Isère (38)'),
    ('Jura', 'Jura (39)'),
    ('Landes', 'Landes (40)'),
    ('Loir-et-Cher', 'Loir-et-Cher (41)'),
    ('Loire', 'Loire (42)'),
    ('Haute-Loire', 'Haute-Loire (43)'),
    ('Loire-Atlantique', 'Loire-Atlantique (44)'),
    ('Loiret', 'Loiret (45)'),
    ('Lot', 'Lot (46)'),
    ('Lot-et-Garonne', 'Lot-et-Garonne (47)'),
    ('Lozère', 'Lozère (48)'),
    ('Maine-et-Loire', 'Maine-et-Loire (49)'),
    ('Manche', 'Manche (50)'),
    ('Marne', 'Marne (51)'),
    ('Haute-Marne', 'Haute-Marne (52)'),
    ('Mayenne', 'Mayenne (53)'),
    ('Meurthe-et-Moselle', 'Meurthe-et-Moselle (54)'),
    ('Meuse', 'Meuse (55)'),
    ('Morbihan', 'Morbihan (56)'),
    ('Moselle', 'Moselle (57)'),
    ('Nièvre', 'Nièvre (58)'),
    ('Nord', 'Nord (59)'),
    ('Oise', 'Oise (60)'),
    ('Orne', 'Orne (61)'),
    ('Pas-de-Calais', 'Pas-de-Calais (62)'),
    ('Puy-de-Dôme', 'Puy-de-Dôme (63)'),
    ('Pyrénées-Atlantiques', 'Pyrénées-Atlantiques (64)'),
    ('Hautes-Pyrénées', 'Hautes-Pyrénées (65)'),
    ('Pyrénées-Orientales', 'Pyrénées-Orientales (66)'),
    ('Bas-Rhin', 'Bas-Rhin (67)'),
    ('Haut-Rhin', 'Haut-Rhin (68)'),
    ('Lyon', 'Lyon (69)'),
    ('Haute-Saône', 'Haute-Saône (70)'),
    ('Saône-et-Loire', 'Saône-et-Loire (71)'),
    ('Sarthe', 'Sarthe (72)'),
    ('Savoie', 'Savoie (73)'),
    ('Haute-Savoie', 'Haute-Savoie (74)'),
    ('Paris', 'Paris (75)'),
    ('Seine-Maritime', 'Seine-Maritime (76)'),
    ('Seine-et-Marne', 'Seine-et-Marne (77)'),
    ('Yvelines', 'Yvelines (78)'),
    ('Deux-Sèvres', 'Deux-Sèvres (79)'),
    ('Somme', 'Somme (80)'),
    ('Tarn', 'Tarn (81)'),
    ('Tarn-et-Garonne', 'Tarn-et-Garonne (82)'),
    ('Var', 'Var (83)'),
    ('Vaucluse', 'Vaucluse (84)'),
    ('Vendée', 'Vendée (85)'),
    ('Vienne', 'Vienne (86)'),
    ('Haute-Vienne', 'Haute-Vienne (87)'),
    ('Vosges', 'Vosges (88)'),
    ('Yonne', 'Yonne (89)'),
    ('Territoire de Belfort', 'Territoire de Belfort (90)'),
    ('Essonne', 'Essonne (91)'),
    ('Hauts-de-Seine', 'Hauts-de-Seine (92)'),
    ('Seine-Saint-Denis', 'Seine-Saint-Denis (93)'),
    ('Val-de-Marne', 'Val-de-Marne (94)'),
    ("Val-d'Oise", "Val-d'Oise (95)"),
    ('Guadeloupe', 'Guadeloupe (971)'),
    ('Martinique', 'Martinique (972)'),
    ('Guyane', 'Guyane (973)'),
    ('La Réunion', 'La Réunion (974)'),
    ('Mayotte', 'Mayotte (976)'),
)

AVAILABILITY_DATE_CHOICE = (
    ('1',  '1 mois'),    #1mois = 30 jours
    ('3',  '3 mois'),   #mois 1 31  / mois 2  30 / mois 3  31
    ('6',  '6 mois'),
    ('12', '1 an'),
)

TIME_ZONE = (
    ('CEST', 'France'),
    ('Etc/GMT', 'GMT'),
    ('Etc/GMT+1', 'GMT+1'),
    ('Etc/GMT+2', 'GMT+2'),
    ('Etc/GMT+3', 'GMT+3'),
    ('Etc/GMT+4', 'GMT+4'),
    ('Etc/GMT+5', 'GMT+5'),
    ('Etc/GMT+6', 'GMT+6'),
    ('Etc/GMT+7', 'GMT+7'),
    ('Etc/GMT+8', 'GMT+8'),
    ('Etc/GMT+9', 'GMT+9'),
    ('Etc/GMT+10', 'GMT+10'),
    ('Etc/GMT+11', 'GMT+11'),
    ('Etc/GMT+12', 'GMT+12'),
    ('Etc/GMT-1', 'GMT-1'),
    ('Etc/GMT-2', 'GMT-2'),
    ('Etc/GMT-3', 'GMT-3'),
    ('Etc/GMT-4', 'GMT-4'),
    ('Etc/GMT-5', 'GMT-5'),
    ('Etc/GMT-6', 'GMT-6'),
    ('Etc/GMT-7', 'GMT-7'),
    ('Etc/GMT-8', 'GMT-8'),
    ('Etc/GMT-9', 'GMT-9'),
    ('Etc/GMT-10', 'GMT-10'),
    ('Etc/GMT-11', 'GMT-11'),
    ('Etc/GMT-12', 'GMT-12'),
    ('Etc/GMT-13', 'GMT-13'),
    ('Etc/GMT-14', 'GMT-14'),
)

def get_image_path_admin(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'superadmin', str(instance.email), 'logo.png')
    try:
        os.remove(path)
    except:
        pass
    instance.logo.name = path
    return path

def get_image_path_template(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'template', str(instance.id), 'template.png')
    try:
        os.remove(path)
    except:
        pass
    instance.image.name = path
    return path

def get_image_path_structure(instance, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'structure', str(instance.id), 'structure.png')
    try:
        os.remove(path)
    except:
        pass
    instance.image.name = path
    return path


class MyCustomException(BaseException):
    """
    Customer exception to exit some loops
    """
    pass

########################################################################################################################
# Read database.
########################################################################################################################

############################################################
# CheckMail
############################################################
class CheckMail(object):
    def __init__(self, email):
        self.email = email.lower()
        self.string = None

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "CHECKMAIL")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def save(self, *args, **kwargs):
        ##############################################################
        # Consult Hbase
        ##############################################################
        self.string = call('read_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

    def is_available_mail_from_hbase(self):
        string = self.string
        root = ET.fromstring(self.string)
        try:
            raise MyCustomException(root.find('CHECKMAIL').find('ERROR').text)
        except MyCustomException:
            return False
        except Exception:
            pass

        try:
            return True if root.find('CHECKMAIL').find('None').text is None else False
        except:
            return False

############################################################
# Connexion
############################################################
class Connexion(object):
    def __init__(self, email, password, structure_template=True):
        self.email = email.lower()
        self.password = password
        self.string = None
        self.structure_template = structure_template

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "CONNEXION")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "password")
        el.text = self.password
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_structure(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "STRUCTURE")
        el = etree.SubElement(SA, "useless")
        el.text = 'useless'
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def save(self, *args, **kwargs):
        self.string = call('read_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())
        if self.structure_template:
            self.string_structure = call('read_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_structure())

    def is_successful_connection(self):
        root = ET.fromstring(self.string)
        try:
            raise MyCustomException(root.find('CONNEXION').find('ERROR').text)
        except MyCustomException:
            return False
        except Exception:
            return True

    def process(self, *args, **kwargs):
        root = ET.fromstring(self.string)

        if self.structure_template:
            self.process_structure()

        try:
            MAN = root.find("MANAGER")
            Manager.from_xml_string_to_model(MAN, *args, **kwargs)
            return
        except Exception as e:
            pass

        try:
            CL = root.find("CLIENT")
            Client.from_xml_string_to_model(CL, *args, **kwargs)
            return
        except Exception as e:
            pass

        try:
            SA = root.find("CONFIGSUPERADMIN")
            SuperAdmin.from_xml_string_to_model(SA, *args, **kwargs)
            return
        except Exception as e:
            pass

        return

    def process_structure(self, *args, **kwargs):
        root = ET.fromstring(self.string_structure)
        for structure in root.findall("STRUCTURE"):
            Structure.from_xml_string_to_model(structure, *args, **kwargs)

########################################################################################################################
# Models
########################################################################################################################
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=30, default='France', choices=COUNTRIES)
    province = models.CharField(max_length=30, choices=PROVINCE)
    code = models.CharField(max_length=5)
    street = models.CharField(max_length=100)
    number = models.IntegerField()

    def tostring(self):
        return "{}|{}|{}|{}|{}".format(self.country, self.province, self.code, self.street, str(self.number))

    @staticmethod
    def fromstring(string, *args, **kwargs):
        split = string.split('|')
        adress = Address(
            country = split[0],
            province = split[1],
            code = split[2],
            street = split[3],
            number = int(split[4]),
        )
        adress.save(*args, **kwargs)
        return adress

    def __str__(self):
        return "{} - {} - {}".format(self.street, self.province, self.country)

class AddressRegistration(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('country', 'province', 'code', 'street', 'number')
        labels = {
            'country': _("Pays"),
            'province': _("Département"),
            'code': _("Code postale"),
            'street': _("Adresse"),
            'number': _("Numéro de rue"),
        }

    def clean(self):
        for element in ['country', 'province', 'code', 'street']:
            if element in self.cleaned_data:
                if '|' in self.cleaned_data[element]:
                    raise forms.ValidationError(_("Le champs contient un caractère interdit"))

    def __init__(self, *args, **kwargs):
        super(AddressRegistration, self).__init__(*args, **kwargs)

class AddressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Général', {'fields': ['country', 'province', 'code', 'street', 'number']}),
    ]
    list_display = ('country', 'province', 'code', 'street', "number")
    form = AddressRegistration

admin.site.register(Address, AddressAdmin)

############################################################
# Structure
############################################################
class Structure(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    image = models.ImageField(
            upload_to=get_image_path_structure,
            default=os.path.join(settings.MEDIA_ROOT, 'default', 'structure.png'))

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "STRUCTURE")

        el = etree.SubElement(SA, "id")
        el.text = self.id

        with open(self.image.name, "rb") as imageFile:
            text = base64.b64encode(imageFile.read())
        if text is None:
            with open("/home/hduser/Bureau/BeamLabs/Scripts/django_1_7/pic_folder/default/structure.png", "rb") as imageFile:  #TODO: le chemain
                text = base64.b64encode(imageFile.read())
        el = etree.SubElement(SA, "image")
        el.text = text
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Template. i.e: The XML string has to start with <TEMPLATE>

        The steps are:
            - Add the template.

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """
        id = root.find('id').text
        image = root.find('image').text.decode('base64')

        # Step 1: Copy the content of the string into a file
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(image)

        # Step 2: Open the file via django
        reopen = open(temp_file.name, 'rb')
        django_file = File(reopen)
        temp_file.close()

        # Step 3: Create model
        structure = Structure(id=id)

        # Step 4: Add the picture
        path = get_image_path_structure(structure, None)
        structure.image.save(path, django_file, save=False)

        # Step 5: Save
        structure.save(hbase=False, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Django
        ##############################################################
        super(Structure, self).save(*args, **kwargs)

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

    def __str__(self):
        return self.id


class StructureRegistration(forms.ModelForm):
    class Meta:
        model = Structure
        fields = ('id', 'image')
        labels = {
            'id': _('Numéro de la structure'),
        }


class StructureAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Structure', {'fields': ['id', 'image']}),
    ]
    list_display = ('id', 'image')
    form = StructureRegistration


admin.site.register(Structure, StructureAdmin)


############################################################
# Client License
############################################################
class ClientLicense(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    admin = models.OneToOneField('SuperAdmin', on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=100)
    quality = models.CharField(max_length=1, choices=QUALITY_CHOICE)
    end = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=15, default='12', choices=AVAILABILITY_DATE_CHOICE)

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        end = arrow.get(self.end)
        year = str(end.year)
        month = str(end.month)
        if len(month) <= 1:
            month = '0'+month
        day = str(end.day)
        if len(day) <= 1:
            day = '0'+day

        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "CLIENTLICENCE")
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "quality")
        el.text = self.quality
        el = etree.SubElement(SA, "end")
        el.text = "{}/{}/{}".format(month, day, year)
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)

        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Client  License. i.e: The XML string has to start with <CLIENTLICENSE>

        The steps are:
            - Add the client license
            - Recursively add the manager licenses attached.

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """
        #####################################################################
        # STEP: 1
        # Parse the XML and Create the Client License
        #####################################################################
        date_fields = [int(a) for a in root.find("end").text.split("/")]

        license = ClientLicense(id=root.find('id').text,
                                # admin=None,
                                email=root.find("email").text,
                                quality=root.find('quality').text,
                                end=arrow.get(date_fields[2], date_fields[0], date_fields[1]).datetime,
                                duration=0
                                )
        license.save(hbase=False, *args, **kwargs)

        #####################################################################
        # STEP: 2
        # Parse the XML and recursively add the Manager Licenses
        #####################################################################
        for manager_license in root.findall('MANAGERLICENSE'):
            ManagerLicense.from_xml_string_to_model(manager_license, license, *args, **kwargs)

    def __str__(self):
        return self.id

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Pre-process
        ##############################################################
        self.email = self.email.lower()
        duration = int(self.duration)

        try:
            previous = self.end if not self.end is None else datetime.datetime.now()

        except:
            previous = datetime.datetime.now()

        end = datetime.datetime(year=previous.year + (duration // 12), month=previous.month, day=1)
        for _ in xrange(duration % 12):
            end = datetime.datetime(year=end.year, month=end.month+1, day=1) if end.month < 12 else datetime.datetime(year=end.year+1, month=1, day=1)
        self.end = end

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

        ##############################################################
        # Update Django
        ##############################################################
        super(ClientLicense, self).save(*args, **kwargs)


class ClientLicenseRegistration(forms.ModelForm):
    class Meta:
        model = ClientLicense
        fields = ('id', 'email', 'quality', 'duration')
        labels = {
            'id': _('Numéro de license'),
            'email': _("Adresse email de l'administrateur (obligatoire)"),
            'quality': _("Type de license"),
            'duration': _("Durée de l'abonnement"),
        }
        help_texts = {
            'id': _('Le numéro de license est disponible dans le mail qui vous à été envoyé'),
            'email': _('Cette adresse email vous sera utile pour vous connecter avec les droits d\'administrateur'),
            'quality': _("Le type de license conditionne l'accès à certaines fonctionnalitées."),
            'duration': _("Veuillez choisir la durée de l'abonnement dans la liste déroulante.")
        }
        error_messages = {
            'id': {
                'max_length': _(
                    "Le numéro de license ne doit contenir que des chiffres, des lettres et des underscores."),
            },
        }

    def __init__(self, *args, **kwargs):
        super(ClientLicenseRegistration, self).__init__(*args, **kwargs)


class ClienLicenseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Général', {'fields': ['id', 'quality', 'duration']}),
        ('Administrateur', {'fields': ['email']}),
    ]
    list_display = ('id', 'admin', 'quality', 'end', "email")
    form = ClientLicenseRegistration

admin.site.register(ClientLicense, ClienLicenseAdmin)

############################################################
# Super admin
############################################################
class SuperAdmin(models.Model):
    email = models.EmailField(max_length=100, primary_key=True)
    password = models.CharField(max_length=30)
    name_client = models.CharField(max_length=30)
    head_office = models.ForeignKey('Address')
    logo = models.ImageField(
        upload_to=get_image_path_admin,
        default=os.path.join(settings.MEDIA_ROOT, 'default', 'beamlabs.png'))

    client_license = models.OneToOneField('ClientLicense')

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "SUPERADMIN")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "password")
        el.text = self.password
        el = etree.SubElement(SA, "id_client_license")
        el.text = self.client_license.id
        el = etree.SubElement(SA, "name_client")
        el.text = self.name_client
        el = etree.SubElement(SA, "head_office")
        el.text = self.head_office.tostring()

        try:
            with open(self.logo.name, "rb") as imageFile:
                text = base64.b64encode(imageFile.read())

            if text is None:
                with open('/home/hduser/Bureau/BeamLabs/Scripts/django_1_7/pic_folder/default/beamlabs.png', "rb") as imageFile:
                    text = base64.b64encode(imageFile.read())
            el = etree.SubElement(SA, 'logo')
            el.text = text

        except:
            pass

        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Client  License. i.e: The XML string has to start with <SUPERADMIN>

        The steps are:
            - Add the client license (which in turn add sub-elements)
            - Add the Super Admin (which depends on the client license...)
            - Recursively add the clients attached.

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """

        #####################################################################
        # Step 1:
        # Add the client licenses in the database!
        #####################################################################
        ClientLicense.from_xml_string_to_model(root.find('CLIENTLICENSE'), *args, **kwargs)

        #####################################################################
        # Step 2:
        # Add the super admin in the database
        #####################################################################
        email = root.find('email').text
        password = root.find('password').text
        id_client_license = root.find('id_client_license').text
        name_client = root.find('name_client').text
        head_office = Address.fromstring(root.find('head_office').text)
        logo = root.find('logo').text.decode('base64')

        # Step 1: Copy the content of the string into a file
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(logo)

        # Step 2: Open the file via django
        reopen = open(temp_file.name, 'rb')
        django_file = File(reopen)
        temp_file.close()

        # Step 3: Create model
        id_session = kwargs.get('id_session', 'default')
        client_license = ClientLicense.objects.using(id_session).get(id=id_client_license)
        super_admin = SuperAdmin(email=email,
                                 password=password,
                                 name_client=name_client,
                                 head_office=head_office,
                                 client_license=client_license,
                                 )

        # Step 4: Add the picture
        path = get_image_path_admin(super_admin, None)
        super_admin.logo.save(path, django_file, save=False)

        # Step 5: Save
        super_admin.save(hbase=False, *args, **kwargs)

        #####################################################################
        # Step 3:
        # Add the clients in the database
        #####################################################################
        clients = root.findall("CLIENT")
        for client in clients:
            Client.from_xml_string_to_model(client, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Pre-processing
        ##############################################################
        self.email = self.email.lower()

        ##############################################################
        # Update Django
        ##############################################################
        if self.client_license.email != self.email:
            raise Exception("Adresse email incorrecte")

        # Update client license
        self.client_license.admin = self
        self.client_license.save(hbase=False, *args, **kwargs)

        # Set logo to default logo
        # path_temp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pic_folder', 'temp.png')
        # path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pic_folder', 'logo.png')
        # if os.path.isfile(path_temp):
        #     self.logo.image = path_temp
        #     self.logo.name = path
        #     os.remove(path_temp)
        # else:
        #     self.logo.name = path
        #
        # path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pic_folder', 'logo.png')
        # path_default = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pic_folder', 'beamlabs.png')
        # if os.path.isfile(path):
        #     os.remove(path)

        # if self.logo is None or self.logo.name is None:
        #     self.logo = path_default
        # self.logo.name = path
        super(SuperAdmin, self).save(*args, **kwargs)

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

    def __str__(self):
        return "{} - {}".format(self.name_client, self.head_office)


class SuperAdminRegistration(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Veuillez entrer un mot de passe"),
        help_text=_('Le mot de passe doit contenir un chiffres et une majuscule')
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Veuillez réecrire le mot de passe"),
    )

    class Meta:
        model = SuperAdmin
        fields = ('email', 'name_client', 'head_office', 'client_license', 'logo')
        labels = {
            'email': _('Adresse email administrateur'),
            'name_client': _('Nom de l\'entreprise'),
            'head_office': _('Siège social'),
            'client_license': _("Numéro de license"),
        }
        help_texts = {
            'email': _('Cette adresse email vous sera utile pour vous connecter avec les droits d\'administrateur'),
            'head_office': _('Adresse du siège sociale'),
        }

        # def clean_password(self):
        #     if len(self.cleaned_data['password']) < 8:
        #         raise forms.ValidationError(_("Le mot de passe doit contenir au moins 8 caractères!"))
        #     if self.cleaned_data['password'] == self.cleaned_data['password'].lower():
        #         raise forms.ValidationError(_("Le mot de passe doit contenir au moins une majuscule!"))
        #     return self.cleaned_data
        #
        # def clean(self):
        #     if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
        #         if self.cleaned_data['password'] != self.cleaned_data['password2']:
        #             raise forms.ValidationError(_("Le mot de passe ne correspond pas!"))
        #     return self.cleaned_data


class SuperAdminAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Général', {'fields': ['email', 'password', 'password2', 'name_client', 'head_office', 'logo']}),
        ('License', {'fields': ['client_license']}),
    ]
    list_display = ('email', 'client_license', 'name_client', 'head_office', 'logo')
    form = SuperAdminRegistration


admin.site.register(SuperAdmin, SuperAdminAdmin)

############################################################
# Client
############################################################
class Client(models.Model):
    email = models.EmailField(max_length=100, primary_key=True)
    password = models.CharField(max_length=30)
    admin = models.ForeignKey('SuperAdmin', null=True, blank=True)
    street = models.ForeignKey('Address')

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "CLIENT")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "password")
        el.text = self.password
        el = etree.SubElement(SA, "email_admin")
        el.text = self.admin.email
        el = etree.SubElement(SA, "street")
        el.text = self.street.tostring()
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_delete(self):
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "DELCLIENT")
        el = etree.SubElement(SA, "id")
        el.text = self.email
        if self.replacement:
            el = etree.SubElement(SA, "replacement")
            el.text = self.replacement.email
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Client. i.e: The XML string has to start with <CLIENT>

        The steps are:
            - Add the beacon_id.
            - Add the Client (which depends on the beacon_id).
            - Recursively add the Beacons.
            - Recursively add the Managers.
            - Recursively add the Calendar tasks.

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """

        email = root.find('email').text
        password = root.find('password').text
        email_admin = root.find('email_admin').text
        street = Address.fromstring(root.find('street').text)
        #TODO: replace find by 'pop'?
        #####################################################################
        # STEP 2:
        #   Add the client.
        #####################################################################
        id_session = kwargs.get('id_session', 'default')
        client = Client(email=email,
                        password=password,
                        admin=SuperAdmin.objects.using(id_session).get(email=email_admin) if SuperAdmin.objects.using(id_session).filter(email=email_admin).exists() else None,
                        street=street,
                        )
        client.save(hbase=False, *args, **kwargs)

        #####################################################################
        # STEP 3:
        #   Add Beacons.
        #####################################################################
        for beacon in root.findall("BEACON"):
            Beacon.from_xml_string_to_model(beacon, client, *args, **kwargs)

        #####################################################################
        # STEP 4:
        #   Add the managers.
        #####################################################################
        for manager in root.findall("MANAGER"):
            Manager.from_xml_string_to_model(manager, *args, **kwargs)

        #####################################################################
        # STEP 5:
        #   Add the calendar tasks.
        #####################################################################
        for calendarTask in root.findall("CALTASK"):
            ClientCalendarTask.from_xml_string_to_model(calendarTask, client, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Pre-processing
        ##############################################################
        self.email = self.email.lower()

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)),
                              self.to_hbase_input_xml_string())

        ##############################################################
        # Update Django
        ##############################################################
        super(Client, self).save(*args, **kwargs)

    def delete(self, hbase=True, *args, **kwargs):
        ##############################################################
        #
        ##############################################################
        self.replacement = None
        try:
            replacement = Client.objects.get(email=kwargs.pop('replacement', ''))
            if replacement:
                self.replacement = replacement
        except:
            pass


        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_delete())

        ##############################################################
        # Update Django
        ##############################################################
        if self.replacement:
            id_session = kwargs.get('id_session', 'default')
            managers = Manager.objects.using(id_session).filter(client=self)
            for manager in managers:
                manager.client = self.replacement
                manager.save(hbase=False, *args, **kwargs)

        super(Client, self).delete(*args, **kwargs)

    def __str__(self):
        return "{} : {}".format(self.admin.name_client , self.street.street)


class ClientRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                               label=_("Veuillez entrer un mot de passe"),
                               help_text=_('Le mot de passe doit contenir des chiffres et une majuscule')
                               )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Veuillez réecrire le mot de passe"),
    )

    class Meta:
        model = Client
        fields = ('email', 'admin', 'street')
        labels = {
            'email': _('Adresse email'),
            'admin': _('Administrateur'),
            'street': _('Adresse de l\'établissement'),
            # 'beacon_id': _("Identifiant balise"),
        }
        # help_texts = {
        #     'beacon_id': _('Cette identifiant est facultatif. Il est disponible sur les balises envoyées par Beamlans'),
        # }

        # def clean_password(self):
        #     if len(self.cleaned_data['password']) < 8:
        #         raise forms.ValidationError(_("Le mot de passe doit contenir au moins 8 caractères!"))
        #     if self.cleaned_data['password'] == self.cleaned_data['password'].lower():
        #         raise forms.ValidationError(_("Le mot de passe doit contenir au moins une majuscule!"))
        #     return self.cleaned_data
        #
        # def clean(self):
        #     if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
        #         if self.cleaned_data['password'] != self.cleaned_data['password2']:
        #             raise forms.ValidationError(_("Le mot de passe ne correspond pas!"))
        #     return self.cleaned_data


class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Général', {'fields': ['email', 'password', 'password2', 'street']}),
        ('Administrateur', {'fields': ['admin']}),
    ]
    list_display = ('email', 'admin', 'street')
    form = ClientRegistration


admin.site.register(Client, ClientAdmin)

############################################################
# Beacon
############################################################
class Beacon(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    number = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    client = models.ForeignKey('Client')

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "CLIENTBEACONS")
        el = etree.SubElement(SA, "email")
        el.text = self.client.email
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, 'number')
        el.text = self.number
        el = etree.SubElement(SA, 'description')
        el.text = self.description
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, client, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Beacon. i.e: The XML string has to start with <BEACON>

        The steps are:
            - Add the beacon.
            - Recursively add the Templates.


        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """
        #####################################################################
        # STEP 1:
        #   Add the beacon
        #####################################################################
        id = root.find("id").text
        number = root.find('number').text
        description = root.find("description").text

        beacon = Beacon(id=id,
                        number=number,
                        description=description,
                        client=client,
                        )
        beacon.save(hbase=False, *args, **kwargs)

        #####################################################################
        # STEP 2:
        #   Add the templates
        #####################################################################
        for template in root.findall("TEMPLATE"):
            Template.from_xml_string_to_model(template, beacon, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

        ##############################################################
        # Update Django
        ##############################################################
        super(Beacon, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class BeaconRegistration(forms.ModelForm):
    class Meta:
        model = Beacon
        fields = ('id', 'number', 'description', 'client')
        labels = {
            'id': _('Identifiant balise'),
            'number': _('Numéro de balise'),
            'description': _("Description de la balise"),
            'client': _("Nom de l'établissement"),
        }
        help_texts = {
            'description': _(
                "Cette description vous sera utile pour répérer la balise. Exemple: Entrée, Allée du milieu, etc..."),
        }


class BeaconAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Beacon', {'fields': ['description', 'id', 'number']}),
        ('Établissement', {'fields': ['client']}),
    ]
    list_display = ('description', 'id', 'number', 'client')
    form = BeaconRegistration


admin.site.register(Beacon, BeaconAdmin)

############################################################
# Template
############################################################
class Template(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=30)
    structure = models.IntegerField(default=0)
    color = models.CharField(max_length=10, default='r', choices=COLOR)

    image = models.ImageField(
            upload_to=get_image_path_template,
            default=os.path.join(settings.MEDIA_ROOT, 'default', 'beamlabs.png'))

    coordonnee_x = models.IntegerField()
    coordonnee_y = models.IntegerField()
    text_1 = models.CharField(max_length=100)
    text_2 = models.CharField(max_length=100)
    redirection = models.CharField(max_length=300)
    paypal = models.BooleanField(default=False)
    reseaux_sociaux = models.BooleanField(default=False)
    debut_campagne = models.DateTimeField()
    fin_campagne = models.DateTimeField()

    beacon = models.ForeignKey('Beacon', blank=True, null=True)

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "TEMPLATE")
        el = etree.SubElement(SA, "id")
        el.text = self.id

        with open(self.image.name, "rb") as imageFile:
            image = base64.b64encode(imageFile.read())

        if image is None:
            with open("/home/hduser/Bureau/BeamLabs/Scripts/django_1_7/pic_folder/default/beamlabs.png", "rb") as imageFile:
                image = base64.b64encode(imageFile.read())

        el = etree.SubElement(SA, "param")
        el.text = '|'.join(
            [self.description,
             str(self.structure),
             self.color,
             image,
             str(self.coordonnee_x),
             str(self.coordonnee_y),
             self.text_1,
             self.text_2,
             self.redirection,
             str(self.paypal),
             str(self.reseaux_sociaux),
             str(arrow.get(self.debut_campagne).timestamp),
             str(arrow.get(self.fin_campagne).timestamp)
             ])

        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_delete(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "DELTEMPLATE")
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, beacon, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Template. i.e: The XML string has to start with <TEMPLATE>

        The steps are:
            - Add the template.

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """
        id = root.find('id').text
        params = root.find('param').text.split('|')
        # Description, structure, color, logo, x, y, t1, t2, url, paypal, fb, begin, end
        logo = params[3].decode('base64')

        # Step 1: Copy the content of the string into a file
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(logo)

        # Step 2: Open the file with Django;
        reopen = open(temp_file.name, 'rb')
        django_file = File(reopen)
        temp_file.close()

        # Step 3: Create the model
        template = Template(id=id,
                            description = params[0],
                            structure=int(params[1]),
                            color=params[2],
                            coordonnee_x=int(params[4]),
                            coordonnee_y=int(params[5]),
                            text_1=params[6],
                            text_2=params[7],
                            redirection=params[8],
                            paypal= True if params[9] == 'True' else False,
                            reseaux_sociaux=True if params[10] == 'True' else False,
                            debut_campagne=arrow.get(params[11]).datetime,
                            fin_campagne=arrow.get(params[12]).datetime,
                            beacon=beacon,
                            )

        # Step 4: Connect the image
        path = get_image_path_template(template, None)
        template.image.save(path, django_file, save=False)

        # Step 5: Save
        template.save(hbase=False, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Django
        ##############################################################
        super(Template, self).save(*args, **kwargs)

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

    def delete(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_delete())

        ##############################################################
        # Update Django
        ##############################################################
        super(Template, self).delete(*args, **kwargs)

    def __str__(self):
        return self.id


class TemplateRegistration(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('id', 'description', 'structure', 'color', 'image', 'coordonnee_x', 'coordonnee_y', 'text_1', 'text_2', 'redirection', 'paypal', 'reseaux_sociaux', 'debut_campagne', 'fin_campagne', 'beacon')
        labels = {
            'id': _('Numéro de template'),
        }


class TemplateAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Template', {'fields': ['id', 'description', 'structure', 'image', 'color', 'coordonnee_x', 'coordonnee_y', 'text_1', 'text_2', 'redirection', 'paypal', 'reseaux_sociaux', 'debut_campagne', 'fin_campagne', 'beacon']}),
    ]
    list_display = ('id', 'description', 'structure', 'color', 'image', 'coordonnee_x', 'coordonnee_y', 'text_1', 'text_2', 'redirection', 'paypal', 'reseaux_sociaux', 'debut_campagne', 'fin_campagne', 'beacon')
    form = TemplateRegistration


admin.site.register(Template, TemplateAdmin)

############################################################
# Template Beacon
############################################################
class TemplateBeacon(models.Model):
    beacon = models.ForeignKey('Beacon')
    template = models.ForeignKey('Template')

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "BEACONTEMPLATE")
        el = etree.SubElement(SA, "id")
        el.text = self.beacon.id
        el = etree.SubElement(SA, "number")
        el.text = self.beacon.number
        el = etree.SubElement(SA, "template")
        el.text = self.template.id
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

        ##############################################################
        # Update Django
        ##############################################################
        self.template.beacon = self.beacon
        self.template.save(hbase=False, *args, **kwargs)


class TemplateBeaconRegistration(forms.ModelForm):
    class Meta:
        model = TemplateBeacon
        fields = ('beacon', 'template')
        labels = {
            'id': _('Balise'),
            'template': _('Template'),
        }


class TemplateBeaconAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Balise', {'fields': ['beacon']}),
        ('Template', {'fields': ['template']}),
    ]
    list_display = ('beacon', 'template')
    form = TemplateBeaconRegistration


admin.site.register(TemplateBeacon, TemplateBeaconAdmin)


############################################################
# Manager
############################################################
class Manager(models.Model):
    email = models.EmailField(max_length=100, primary_key=True)
    password = models.CharField(max_length=30)
    client = models.ForeignKey('Client', null=True, blank=True)
    first_name = models.CharField(max_length=30)
    family_name = models.CharField(max_length=50)
    profil = models.CharField(max_length=900, default='')
    position = models.CharField(max_length=100, default='Manager')
    license = models.OneToOneField('ManagerLicense', related_name="license_attached", on_delete=models.SET_NULL,
                                   blank=True, null=True)

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "MANAGER")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "password")
        el.text = self.password
        el = etree.SubElement(SA, "email_client")
        el.text = self.client.email
        el = etree.SubElement(SA, "first_name")
        el.text = self.first_name
        el = etree.SubElement(SA, "family_name")
        el.text = self.family_name
        el = etree.SubElement(SA, "position")
        el.text = self.position
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_delete(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "DELMANAGER")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)

        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_profil(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "PROFILMANAGER")
        el = etree.SubElement(SA, "email")
        el.text = self.email
        el = etree.SubElement(SA, "profil")
        el.text = self.profil or ''

        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        # tring = etree.tostring(el_tree, encoding='utf-8', pretty_print=True)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the manager. i.e: The XML string has to start with <MANAGER>

        The steps are:
            - Add the manager
            - Recursively add the calendar tasks

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """

        #####################################################################
        # STEP 1:
        #   Add the manager
        #####################################################################
        email = root.find('email').text
        password = root.find('password').text
        email_client = root.find("email_client").text
        first_name = root.find('first_name').text
        family_name = root.find('family_name').text
        position = root.find('position').text
        profil = root.find('profil').text
        license = root.find('license').text

        id_session = kwargs.get('id_session', 'default')

        manager = Manager(email=email,
                          password=password,
                          client=Client.objects.using(id_session).get(email=email_client) if Client.objects.using(id_session).filter(email=email_client).exists() else None,
                          first_name=first_name,
                          family_name=family_name,
                          position=position,
                          profil=profil or '',
        )

        if ManagerLicense.objects.using(id_session).filter(id=license).exists():
            #####################################################################
            # Update a maanger license
            #####################################################################
            manager_license = ManagerLicense.objects.using(id_session).get(id=license)
            manager_license.manager = manager
            manager_license.save(hbase=False, *args, **kwargs)

            #####################################################################
            # Update manager
            #####################################################################
            manager.license = manager_license

        manager.save(hbase=False, *args, **kwargs)

        #####################################################################
        # STEP 2:
        #   Add the calendar tasks.
        #####################################################################
        # for calendar_task in root.findall('CALTASK'):
        #     ClientCalendarTask.from_xml_string_to_model(calendar_task, client)

    def update_profil(self, hbase=True, *args, **kwargs):
        profil = kwargs.pop('profil', '')
        self.profil = profil

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_profil())

        ##############################################################
        # Update Django
        ##############################################################
        self.save(hbase=False, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Pre-processing
        ##############################################################
        self.email = self.email.lower()

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

        ##############################################################
        # Update Django
        ##############################################################
        if self.license:
            if not self.license.manager == self:
                self.license.manager = self
                self.license.save(hbase=False, *args, **kwargs)
        super(Manager, self).save(*args, **kwargs)

    def delete(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_delete())

        ##############################################################
        # Update Django
        ##############################################################
        id_session = kwargs.get('id_session', 'default')
        if ManagerLicense.objects.using(id_session).filter(manager=self.email).exists():
            manager_license = ManagerLicense.objects.using(id_session).get(manager=self.email)
            manager_license.manager = None
            manager_license.save(hbase=False, *args, **kwargs)

        super(Manager, self).delete(*args, **kwargs)

    def __str__(self):
        return self.email


class ManagerRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                               label=_("Veuillez entrer un mot de passe"),
                               help_text=_('Le mot de passe doit contenir des chiffres et une majuscule')
                               )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Veuillez réecrire le mot de passe"),
    )

    class Meta:
        model = Manager
        fields = ('email', 'password', 'client', 'first_name', 'family_name', 'position')
        labels = {
            'email': _('Adresse email du manager'),
            'client': _('Établissement'),
            'first_name': _('Prénom'),
            'family_name': _('Nom'),
            'position': _('Profession'),
        }

class ManagerUpdateProfilRegistration(forms.Form):

    manager = forms.ModelChoiceField(queryset=Manager.objects.all())
    profil = forms.CharField(
        max_length=3000,
        label=_("Profil désiré"),
    )

    def save(self, *args, **kwargs):
        manager = self.fields['manager'].queryset
        if manager:
            kwargs['profil'] = self.fields['profil'].queryset or ''
            manager.update_profil(*args, **kwargs)

    def __init__(self, manager=None, profil=None, *args, **kwargs):
        super(ManagerUpdateProfilRegistration, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = manager
        self.fields['profil'].queryset = profil


class ManagerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Général', {'fields': ['first_name', 'family_name', 'email', 'password', 'password2', 'position']}),
        ('Établissement associé', {'fields': ['client']}),
        ('License (optionnel)', {'fields': ['license']}),
    ]
    list_display = ('email', 'client', 'first_name', 'family_name', 'position', 'license', 'profil')
    form = ManagerRegistration


admin.site.register(Manager, ManagerAdmin)

############################################################
# Manager License
############################################################
class ManagerLicense(models.Model):
    client_license = models.ForeignKey('ClientLicense')
    id = models.CharField(max_length=30, primary_key=True)

    quality = models.CharField(max_length=1, choices=QUALITY_CHOICE)
    manager = models.OneToOneField('Manager', related_name="manager_attached", on_delete=models.SET_NULL, blank=True,
                                   null=True)

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "LICENSEMANAGER")
        el = etree.SubElement(SA, "email")
        el.text = self.client_license.admin.email
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, "quality")
        el.text = self.quality
        el = etree.SubElement(SA, "manager")
        el.text = self.manager.email if not self.manager is None else None

        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_delete(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "REMOVELICENSEMANAGER")
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, "client_license")
        el.text = self.client_license.id
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    def to_hbase_input_xml_string_attrib(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "ATTRIBLICENSEMANAGER")
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, "manager")
        el.text = self.manager.email if self.manager else "none"
        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, client_license, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the manager  License. i.e: The XML string has to start with <MANAGERLICENSE>

        The steps are:
            - Add the manager license
            - Recursively add the managers attached.

        :param root: Root in a XML tre
        :type root: Tree
        :param id_super_admin: This function takes an additional parameter, the id of the super admin.
        :type id_super_admin: String
        :return: This function does not return anything but populates the database.
        :rtype: void
        """

        #####################################################################
        # STEP 1:
        #   Add the manager license
        #####################################################################
        manager_license = ManagerLicense(
            client_license=client_license,
            id=root.find('id').text,
            manager=None,
            quality=root.find('quality').text,
        )
        manager_license.save(hbase=False, *args, **kwargs)

    def attrib(self, hbase=True, *args, **kwargs):
        """
        Connect a manager license and a manager

        :param args:
        :param kwargs:
        :return:
        """
        ##############################################################
        #
        ##############################################################
        manager = kwargs.pop('manager', None)

        if manager:
            self.manager = manager
            super(ManagerLicense, self).save(*args, **kwargs)

            self.manager.license = self
            super(Manager, self.manager).save(*args, **kwargs)

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_attrib())

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

        ##############################################################
        # Update Django
        ##############################################################
        if hbase and self.manager:
            if not self.manager.license == self:
                self.manager.license = self
                self.manager.save(hbase=False, *args, **kwargs)
        super(ManagerLicense, self).save(*args, **kwargs)

    def delete(self, hbase=True, *args, **kwargs):
        """
        Delete a manager license in the database

        :param args:
        :param kwargs:
        :return:
        """
        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string_delete())

        ##############################################################
        # Update Django
        ##############################################################
        if self.manager:
            self.manager.license = None
            self.manager.save(hbase=False, *args, **kwargs)

        super(ManagerLicense, self).delete(*args, **kwargs)

    def __str__(self):
        return self.id


class ManagerLicenseRegistration(forms.ModelForm):
    class Meta:
        model = ManagerLicense
        fields = ('client_license', 'id', 'quality', 'manager')
        labels = {
            'client_license': _('Numéro de la super license'),
            'id': _('Numéro de license'),
            'quality': _("Type de license"),
            'manager': _("Adresse email du manager"),
        }
        help_texts = {
            'quality': _("Le type de license conditionne l'accès à certaines fonctionnalitées."),
            'manager': _("Il est possible d'affecter directement cette license à un manager"),
        }

class ManagerLicenseAttribRegistration(forms.Form):
    manager_license = forms.ModelChoiceField(
        queryset=ManagerLicense.objects.all(),
        label = _("License manager"),
        help_text = _("Vous pouvez retrouver le numéro de license dans votre espace personnel"),
    )
    manager = forms.ModelChoiceField(
        queryset=Manager.objects.all(),
        label = _("Adresse email du manager"),
    )

    def save(self, *args, **kwargs):
        manager_license = self.fields['manager_license'].queryset or None
        kwargs['manager'] = self.fields['manager'].queryset or None
        manager_license.attrib(*args, **kwargs)

    def __init__(self, manager, manager_license, *args, **kwargs):
        super(ManagerLicenseAttribRegistration, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = manager
        self.fields['manager_license'].queryset = manager_license

class ManagerLicenseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('License', {'fields': ['id', 'client_license', 'quality']}),
        ('Manager', {'fields': ['manager']}),
    ]
    list_display = ('id', 'client_license', 'quality', 'manager')
    form = ManagerLicenseRegistration


admin.site.register(ManagerLicense, ManagerLicenseAdmin)

############################################################
# Manager License Attrib
############################################################
# class ManagerLicenseAttrib(models.Model):
#     manager_license = models.ForeignKey('ManagerLicense')
#     manager = models.ForeignKey('Manager')
#
#     def to_hbase_input_xml_string(self):
#         """
#         Turn a model into an XML string compatible with the database.
#
#         The structure of the XML string is shown in the document called "Communication Protocol".
#
#         :return: XML string
#         :rtype: string
#         """
#         tree = etree.Element("ROOT")
#         SA = etree.SubElement(tree, "ATTRIBLICENSEMANAGER")
#         el = etree.SubElement(SA, "id")
#         el.text = self.manager_license.id
#         el = etree.SubElement(SA, "manager")
#         el.text = self.manager.email
#         el = etree.SubElement(SA, "stamp")
#         el.text = str(1000 * arrow.utcnow().timestamp)
#         el_tree = etree.ElementTree(tree)
#         return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)
#
#     def save(self, hbase=True, *args, **kwargs):
#         """
#         Connect a manager license and a manager
#
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         ##############################################################
#         # Update Hbase
#         ##############################################################
#         if hbase:
#             result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())
#
#         ##############################################################
#         # Update Django
#         ##############################################################
#         self.manager_license.manager = self.manager
#         self.manager_license.save(hbase=False, *args, **kwargs)
#
#         self.manager.license = self.manager_license
#         self.manager.save(hbase=False, *args, **kwargs)
#
#     def __str__(self):
#         return self.id
#
#
# class ManagerLicenseAttribRegistration(forms.ModelForm):
#     class Meta:
#         model = ManagerLicenseAttrib
#         fields = ('manager_license', 'manager')
#         labels = {
#             'manager_license': _('Numéro de license'),
#             'manager': _("Adresse email du manager"),
#         }
#         help_texts = {
#             'manager_license': _("Vous pouvez retrouver le numéro de license dans votre espace personnel"),
#         }
#
#
# class ManagerLicenseAttribAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('License', {'fields': ['manager_license']}),
#         ('Manager', {'fields': ['manager']}),
#
#     ]
#     list_display = ('manager_license', 'manager')
#     form = ManagerLicenseAttribRegistration
#
#
# admin.site.register(ManagerLicenseAttrib, ManagerLicenseAttribAdmin)



###########################################################
# Client Calendar Task
############################################################
class ClientCalendarTask(models.Model):
    creator = models.CharField(max_length=30)
    id = models.CharField(max_length=50, primary_key=True)
    client = models.ForeignKey('Client')
    description = models.CharField(max_length=30)
    debut = models.DateTimeField()
    fin = models.DateTimeField()
    timeZone = models.CharField(max_length=30, choices=TIME_ZONE)
    room = models.CharField(max_length=30)
    followers = models.ManyToManyField('Manager', blank=True)

    def to_hbase_input_xml_string(self):
        """
        Turn a model into an XML string compatible with the database.

        The structure of the XML string is shown in the document called "Communication Protocol".

        :return: XML string
        :rtype: string
        """
        tree = etree.Element("ROOT")
        SA = etree.SubElement(tree, "CALTASK")
        el = etree.SubElement(SA, "creator")
        el.text = self.creator
        el = etree.SubElement(SA, "id")
        el.text = self.id
        el = etree.SubElement(SA, "email_client")
        el.text = self.client.email
        el = etree.SubElement(SA, "description")
        el.text = self.description
        el = etree.SubElement(SA, "deadline")
        el.text = str(1000 * arrow.get(self.fin).to('utc').timestamp)
        el = etree.SubElement(SA, "timeZone")
        el.text = self.timeZone
        el = etree.SubElement(SA, "duration")
        el.text = str(arrow.get(self.fin).timestamp - arrow.get(self.debut).timestamp)
        el = etree.SubElement(SA, "room")
        el.text = self.room

        el = etree.SubElement(SA, "follower")
        text = ','.join([follower.email for follower in self.followers.all()])
        el.text = text if len(text) > 0 else str(None)

        el = etree.SubElement(SA, "stamp")
        el.text = str(1000 * arrow.utcnow().timestamp)
        el_tree = etree.ElementTree(tree)
        return etree.tostring(el_tree, encoding="utf-8", pretty_print=True)

    @staticmethod
    def from_xml_string_to_model(root, client, *args, **kwargs):
        """
        This function is used to parse an XML string issued by WidgetManager into an object of this model.

        This function is specialized for the Calendar task. i.e: The XML string has to start with <CALENDARTASK>

        The steps are:
            - Add the calendar task.

        :param root: Root in a XML tre
        :type root: Tree
        :return: This function does not return anything but populates the database.
        :rtype: void
        """

        #####################################################################
        # STEP 1
        #####################################################################
        creator = root.find('creator').text
        id_task = root.find('id').text
        description = root.find('description').text
        deadline = root.find('deadline').text
        timeZone = root.find('timeZone').text
        duration = root.find('duration').text
        room = root.find('room').text
        # follower = ','.join([id.text for id in root.find('Followers').findall('id')])
        followers = [id.text for id in root.find('Followers').findall('id')]

        fin = arrow.get(int(deadline) / 1000).datetime
        debut = arrow.get(int(deadline) / 1000 - int(duration)).datetime

        calendar_task = ClientCalendarTask(
            creator=creator,
            id=id_task,
            client=client,
            description=description,
            debut=debut,
            fin=fin,
            timeZone=timeZone,
            room=room,
        )
        for follower in followers:
            manager =  Manager.objects.get(id=follower) if Manager.objects.filter(id=follower).exist() else None
            calendar_task.followers.add(manager)

        calendar_task.save(hbase=False, *args, **kwargs)

    def save(self, hbase=True, *args, **kwargs):
        ##############################################################
        # Update Django
        ##############################################################
        super(ClientCalendarTask, self).save(*args, **kwargs)

        ##############################################################
        # Update Hbase
        ##############################################################
        if hbase:
            result = call('write_database_SC' + str(random.randint(1, NUMBER_SERVER)), self.to_hbase_input_xml_string())

    def __str__(self):
        return self.id


class ClientCalendarTaskRegistration(forms.ModelForm):
    class Meta:
        model = ClientCalendarTask
        fields = ('creator', 'id', 'client', 'description',
                  'debut', 'fin', 'timeZone',
                  'room')
        labels = {
            'creator': _('Créateur de l\'évenement'),
            'id': _('ID'),
            'client': _('Client'),
            'description': _('Description'),
            'debut': _('Début de l\événement'),
            'fin': _('Fin de l\'événement'),
            'timeZone': _('Heure locale'),
            'room': _('Localisation de l\'événement'),
        }

    followers = forms.ModelMultipleChoiceField(queryset=Manager.objects.all())


class ClientCalendarTaskAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Createur', {'fields': ['creator']}),
        ('Événement', {'fields': ['description', 'client', 'room']}),
        ('Time', {'fields': ['debut', 'fin', 'timeZone']}),
        (None, {'fields': ['id']}),
        ('Participants', {'fields': ['followers']})
    ]
    list_display = ('creator', 'id', 'client', 'description', 'debut', 'fin', 'timeZone', 'room', 'get_followers')
    form = ClientCalendarTaskRegistration

    def get_followers(self, obj):
        return "\n".join([p.email for p in obj.followers.all()])


admin.site.register(ClientCalendarTask, ClientCalendarTaskAdmin)

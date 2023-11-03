import subprocess
import threading
from django.core.management.base import BaseCommand
from rightmove.models import Area
from rightmove.tasks import scrape_properties
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run multiple commands in parallel"

    def handle(self, *args, **options):
        # Define the commands to run in parallel
        self.create_areas()
        self.create_superuser()

    def create_superuser(self):
        # Check if the superuser already exists
        if not User.objects.filter(username="admin").exists():
            user = User()
            user.username = "admin"
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.set_password = "1234"
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists."))

    def create_areas(self):
    
        areas_list = [
            {"name": "Amber Valley", "zip_codes": ["DE5"]},
            {"name": "Ashfield", "zip_codes": ["NG17"]},
            {"name": "Bassetlaw", "zip_codes": ["DN22"]},
            {"name": "Birmingham", "zip_codes": ["B1"]},
            {"name": "Blaby", "zip_codes": ["LE8"]},
            {"name": "Bolsover", "zip_codes": ["S44"]},
            {"name": "Boston", "zip_codes": ["PE21"]},
            {"name": "Bromsgrove and Redditch", "zip_codes": ["B96", "B97"]},
            {"name": "Broxtowe", "zip_codes": ["NG9"]},
            {"name": "Cannock Chase", "zip_codes": ["WS11", "WS12"]},
            {"name": "Charnwood", "zip_codes": ["LE11", "LE12"]},
            {"name": "Chesterfield", "zip_codes": ["S40", "S41"]},
            {"name": "Derby", "zip_codes": ["DE1"]},
            {"name": "Derbyshire Dales", "zip_codes": ["DE4"]},
            {"name": "East Lindsey", "zip_codes": ["LN11", "LN12", "LN13"]},
            {"name": "East Staffordshire", "zip_codes": ["DE14"]},
            {"name": "Erewash", "zip_codes": ["DE7"]},
            {"name": "Gedling", "zip_codes": ["NG4", "NG5"]},
            {"name": "Harborough", "zip_codes": ["LE16"]},
            {"name": "Herefordshire County of", "zip_codes": ["HR1", "HR2"]},
            {"name": "High Peak", "zip_codes": ["SK22", "SK23"]},
            {"name": "Hinckley & Bosworth", "zip_codes": ["LE10", "LE9"]},
            {"name": "Huntingdonshire", "zip_codes": ["PE29", "PE28"]},
            {"name": "Leicester", "zip_codes": ["LE1"]},
            {"name": "Lichfield", "zip_codes": ["WS13"]},
            {"name": "Malvern Hills", "zip_codes": ["WR13", "WR14"]},
            {"name": "Mansfield", "zip_codes": ["NG18", "NG19", "NG21"]},
            {"name": "Melton", "zip_codes": ["LE13"]},
            {
                "name": "Newark and Sherwood",
                "zip_codes": ["NG22", "NG23", "NG24", "NG25"],
            },
            {"name": "Newcastle-under-Lyme", "zip_codes": ["ST5"]},
            {"name": "North East Derbyshire", "zip_codes": ["S42", "S43"]},
            {"name": "North Kesteven", "zip_codes": ["NG31", "NG32", "NG33", "NG34"]},
            {"name": "North Northamptonshire", "zip_codes": ["NN10", "NN15", "NN16"]},
            {"name": "North Warwickshire", "zip_codes": ["CV9", "B79"]},
            {"name": "North West Leicestershire", "zip_codes": ["LE65", "DE12"]},
            {"name": "Nottingham", "zip_codes": ["NG1"]},
            {"name": "Nuneaton and Bedworth", "zip_codes": ["CV10", "CV11", "CV12"]},
            {"name": "Oadby & Wigston", "zip_codes": ["LE18", "LE2"]},
            {"name": "Rugby", "zip_codes": ["CV21", "CV22", "CV23"]},
            {"name": "Rushcliffe", "zip_codes": ["NG11", "NG12", "NG2", "NG3", "NG4"]},
            {"name": "Rutland", "zip_codes": ["LE15"]},
            {"name": "Shropshire", "zip_codes": ["SY1", "SY2", "SY3", "SY4", "SY5"]},
            {"name": "Solihull", "zip_codes": ["B90", "B91", "B92", "B93", "B94"]},
            {"name": "South Derbyshire", "zip_codes": ["DE11", "DE12", "DE65"]},
            {"name": "South Holland", "zip_codes": ["PE11", "PE12", "PE20", "PE21"]},
            {"name": "South Kesteven", "zip_codes": ["NG31", "NG32", "NG33", "NG34"]},
            {
                "name": "South Staffordshire",
                "zip_codes": ["ST16", "ST17", "ST18", "ST19"],
            },
            {"name": "Staffordshire Moorlands", "zip_codes": ["ST13", "ST9"]},
            {"name": "Stratford-upon-Avon", "zip_codes": ["CV37", "CV36"]},
            {"name": "Tamworth", "zip_codes": ["B77", "B78"]},
            {
                "name": "Telford and Wrekin",
                "zip_codes": ["TF1", "TF2", "TF3", "TF4", "TF5"],
            },
            {"name": "Warwick", "zip_codes": ["CV34", "CV35", "CV37"]},
            {
                "name": "West Northamptonshire",
                "zip_codes": ["NN1", "NN2", "NN3", "NN4", "NN5"],
            },
            {"name": "Worcester", "zip_codes": ["WR1", "WR2", "WR3", "WR4", "WR5"]},
            {"name": "Wychavon", "zip_codes": ["WR10", "WR11", "WR12", "WR7", "WR8"]},
            {
                "name": "Wyre Forest",
                "zip_codes": ["DY10", "DY11", "DY12", "DY13", "DY14"],
            },
            {
                "name": "Babergh/Mid Suffolk Breckland",
                "zip_codes": ["IP22", "IP23", "IP24", "IP31"],
            },
            {
                "name": "Broadlands/South Norfolk",
                "zip_codes": ["NR15", "NR16", "NR18", "NR35"],
            },
            {"name": "Cambridge", "zip_codes": ["CB1", "CB2", "CB3", "CB4", "CB5"]},
            {"name": "East Cambridgeshire", "zip_codes": ["CB6", "CB7"]},
            {"name": "Fenland", "zip_codes": ["PE13", "PE14", "PE15", "PE16"]},
            {
                "name": "East Suffolk",
                "zip_codes": ["IP1", "IP10", "IP11", "IP12", "IP13"],
            },
            {"name": "Great Yarmouth", "zip_codes": ["NR29", "NR30", "NR31", "NR32"]},
            {"name": "Ipswich", "zip_codes": ["IP1", "IP2", "IP3", "IP4", "IP5"]},
            {
                "name": "Kings Lynn & West Norfolk",
                "zip_codes": ["PE30", "PE31", "PE32", "PE33", "PE34"],
            },
        ]

        for area_dict in areas_list:
            name = area_dict["name"]
            for zip_code in area_dict['zip_codes']:
            # Check if an area with the given name and zip code already exists
                existing_area = Area.objects.filter(name=name, zip=zip_code).first()

                if not existing_area:
                    # If the area does not exist, create a new one
                    new_area = Area(name=name, zip=zip_code)
                    new_area.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully created area: {new_area}")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Area already exists: {existing_area}")
                    )

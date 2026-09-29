from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Ejecuta secuencialmente todos los scripts de semillas (Emociones, Actividades, Logros)."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("=== INICIANDO CARGA MAESTRA DE DATOS DE SEMILLA ==="))
        
        self.stdout.write(self.style.NOTICE("\n[1/3] Carga de Emociones..."))
        call_command('seed_emociones')

        self.stdout.write(self.style.NOTICE("\n[2/3] Carga de Actividades..."))
        call_command('seed_actividades')

        self.stdout.write(self.style.NOTICE("\n[3/3] Carga de Logros..."))
        call_command('seed_logros')

        self.stdout.write(self.style.SUCCESS("\n=== CARGA MAESTRA COMPLETADA CON ÉXITO ==="))

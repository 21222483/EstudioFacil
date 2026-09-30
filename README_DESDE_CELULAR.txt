ESTUDIO FÁCIL — CREAR APK DESDE EL CELULAR SIN TERMUX

Esta carpeta incluye un workflow de GitHub Actions para que GitHub compile
la APK en sus servidores. No necesitas instalar Termux ni Buildozer en tu
celular.

PASOS:

1. Crea una cuenta en GitHub si no tienes una.
2. Entra a https://github.com/new
3. Crea un repositorio nuevo. Puedes llamarlo:
   EstudioFacil
4. Puedes dejarlo como Public.
5. Dentro del repositorio pulsa "Add file" -> "Upload files".
6. Sube TODOS los archivos de esta carpeta, incluyendo:
   - main.py
   - buildozer.spec
   - .github/workflows/build_apk.yml

   Es importante conservar la carpeta:
   .github/workflows/

7. Pulsa "Commit changes".

8. En tu repositorio entra en:
   Actions

9. Busca:
   "Crear APK Estudio Fácil"

10. Pulsa "Run workflow" y después vuelve a pulsar "Run workflow".

11. Espera a que termine el proceso. La primera compilación puede tardar
   bastante porque GitHub tiene que preparar Android SDK/NDK.

12. Cuando aparezca un check verde, entra en esa ejecución.

13. Busca la sección "Artifacts".

14. Descarga:
   EstudioFacil-APK

15. Descomprime ese archivo si viene en ZIP. Dentro estará el archivo .apk.

16. Abre el .apk en tu celular y pulsa "Instalar".

NOTA:
La compilación la hace GitHub en un servidor Linux. Buildozer oficialmente
está pensado para Linux/macOS (en Windows se usa WSL), por eso esta opción
evita tener que instalar todo el entorno de compilación en Android.

"""Filtros de plantilla de la app core (resaltado de codigo y formato)."""

import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

DIRECTIVAS_DOCKER = {
    "FROM",
    "RUN",
    "CMD",
    "LABEL",
    "EXPOSE",
    "ENV",
    "ADD",
    "COPY",
    "ENTRYPOINT",
    "VOLUME",
    "USER",
    "WORKDIR",
    "ARG",
}

COMANDOS_SHELL = {
    "docker",
    "pip",
    "python",
    "git",
    "npm",
    "kubectl",
    "mkdir",
    "cd",
    "export",
}

OPCIONES = {"--no-cache-dir", "-r", "-t", "-p", "-f", "-d", "-it"}


@register.filter(name="resaltar")
def resaltar(valor) -> str:
    """Resalta una linea de codigo (comentarios, directivas, strings)."""
    texto = escape(str(valor))

    if not texto.strip():
        return mark_safe("&nbsp;")

    if texto.lstrip().startswith("#"):
        return mark_safe(f'<span class="tok-comentario">{texto}</span>')

    partes = []
    for token in re.split(r"(\s+)", texto):
        if not token.strip():
            partes.append(token)
            continue

        if token.startswith(('"', "'")):
            partes.append(f'<span class="tok-cadena">{token}</span>')
        elif token.upper() in DIRECTIVAS_DOCKER:
            partes.append(f'<span class="tok-directiva">{token}</span>')
        elif token.lstrip("-") in OPCIONES:
            partes.append(f'<span class="tok-opcion">{token}</span>')
        elif token.split("/")[0] in COMANDOS_SHELL:
            partes.append(f'<span class="tok-comando">{token}</span>')
        elif re.fullmatch(r"-{1,2}[a-zA-Z][\w-]*", token):
            partes.append(f'<span class="tok-opcion">{token}</span>')
        else:
            partes.append(token)

    return mark_safe("".join(partes))


@register.filter(name="resaltar_shell")
def resaltar_shell(valor) -> str:
    """Resalta una linea de shell: comando, opciones y argumentos."""
    texto = escape(str(valor)).strip()
    if not texto:
        return mark_safe("&nbsp;")

    piezas = texto.split(" ")
    comando = piezas[0]
    resto = piezas[1:]

    partes = [f'<span class="tok-comando">{comando}</span>']
    for token in resto:
        if token.startswith("-"):
            partes.append(f'<span class="tok-opcion">{token}</span>')
        elif token.startswith(('"', "'")):
            partes.append(f'<span class="tok-cadena">{token}</span>')
        else:
            partes.append(token)

    return mark_safe(" ".join(partes))


@register.filter(name="sin_espacios")
def sin_espacios(valor) -> str:
    """Elimina espacios y comillas sobrantes de una cadena."""
    return str(valor).strip().strip('"')


@register.filter(name="get_item")
def get_item(diccionario, clave):
    """Accede a un diccionario con una clave variable (PK de un objeto)."""
    if isinstance(clave, str) and clave.isdigit():
        clave = int(clave)
    try:
        return diccionario.get(clave, [])
    except AttributeError:
        return []


@register.filter(name="siguiente_anio")
def siguiente_anio(valor) -> int:
    """Devuelve el valor + 1 (util para etiquetas de precio anual)."""
    return int(valor) + 1

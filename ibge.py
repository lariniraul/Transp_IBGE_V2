"""Consultas públicas ao IBGE. Unidades e anos vêm da resposta oficial."""
import gzip
import json
import time
from decimal import Decimal, InvalidOperation
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://servicodados.ibge.gov.br/api"
CONSULTAS = {
    "População, área e densidade (Censo)": ("4714", "93|6318|614"),
    "PIB municipal": ("5938", "37"),
}


def obter(caminho):
    for tentativa in range(3):
        try:
            req = Request(f"{BASE}/{caminho}", headers={"Accept": "application/json", "Accept-Encoding": "gzip"})
            with urlopen(req, timeout=40) as resposta:
                raw = resposta.read()
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            dados = json.loads(raw.decode("utf-8-sig"))
            if not isinstance(dados, list):
                raise ValueError("O IBGE retornou um formato inesperado.")
            return dados
        except (URLError, TimeoutError, OSError) as erro:
            if tentativa < 2:
                time.sleep(2 ** tentativa)
                continue
            raise ValueError("Não foi possível consultar o IBGE. Tente novamente mais tarde.") from erro
        except (UnicodeDecodeError, json.JSONDecodeError) as erro:
            raise ValueError("O IBGE não retornou JSON válido.") from erro


def municipios_sp():
    dados = obter("v1/localidades/estados/35/municipios?orderBy=nome")
    if not dados or any(not r.get("id") or not r.get("nome") for r in dados):
        raise ValueError("A lista de municípios do IBGE está vazia ou inválida.")
    return dados


def periodos(tabela):
    dados = obter(f"v3/agregados/{tabela}/periodos")
    anos = sorted({str(r["id"]) for r in dados if str(r.get("id", "")).isdigit()})
    if not anos:
        raise ValueError("Nenhum ano disponível nesta tabela do IBGE.")
    return anos


def consultar(tabela, variaveis, municipio, anos):
    if not anos:
        raise ValueError("Selecione pelo menos um ano.")
    query = urlencode({"localidades": f"N6[{municipio}]"})
    dados = obter(f"v3/agregados/{tabela}/periodos/{'|'.join(anos)}/variaveis/{variaveis}?{query}")
    linhas = []
    try:
        for variavel in dados:
            for resultado in variavel["resultados"]:
                for serie in resultado["series"]:
                    if str(serie["localidade"]["id"]) != str(municipio):
                        raise ValueError("O IBGE retornou um município diferente do solicitado.")
                    for ano, valor in serie["serie"].items():
                        if ano not in anos:
                            continue
                        linhas.append({"Indicador": variavel["variavel"], "Ano": ano,
                            "Valor": str(valor), "Unidade": variavel["unidade"],
                            "Município": serie["localidade"]["nome"], "Tabela SIDRA": tabela})
    except (KeyError, TypeError) as erro:
        raise ValueError("A estrutura dos indicadores do IBGE mudou ou está incompleta.") from erro
    return sorted(linhas, key=lambda r: (r["Ano"], r["Indicador"]))


def formatar_valor(valor):
    # Sinais especiais do SIDRA não são zeros e devem ser preservados.
    try:
        numero = Decimal(valor)
        if not numero.is_finite():
            return valor
        casas = max(0, -numero.as_tuple().exponent)
        return f"{numero:,.{casas}f}".translate(str.maketrans(",.", ".,"))
    except InvalidOperation:
        return valor

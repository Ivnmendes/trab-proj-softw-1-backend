import re
import time
import logging
import unicodedata

import requests
from django.core.management.base import BaseCommand

from medications.models import CID, Document, Medication

logger = logging.getLogger(__name__)


CLIENT_ID = "188_64xd8b39858gc4sksswo8wkksc0kwc4wc0gk44848okgo8ss40"
BASE_URL = "https://secweb.procergs.com.br/ame3/rest"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "client_id": CLIENT_ID,
    "connection": "keep-alive",
    "host": "secweb.procergs.com.br",
    "origin": "https://farmaciadigital.rs.gov.br",
    "pragma": "no-cache",
    "referer": "https://farmaciadigital.rs.gov.br/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    ),
}


def _get(url: str) -> dict | list:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()


def _sem_acentos(s: str) -> str:
    """Remove acentos para não causar erro 400 na API."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def buscar_medicamentos(termo: str) -> list[dict]:
    """Busca usando apenas o primeiro princípio ativo sem acentos."""
    primeiro_token = re.split(r"\s*\+\s*|\s+\d", termo)[0].strip()
    termo_limpo = _sem_acentos(primeiro_token)
    return _get(f"{BASE_URL}/medicamento/busca/{termo_limpo}")


def consultar_medicamento(med_id: int) -> dict:
    return _get(f"{BASE_URL}/medicamento/consulta/{med_id}")


def listar_documentos_paciente() -> list[dict]:
    return _get(f"{BASE_URL}/cidadao/listarDocumentosPaciente")


_DOSE_RE = re.compile(
    r"\b(\d+(?:[.,]\d+)?)\s*(MCG/ML|MG/ML|UI/ML|MCG|MG|G\b|ML\b|UI|%)"
)


def _parsear_nome(nome_comercial: str) -> tuple[str, str | None]:
    nome_limpo = re.sub(r"\s*\([^)]*\)\s*$", "", nome_comercial.strip()).upper()
    doses = [f"{m.group(1)} {m.group(2)}" for m in _DOSE_RE.finditer(nome_limpo)]
    nome_sem_doses = _DOSE_RE.sub("", nome_limpo)
    nome_sem_doses = re.sub(r"\s+", " ", nome_sem_doses).strip().strip("+").strip()
    nome_sem_doses = re.sub(r"\s*\+\s*", " + ", nome_sem_doses).strip()
    return nome_sem_doses or nome_comercial, (" + ".join(doses) if doses else None)


def _normalizar(s: str | None) -> str:
    """Normaliza para comparação: upper, sem acentos, sem espaços duplos."""
    if not s:
        return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s.strip().upper())


def encontrar_id_na_api(med: Medication, resultados: list[dict]) -> int | None:
    """
    Compara o medicamento do banco com os resultados da API.

    O campo concentration do banco pode ter sido cadastrado manualmente com
    a forma farmacêutica junto (ex: "125 mg injetável"). Para garantir o match,
    passamos a concentration do banco pelo mesmo _parsear_nome antes de comparar,
    assim "125 mg injetável" e "125 MG" viram ambos "125 MG".
    """
    generic_banco = _normalizar(med.generic_name)

    _, conc_banco_parsed = _parsear_nome(f"X {med.concentration or ''}")
    concentration_banco = _normalizar(conc_banco_parsed)

    for item in resultados:
        generic_api, conc_api = _parsear_nome(item["nomeComercial"])
        if (
            _normalizar(generic_api) == generic_banco
            and _normalizar(conc_api) == concentration_banco
        ):
            return item["id"]

    return None


def importar_documento(doc_data: dict) -> Document:
    nro  = str(doc_data["nroIntDoc"])
    nome = (doc_data.get("nome") or f"Documento {nro}").strip()
    doc, created = Document.objects.get_or_create(
        description=nro,
        defaults={"name": nome},
    )
    if not created and doc.name != nome:
        doc.name = nome
        doc.save(update_fields=["name"])
    return doc


def importar_cid(cid_data: dict, docs_protocolo: list[dict]) -> CID:
    codigo    = cid_data["codigo"]
    descricao = cid_data["descricao"]
    cid, created = CID.objects.get_or_create(
        code=codigo,
        defaults={"description": descricao},
    )
    if not created and cid.description != descricao:
        cid.description = descricao
        cid.save(update_fields=["description"])
    for doc_data in docs_protocolo:
        if doc_data.get("visivel"):
            cid.documents.add(importar_documento(doc_data))
    return cid


def _limpar_concentracao(conc: str | None) -> str | None:
    """
    Remove sufixos de forma farmacêutica, mantendo só doses numéricas.
    Ex: "125 mg injetável"          → "125 MG"
        "40 mg solução injetável"   → "40 MG"
        "0,1 mg/ml aplicação nasal" → "0,1 MG/ML"
        "125 mg"                    → "125 MG"  (só normaliza case)
    """
    if not conc:
        return conc
    doses = [f"{m.group(1)} {m.group(2)}" for m in _DOSE_RE.finditer(conc.upper())]
    return " + ".join(doses) if doses else conc


def atualizar_medicamento(med: Medication, detalhe: dict, docs_paciente: list[Document]) -> None:
    """
    Limpa o campo concentration e atualiza as relações M2M do medicamento.
    """
    conc_limpa = _limpar_concentracao(med.concentration)
    if conc_limpa != med.concentration:
        med.concentration = conc_limpa
        med.save(update_fields=["concentration"])

    for doc in docs_paciente:
        med.documents.add(doc)

    for med_cid in detalhe.get("medicamentoCidList") or []:
        cid_data = med_cid.get("cidViewED")
        if not cid_data:
            continue
        protocolo      = med_cid.get("protocoloClinicoViewED") or {}
        docs_protocolo = protocolo.get("protocoloClinicoDocumentoList") or []

        cid = importar_cid(cid_data, docs_protocolo)
        med.cids.add(cid)

        for doc_data in docs_protocolo:
            if doc_data.get("visivel"):
                med.documents.add(importar_documento(doc_data))


class Command(BaseCommand):
    help = (
        "Atualiza CIDs e documentos dos medicamentos ESPECIALIZADOS já existentes no banco "
        "a partir da API da Farmácia Digital RS. Não cria medicamentos novos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--delay",
            type=float,
            default=0.3,
            metavar="SEG",
            help="Intervalo em segundos entre requests (padrão: 0.3)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostra o que seria feito sem gravar nada no banco",
        )

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
        delay   = options["delay"]
        dry_run = options["dry_run"]

        self.stdout.write(self.style.MIGRATE_HEADING(
            "\n╔══════════════════════════════════════════╗\n"
            "║  Farmácia Digital RS — Atualização ESP   ║\n"
            "╚══════════════════════════════════════════╝"
        ))

        medicamentos = list(
            Medication.objects.filter(type=Medication.MedicationType.SPECIALIZED)
        )
        self.stdout.write(f"\n▶ {len(medicamentos)} medicamentos ESPECIALIZADOS no banco.")

        if not medicamentos:
            self.stdout.write(self.style.WARNING("  Nenhum medicamento para atualizar."))
            return

        self.stdout.write("\n▶ Buscando documentos obrigatórios do paciente...")
        try:
            raw_docs = listar_documentos_paciente()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"  Falha: {e}"))
            return

        obrigatorios  = [d for d in raw_docs if d.get("obrigatorio") and d.get("visivel")]
        docs_paciente = [importar_documento(d) for d in obrigatorios] if not dry_run else []
        self.stdout.write(self.style.SUCCESS(
            f"  {len(obrigatorios)} documento(s) obrigatório(s)."
        ))
        time.sleep(delay)

        self.stdout.write("\n▶ Buscando e atualizando cada medicamento...\n")

        atualizados = nao_encontrados = erros = 0
        nao_encontrados_lista: list[str] = []

        total = len(medicamentos)
        w     = len(str(total))

        for i, med in enumerate(medicamentos, start=1):
            label = f"{med.generic_name} {med.concentration or ''}".strip()
            prefix = f"  [{i:{w}}/{total}]"

            try:
                resultados = buscar_medicamentos(med.generic_name)
                time.sleep(delay)

                api_id = encontrar_id_na_api(med, resultados)

                if api_id is None:
                    nao_encontrados += 1
                    nao_encontrados_lista.append(label)
                    self.stdout.write(
                        self.style.WARNING(f"{prefix} NÃO ENCONTRADO  {label}")
                    )
                    continue

                if dry_run:
                    self.stdout.write(f"{prefix} encontrado id={api_id}  {label}")
                    atualizados += 1
                    continue

                detalhe = consultar_medicamento(api_id)
                time.sleep(delay)

                atualizar_medicamento(med, detalhe, docs_paciente)
                atualizados += 1
                self.stdout.write(
                    self.style.SUCCESS(f"{prefix} ✓  {label}  (id_api={api_id})")
                )

            except requests.RequestException as e:
                erros += 1
                self.stderr.write(self.style.WARNING(f"{prefix} ERRO  {label}: {e}"))

        sep = "═" * 44
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{sep}"))
        self.stdout.write(self.style.SUCCESS( f"  Atualizados:      {atualizados}"))
        self.stdout.write(self.style.WARNING( f"  Não encontrados:  {nao_encontrados}") if nao_encontrados else
                          self.style.SUCCESS( f"  Não encontrados:  {nao_encontrados}"))
        if erros:
            self.stdout.write(self.style.ERROR(f"  Erros:            {erros}"))
        self.stdout.write(self.style.MIGRATE_HEADING(f"{sep}"))

        if nao_encontrados_lista:
            self.stdout.write(self.style.WARNING(
                "\nMedicamentos não encontrados na API (revisar manualmente):"
            ))
            for nome in nao_encontrados_lista:
                self.stdout.write(f"  - {nome}")

        self.stdout.write("")
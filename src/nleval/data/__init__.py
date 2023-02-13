"""Interface with various databases to retrieve data."""
from nleval.data.annotated_ontology import (
    DISEASES,
    GOBP,
    GOCC,
    GOMF,
    HPO,
    DISEASES_ExperimentsFiltered,
    DISEASES_ExperimentsFull,
    DISEASES_KnowledgeFiltered,
    DISEASES_KnowledgeFull,
    DISEASES_TextminingFiltered,
    DISEASES_TextminingFull,
    DisGeNET,
    DisGeNET_Animal,
    DisGeNET_BEFREE,
    DisGeNET_Curated,
    DisGeNET_GWAS,
)
from nleval.data.annotation import (
    DISEASESAnnotation,
    DisGeNETAnnotation,
    GeneOntologyAnnotation,
    HumanPhenotypeOntologyAnnotation,
)
from nleval.data.network import (
    HIPPIE,
    SIGNOR,
    STRING,
    BioGRID,
    BioPlex,
    ComPPIHumanInt,
    FunCoup,
    HumanBaseTopGlobal,
    HumanNet,
    HuMAP,
    HuRI,
    OmniPath,
    PCNet,
    ProteomeHD,
)
from nleval.data.ontology import GeneOntology, MondoDiseaseOntology

__all__ = classes = [
    # Networks
    "BioGRID",
    "BioPlex",
    "ComPPIHumanInt",
    "FunCoup",
    "HIPPIE",
    "HuRI",
    "HuMAP",
    "HumanBaseTopGlobal",
    "HumanNet",
    "OmniPath",
    "PCNet",
    "ProteomeHD",
    "SIGNOR",
    "STRING",
    # Gene set collections
    "DISEASES",
    "DISEASES_ExperimentsFiltered",
    "DISEASES_ExperimentsFull",
    "DISEASES_KnowledgeFiltered",
    "DISEASES_KnowledgeFull",
    "DISEASES_TextminingFiltered",
    "DISEASES_TextminingFull",
    "DisGeNET",
    "DisGeNET_Animal",
    "DisGeNET_BEFREE",
    "DisGeNET_Curated",
    "DisGeNET_GWAS",
    "GOBP",
    "GOCC",
    "GOMF",
    "HPO",
    # Annotations
    "DISEASESAnnotation",
    "DisGeNETAnnotation",
    "GeneOntologyAnnotation",
    "HumanPhenotypeOntologyAnnotation",
    # Ontologies
    "GeneOntology",
    "MondoDiseaseOntology",
]

# observer.py

#  importação do módulo abc (Abstract Base Classes) do Python, que fornece infraestrutura para criar classes abstratas
from abc import ABC, abstractmethod

# importação do módulo typing (tipos genéricos do módulo typing):
# List - representa uma lista e permite especificar o tipo dos elementos contidos na lista;
# dict - permite especificar os tipos das chaves e valores do dicionário;
# Any - (int, str, list, etc.)
from typing import List, Dict, Any
from datetime import datetime
import json
import os

# Interface do Observer
class AnalyticsObserver(ABC):
    @abstractmethod
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        pass

    def _save_to_json(self, filename: str, data: Dict[str, Any]) -> None:
        """Método auxiliar para guardar dados em arquivo JSON"""
        os.makedirs("analytics_data", exist_ok=True)
        filepath = f"analytics_data/{filename}"

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        data["timestamp"] = datetime.now().isoformat()
        existing_data.append(data)

        with open(filepath, "w") as file:
            json.dump(existing_data, file, indent=4)


# Observer Qualitativo
class QualitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        qualitative_data = {
            "activity_id": activity_id,
            "student_id": student_id,
            "type": "qualitative",
            "data": {
                "acesso_atividade": data.get("acesso_atividade", False),
                "download_recursos": data.get("download_recursos", False),
                "upload_documentos": data.get("upload_documentos", False),
                "relatorio_respostas": data.get("relatorio_respostas", ""),
            },
        }
        self._save_to_json(f"qualitative_{activity_id}.json", qualitative_data)
        print(
            f"Dados qualitativos salvos para estudante {student_id} na atividade {activity_id}"
        )


# Observer Quantitativo
class QuantitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        quantitative_data = {
            "activity_id": activity_id,
            "student_id": student_id,
            "type": "quantitative",
            "data": {
                "numero_acessos": data.get("numero_acessos", 0),
                "downloads_recursos": data.get("downloads_recursos", 0),
                "progresso_atividade": data.get("progresso_atividade", 0.0),
            },
        }
        self._save_to_json(f"quantitative_{activity_id}.json", quantitative_data)
        print(
            f"Dados quantitativos salvos para estudante {student_id} na atividade {activity_id}"
        )


# Subject (Observable)
class ActivityAnalytics:
    def __init__(self):
        self._observer: List[AnalyticsObserver] = []

    def attach(self, observer: AnalyticsObserver) -> None:
        """Adiciona um novo observer"""
        if observer not in self._observer:
            self._observer.append(observer)

    def detach(self, observer: AnalyticsObserver) -> None:
        """Remove um observer"""
        self._observer.remove(observer)

    def notify(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        """Notifica todos os observers"""
        for observer in self._observer:
            observer.update(activity_id, student_id, data)

    def record_activity(
        self, activity_id: str, student_id: str, data: Dict[str, Any]
    ) -> None:
        """Registra uma atividade e notifica os observers"""
        print(
            f"Registrando atividade para estudante {student_id} na atividade {activity_id}"
        )
        self.notify(activity_id, student_id, data)

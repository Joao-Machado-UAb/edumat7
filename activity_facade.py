# activity_facade.py

from singleton_db import SingletonDB
from observer import (
    ActivityAnalytics,
    QualitativeAnalyticsObserver,
    QuantitativeAnalyticsObserver,
)


class ActivityFacade:
    def __init__(self):
        self.db = SingletonDB()
        # Inicializar o sistema de analytics
        self.analytics = ActivityAnalytics()
        # Anexar os observers
        self.analytics.attach(QualitativeAnalyticsObserver())
        self.analytics.attach(QuantitativeAnalyticsObserver())

    def create_activity(self, activity_id):
        return self.db.create_instance(activity_id)

    def access_activity_data(self, activity_id):
        # Registrar o acesso à atividade
        if activity_id:
            self.analytics.record_activity(
                activity_id,
                "student_test",  # Você deve passar o ID real do estudante aqui
                {"acesso_atividade": True, "numero_acessos": 1},
            )
        return self.db.access_data(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        return self.db.execute_operations(activity_id, resumo, instrucoes)

    def get_analytics_list(self):
        return {
            "qualAnalytics": [
                {"name": "Acesso à atividade", "type": "boolean"},
                {"name": "Download de recursos", "type": "boolean"},
                {"name": "Upload de documentos", "type": "boolean"},
                {
                    "name": "Relatório das respostas concretamente dadas",
                    "type": "text/plain",
                },
            ],
            "quantAnalytics": [
                {"name": "Número de acessos", "type": "integer"},
                {"name": "Download de recursos", "type": "integer"},
                {"name": "Progresso na atividade (%)", "type": "integer"},
            ],
        }

    def get_analytics_data(self):
        return [
            {
                "inveniraStdID": 1001,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {
                        "name": "Relatório das respostas concretamente dadas",
                        "value": "Suficiente",
                    },
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 50},
                    {"name": "Download de recursos", "value": 12},
                    {"name": "Progresso na atividade (%)", "value": 10.0},
                ],
            },
            {
                "inveniraStdID": 1002,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {
                        "name": "Relatório das respostas concretamente dadas",
                        "value": "Suficiente",
                    },
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 60},
                    {"name": "Download de recursos", "value": 16},
                    {"name": "Progresso na atividade (%)", "value": 40.0},
                ],
            },
        ]

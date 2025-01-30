# activity_manager.py

from singleton_db import SingletonDB
from observers import (
    ActivityAnalytics,
    QualitativeAnalyticsObserver,
    QuantitativeAnalyticsObserver,
)


class ActivityManager:
    """
    Classe principal responsável pela gestão de atividades educacionais.
    Substitui o ActivityFacade anterior, consolidando as responsabilidades
    e eliminando o antipadrão Poltergeist.
    """

    def __init__(self):
        self._db = SingletonDB()
        self._analytics = self._setup_analytics()
        self._default_analytics_data = self._setup_default_analytics()

    def _setup_analytics(self):
        """Configura e retorna o sistema de analytics"""
        analytics = ActivityAnalytics()
        analytics.attach(QualitativeAnalyticsObserver())
        analytics.attach(QuantitativeAnalyticsObserver())
        return analytics

    def _setup_default_analytics(self):
        """Define os dados padrão de analytics"""
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

    def create_activity(self, activity_id):
        """
        Cria uma nova atividade e regista o evento nos analytics.

        Args:
            activity_id: Identificador único da atividade
        Retorna:
            Dict com os dados da atividade criada
        """
        activity_data = self._db.create_instance(activity_id)
        self._analytics.record_activity(
            activity_id, "system", {"acesso_atividade": True, "numero_acessos": 1}
        )
        return activity_data

    def get_activity(self, activity_id, student_id=None):
        """
        Obtém os dados duma atividade e regista o acesso nos analytics.

        Args:
            activity_id: Identificador da atividade
            student_id: Identificador do estudante (opcional)
        Retorna:
            Dict com os dados da atividade ou None se não existir
        """
        activity_data = self._db.access_data(activity_id)

        if activity_id and student_id:
            self._analytics.record_activity(
                activity_id,
                student_id,
                {"acesso_atividade": True, "numero_acessos": 1, "timestamp": "auto"},
            )

        return activity_data

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        """
        Atualiza os dados duma atividade existente.

        Args:
            activity_id: Identificador da atividade
            resumo: Novo resumo (opcional)
            instrucoes: Novas instruções (opcional)
        Retorna:
            Dict com os dados atualizados da atividade
        """
        return self._db.execute_operations(activity_id, resumo, instrucoes)

    def get_analytics_config(self):
        """
        Retorna a configuração dos analytics disponíveis.

        Retorna:
            Dict com as configurações dos analytics qualitativos e quantitativos
        """
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
        """
        Retorna os dados de analytics acumulados.

        Returns:
            Lista com todos os dados de analytics
        """
        return self._default_analytics_data

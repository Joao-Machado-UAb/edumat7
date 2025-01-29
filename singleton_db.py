# singleton_db.py

DEFAULT_RESUMO = "Resumo de equações de 7º ano: Aqui pode encontrar um resumo de equações de 7º ano."


class SingletonDB:
    # Classe Singleton para administrar o banco de dados

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonDB, cls).__new__(cls)
            cls._instance.db = {}
        return cls._instance

    def get_database(self):
        # Retorna o banco de dados
        return self._instance.db

    def create_instance(self, activity_id):
        """
        Cria uma entrada no banco de dados se ela não existir
                Parâmetros:
            activity_id: ID da atividade a ser criada
        Retorna:
            A entrada criada ou já existente
        """
        if activity_id not in self._instance.db:
            self._instance.db[activity_id] = {
                "resumo": DEFAULT_RESUMO,
                "instrucoes": "https://www.matematica.pt/aulas-matematica.php?ano=7",
            }
        return self._instance.db[activity_id]

    def access_data(self, activity_id):
        """
        Retorna os dados de uma entrada específica

        Parâmetros:
            activity_id: ID da atividade a ser acessada
        Retorna:
            Os dados da entrada, ou None se não existir
        """
        return self._instance.db.get(activity_id, None)

    def execute_operations(self, activity_id, resumo=None, instrucoes=None):
        """
        Atualiza os dados de uma entrada existente no banco de dados

        Parâmetros:
            activity_id: ID da atividade a ser atualizada
            resumo: Novo resumo (opcional).
            instrucoes: Novas instruções (opcional).
        """
        if activity_id not in self._instance.db:
            raise KeyError(
                f"Activity ID '{activity_id}' não encontrado no banco de dados."
            )
        if resumo:
            self._instance.db[activity_id]["resumo"] = resumo
        if instrucoes:
            self._instance.db[activity_id]["instrucoes"] = instrucoes
        return self._instance.db[activity_id]

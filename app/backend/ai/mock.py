from .base import BaseAIService

class MockAIService(BaseAIService):

    def analyze(self, defect: str, zone: str) -> str:
        return (
            f"Обнаружен дефект: {defect}. "
            f"Зона: {zone}. "
            "Рекомендуется дополнительное обследование."
        )

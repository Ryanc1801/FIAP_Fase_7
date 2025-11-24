"""
Módulo aws_mensageria
---------------------
Centraliza o envio de mensagens para o Amazon SNS.

- Este módulo **não** armazena chaves de acesso.
- As credenciais devem estar configuradas via AWS CLI ou variáveis de ambiente.
- O ARN do tópico é lido da variável de ambiente `FARMTECH_SNS_ARN`.

"""

from __future__ import annotations
import os
from typing import Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _obter_topico_arn() -> str:
    arn = os.getenv("FARMTECH_SNS_ARN")
    if not arn:
        raise RuntimeError(
            "Variável de ambiente FARMTECH_SNS_ARN não configurada. "
            "Defina o ARN do tópico SNS antes de usar a mensageria."
        )
    return arn


def enviar_alerta_sns(mensagem: str, assunto: Optional[str] = None) -> None:
    """Envia uma mensagem para o tópico SNS configurado.

    Levanta exceção em caso de erro (para ser tratada pela interface).
    """
    topic_arn = _obter_topico_arn()
    sns = boto3.client("sns")

    kwargs = {"TopicArn": topic_arn, "Message": mensagem}
    if assunto:
        kwargs["Subject"] = assunto

    try:
        sns.publish(**kwargs)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Falha ao enviar mensagem para o SNS: {exc}") from exc
